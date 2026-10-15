"""Executa experimentos pareados e gera CSV e registro do ambiente."""

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
                    comparacoes = ''  # Desafio extra será acrescentado na etapa 4.
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
            contagens = [linha['comparacoes'] for linha in grupo if linha['comparacoes'] != '']
            linha = dict(grupo[0])
            linha.update(tipo='media', repeticao='', tempo_s=statistics.mean(tempos),
                         desvio_tempo_s=statistics.stdev(tempos),
                         comparacoes=statistics.mean(contagens) if contagens else '',
                         desvio_comparacoes=statistics.stdev(contagens) if contagens else '')
            resumo.append(linha)
    return resumo


def salvar_csv(linhas, resumo):
    with (PASTA / 'dados.csv').open('w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(linhas[0]))
        escritor.writeheader()
        escritor.writerows(linhas + resumo)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repeticoes', type=int, default=30)
    parser.add_argument('--semente', type=int, default=20261015)
    args = parser.parse_args()
    if args.repeticoes < 10:
        parser.error('Use pelo menos 10 repetições, conforme o enunciado.')

    linhas = executar_experimentos(args.repeticoes, args.semente)
    resumo = resumir(linhas)
    salvar_csv(linhas, resumo)
    metadados = {
        'gerado_em_utc': datetime.now(timezone.utc).isoformat(),
        'python': sys.version, 'implementacao': platform.python_implementation(),
        'sistema': platform.platform(), 'processador': platform.processor() or platform.machine(),
        'repeticoes': args.repeticoes,
        'semente': args.semente, 'tamanhos': TAMANHOS,
        'entradas': 'Permutações de range(n), Random(semente + n); uma nova por repetição.',
        'lotes': '50 chamadas por entrada para n <= 100; 5 para n > 100.',
        'tempo': 'perf_counter_ns; cópia e contadores internos dos algoritmos próprios incluídos; sorted com inteiros.',
        'comparacoes': 'Comparações entre valores de Insertion e Merge; sorted ainda sem contagem.',
    }
    (PASTA / 'ambiente.json').write_text(json.dumps(metadados, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Pronto: dados.csv e ambiente.json atualizados.')


if __name__ == '__main__':
    main()
