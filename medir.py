"""Executa experimentos pareados e refaz CSV e gráficos."""

import argparse
import csv
import json
import math
import platform
import random
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from ordenacao import insertion_sort, merge_sort

TAMANHOS = [5, 10, 20, 30, 50, 75, 100, 200, 500, 1000]
ALGORITMOS = {'Insertion Sort': insertion_sort, 'Merge Sort': merge_sort, 'sorted()': sorted}
PASTA = Path(__file__).resolve().parent


class ElementoContador:
    """Instrumenta somente as comparações de valores feitas por sorted()."""

    comparacoes = 0

    def __init__(self, valor):
        self.valor = valor

    def __lt__(self, outro):
        ElementoContador.comparacoes += 1
        return self.valor < outro.valor


def contar_sorted(entrada):
    objetos = [ElementoContador(valor) for valor in entrada]
    ElementoContador.comparacoes = 0
    resultado = sorted(objetos)
    contagem = ElementoContador.comparacoes
    if [objeto.valor for objeto in resultado] != sorted(entrada):
        raise AssertionError('O sorted instrumentado produziu resultado incorreto.')
    return contagem


def cronometrar(funcao, entrada, lote):
    """Tempo médio por chamada do lote; geração e validação ficam de fora."""
    inicio = time.perf_counter_ns()
    for _ in range(lote):
        resultado = funcao(entrada)
    tempo_s = (time.perf_counter_ns() - inicio) / lote / 1_000_000_000
    return tempo_s, resultado


def executar_experimentos(repeticoes, semente, tamanhos=TAMANHOS):
    linhas = []
    for funcao in ALGORITMOS.values():
        for _ in range(3):
            funcao(list(range(30, 0, -1)))

    for n in tamanhos:
        gerador = random.Random(semente + n)
        lote = 50 if n <= 100 else 5
        for repeticao in range(1, repeticoes + 1):
            # Permutação aleatória: n valores distintos, todos os algoritmos
            # recebem a mesma entrada nesta repetição.
            entrada = gerador.sample(range(n), n)
            esperado = sorted(entrada)
            nomes = list(ALGORITMOS)
            deslocamento = (repeticao - 1) % len(nomes)
            nomes = nomes[deslocamento:] + nomes[:deslocamento]
            for nome in nomes:
                tempo_s, retorno = cronometrar(ALGORITMOS[nome], entrada, lote)
                if nome == 'sorted()':
                    resultado = retorno
                    comparacoes = contar_sorted(entrada)
                else:
                    resultado, comparacoes = retorno
                if resultado != esperado:
                    raise AssertionError(f'Resultado incorreto: {nome}, n={n}.')
                linhas.append({
                    'tipo': 'bruto', 'n': n, 'repeticao': repeticao,
                    'algoritmo': nome, 'tempo_s': tempo_s, 'desvio_tempo_s': '',
                    'comparacoes': comparacoes, 'desvio_comparacoes': '',
                    'lote': lote, 'semente': semente,
                    'referencia_n_log2_n': n * math.log2(n),
                    'referencia_log2_fatorial': math.lgamma(n + 1) / math.log(2),
                })
        print(f'n={n}: {repeticoes} entradas medidas.')
    return linhas


def resumir(linhas):
    resumo = []
    for n in sorted({linha['n'] for linha in linhas}):
        for nome in ALGORITMOS:
            grupo = [linha for linha in linhas if linha['n'] == n and linha['algoritmo'] == nome]
            tempos = [linha['tempo_s'] for linha in grupo]
            contagens = [linha['comparacoes'] for linha in grupo]
            linha = dict(grupo[0])
            linha.update(tipo='media', repeticao='', tempo_s=statistics.mean(tempos),
                         desvio_tempo_s=statistics.stdev(tempos),
                         comparacoes=statistics.mean(contagens),
                         desvio_comparacoes=statistics.stdev(contagens))
            resumo.append(linha)
    return resumo


def salvar_csv(linhas, resumo):
    with (PASTA / 'dados.csv').open('w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(linhas[0]))
        escritor.writeheader()
        escritor.writerows(linhas + resumo)


def gerar_graficos(resumo):
    import matplotlib
    matplotlib.use('Agg')  # Funciona também em ambientes sem interface gráfica.
    import matplotlib.pyplot as plt

    cores = {'Insertion Sort': '#d76d35', 'Merge Sort': '#2363b4', 'sorted()': '#158276'}
    tamanhos = sorted({linha['n'] for linha in resumo})
    plt.rcParams.update({'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False})
    for campo, titulo, unidade, nome_arquivo in (
        ('tempo_s', 'Tempo de execução por tamanho da lista', 'Tempo médio por chamada (s)', 'grafico_tempos.png'),
        ('comparacoes', 'Comparações entre valores por tamanho da lista', 'Média de comparações por ordenação', 'grafico_comparacoes.png'),
    ):
        fig, eixos = plt.subplots(1, 2, figsize=(13.5, 5.4), gridspec_kw={'width_ratios': [1.25, 1]})
        for nome in ALGORITMOS:
            grupo = [linha for linha in resumo if linha['algoritmo'] == nome]
            xs = [linha['n'] for linha in grupo]
            ys = [linha[campo] for linha in grupo]
            eixos[0].plot(xs, ys, 'o-', label=nome, color=cores[nome], linewidth=2, markersize=4)
            pequenos = [linha for linha in grupo if linha['n'] <= 100]
            eixos[1].plot([x['n'] for x in pequenos], [x[campo] for x in pequenos],
                          'o-', color=cores[nome], linewidth=2, markersize=4)
        if campo == 'comparacoes':
            eixos[0].plot(tamanhos, [n * math.log2(n) for n in tamanhos], '--', color='#64748b', label='Referência n log₂ n')
            pequenos = [n for n in tamanhos if n <= 100]
            eixos[1].plot(pequenos, [n * math.log2(n) for n in pequenos], '--', color='#64748b')
        eixos[0].set_xscale('log')
        eixos[0].set_yscale('log')
        eixos[0].set_title('Visão geral · escalas logarítmicas', fontsize=11)
        eixos[0].legend(fontsize=9)
        eixos[1].set_title('Detalhe de n ≤ 100 · escalas lineares', fontsize=11)
        for eixo in eixos:
            eixo.set_xlabel('Número de elementos (n)')
            eixo.set_ylabel(unidade)
            eixo.grid(True, alpha=0.2)
        if campo == 'tempo_s':
            eixos[1].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        fig.suptitle(titulo, fontsize=16, fontweight='bold')
        fig.tight_layout(rect=(0, 0.04, 1, 0.93))
        fig.text(0.5, 0.015, 'Mesmas entradas para os três algoritmos; médias das repetições. Fonte: dados.csv.', ha='center', fontsize=9)
        fig.savefig(PASTA / nome_arquivo, dpi=170)
        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repeticoes', type=int, default=30)
    parser.add_argument('--semente', type=int, default=20261015)
    args = parser.parse_args()
    if args.repeticoes < 10:
        parser.error('Use pelo menos 10 repetições, conforme o enunciado.')
    try:
        import matplotlib
    except ImportError:
        parser.exit(1, 'Instale matplotlib: python -m pip install matplotlib\n')

    linhas = executar_experimentos(args.repeticoes, args.semente)
    resumo = resumir(linhas)
    salvar_csv(linhas, resumo)
    metadados = {
        'gerado_em_utc': datetime.now(timezone.utc).isoformat(),
        'python': sys.version, 'implementacao': platform.python_implementation(),
        'sistema': platform.platform(), 'processador': platform.processor() or platform.machine(),
        'matplotlib': matplotlib.__version__, 'repeticoes': args.repeticoes,
        'semente': args.semente, 'tamanhos': TAMANHOS,
        'entradas': 'Permutações de range(n), Random(semente + n); uma nova por repetição.',
        'lotes': '50 chamadas por entrada para n <= 100; 5 para n > 100.',
        'tempo': 'perf_counter_ns; cópia e contadores internos dos algoritmos próprios incluídos; sorted com inteiros.',
        'comparacoes': 'Comparações entre valores; sorted contado separadamente usando __lt__.',
    }
    (PASTA / 'ambiente.json').write_text(json.dumps(metadados, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    gerar_graficos(resumo)
    print('Pronto: dados.csv, ambiente.json, dois gráficos atualizados.')


if __name__ == '__main__':
    main()
