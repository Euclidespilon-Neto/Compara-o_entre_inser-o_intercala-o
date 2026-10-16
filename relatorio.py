"""Gera o relatório a partir das médias reais, sem fixar conclusões antecipadas."""

import math


def gerar_relatorio(resumo, ambiente, pasta):
    dados = {(linha['n'], linha['algoritmo']): linha for linha in resumo}
    tamanhos = sorted({linha['n'] for linha in resumo})

    def vencedores(campo):
        return [n for n in tamanhos if dados[n, 'Merge Sort'][campo] < dados[n, 'Insertion Sort'][campo]]

    def descrever_virada(campo):
        ganhos = vencedores(campo)
        if not ganhos:
            return 'O Merge Sort não ficou abaixo do Insertion Sort em nenhum tamanho testado.'
        primeiro = ganhos[0]
        indice = tamanhos.index(primeiro)
        texto = f'O primeiro tamanho testado com média menor para o Merge Sort foi **n = {primeiro}**.'
        if indice:
            anterior = tamanhos[indice - 1]
            texto += (f' A mudança observada está entre os pontos amostrados n = {anterior} e n = {primeiro}.'
                      ' Os inteiros intermediários não foram medidos; não é possível apontar uma fronteira exata nesse intervalo.')
        else:
            texto += ' Ele já teve vantagem no menor tamanho da amostra; uma virada anterior não foi observada.'
        retornos = [n for n in tamanhos if n > primeiro and n not in ganhos]
        if retornos:
            texto += f' A vantagem não foi contínua: em {retornos} o Merge não teve média menor.'
        else:
            texto += ' A vantagem continuou nos demais tamanhos amostrados.'
        return texto

    tempos = vencedores('tempo_s')
    comparacoes = vencedores('comparacoes')
    primeiro_t = tempos[0] if tempos else None
    primeiro_c = comparacoes[0] if comparacoes else None
    if primeiro_t is None or primeiro_c is None:
        confronto = 'Não foram observadas duas viradas que permitam afirmar coincidência entre os gráficos.'
    elif primeiro_t == primeiro_c:
        confronto = (f'Nesta execução, os primeiros tamanhos amostrados com vantagem do Merge coincidiram: n = {primeiro_t}.'
                     ' Isso não prova uma igualdade universal entre as duas fronteiras.')
    else:
        confronto = (f'Nesta execução, os pontos não coincidiram: **tempo em n = {primeiro_t}** e '
                     f'**comparações em n = {primeiro_c}**.')

    tabela = ['| n | Insertion: tempo (µs) | Merge: tempo (µs) | sorted: tempo (µs) | Insertion: comparações | Merge: comparações | sorted: comparações |',
              '|---:|---:|---:|---:|---:|---:|---:|']
    extra = ['| n | sorted: média de comparações | n log₂ n | log₂(n!) | sorted / (n log₂ n) |',
             '|---:|---:|---:|---:|---:|']
    for n in tamanhos:
        grupo = [dados[n, nome] for nome in ('Insertion Sort', 'Merge Sort', 'sorted()')]
        celulas = [str(n)]
        celulas.extend(f"{x['tempo_s'] * 1e6:.3f} ± {x['desvio_tempo_s'] * 1e6:.3f}" for x in grupo)
        celulas.extend(f"{x['comparacoes']:.2f} ± {x['desvio_comparacoes']:.2f}" for x in grupo)
        tabela.append('| ' + ' | '.join(celulas) + ' |')
        ref = n * math.log2(n)
        limite = math.lgamma(n + 1) / math.log(2)
        extra.append(f"| {n} | {grupo[2]['comparacoes']:.2f} | {ref:.2f} | {limite:.2f} | {grupo[2]['comparacoes'] / ref:.3f} |")

    maior = tamanhos[-1]
    insercao = dados[maior, 'Insertion Sort']
    intercalacao = dados[maior, 'Merge Sort']
    razao_t = insercao['tempo_s'] / intercalacao['tempo_s']
    razao_c = insercao['comparacoes'] / intercalacao['comparacoes']
    texto = f'''# Comparação de algoritmos de ordenação

**Integrantes:** Euclides Carlos Pilon Neto e Gabriela de Araújo Reis.  
**Disciplina:** Estrutura de Dados Avançados.  
**Execução registrada (UTC):** {ambiente['gerado_em_utc']}.

## 1. Objetivo e implementação

O trabalho compara Insertion Sort, Merge Sort e a função `sorted()` do Python.
Foram medidos o tempo de execução e o número de comparações para os dez tamanhos exigidos.
O desafio extra contabiliza as comparações do `sorted()` com uma classe que implementa `__lt__`.

No Insertion Sort, cada elemento é colocado na posição correta da parte já ordenada.
O contador aumenta antes da comparação entre a chave e o elemento anterior, inclusive quando ela é falsa.
A expressão `chave < resultado[j]` equivale a `resultado[j] > chave` para os inteiros utilizados.

No Merge Sort, a lista é dividida em duas metades e cada metade é ordenada recursivamente.
Na intercalação, comparamos os primeiros elementos ainda disponíveis e copiamos o menor.
A contagem final soma as comparações das duas chamadas e da intercalação.
Copiar a sobra de uma metade não acrescenta comparações entre valores.

As funções devolvem `(lista_ordenada, comparacoes)` e preservam a entrada.
Ambas são estáveis: elementos com a mesma chave mantêm sua ordem relativa.
O Insertion não desloca elementos iguais à chave; o Merge escolhe a esquerda em um empate.

## 2. Procedimento experimental

- Tamanhos: `{tamanhos}`.
- Repetições: **{ambiente['repeticoes']} entradas aleatórias por tamanho**, acima do mínimo de dez.
- Semente: **{ambiente['semente']}**, usando um gerador `Random(semente + n)` para cada tamanho.
- Cada entrada é uma permutação de `range(n)`, com valores distintos; duplicatas são cobertas nos testes.
- Os três algoritmos recebem o mesmo conteúdo em cada repetição, sem alteração da entrada.
- Há três chamadas iniciais de aquecimento por algoritmo e rotação da ordem de medição entre as repetições.
- Cronômetro: `time.perf_counter_ns()`. Medimos 50 chamadas por entrada até n = 100 e cinco acima disso.
  O tempo do lote é dividido pela quantidade de chamadas. Depois calculamos a média entre as entradas.
- A geração das listas, a contagem separada do `sorted()` e a validação ficam fora do trecho cronometrado.
- A cópia das listas e a contagem interna de Insertion/Merge estão incluídas nos seus tempos.
  O tempo de `sorted()` usa inteiros normais. Portanto, os tempos são das implementações descritas,
  e não de algoritmos abstratos com todos os custos igualados.
- `dados.csv` conserva uma linha bruta por algoritmo/entrada e uma linha de média por algoritmo/tamanho.
  O desvio padrão é amostral. Repetir a semente reproduz as entradas e contagens neste ambiente,
  mas não torna os tempos idênticos.

**Ambiente efetivo:** {ambiente['implementacao']} {ambiente['python'].split()[0]};
{ambiente['sistema']}; processador informado: {ambiente['processador']};
Matplotlib {ambiente['matplotlib']}. Os detalhes estão em `ambiente.json`.
Os resultados descrevem esse ambiente, sem atribuí-los ao computador pessoal dos integrantes.

## 3. Tabela de resultados

Valores apresentados como **média ± desvio padrão amostral**. A tabela converte segundos para
microssegundos (1 µs = 10⁻⁶ s); o CSV e o gráfico de tempo usam segundos.
Uma contagem individual é inteira e exata. Sua média entre diferentes listas pode ser fracionária.

{chr(10).join(tabela)}

## 4. Gráficos

![Tempo de execução](grafico_tempos.png)

![Número de comparações](grafico_comparacoes.png)

O painel da esquerda usa escalas logarítmicas para mostrar todos os tamanhos e curvas.
O painel da direita usa escalas lineares e destaca as listas pequenas.
As linhas ligam os pontos medidos e não representam medições dos valores intermediários.
A linha n log₂ n é uma referência de crescimento, não um mínimo exato por entrada.

## 5. Em qual n o Merge passa a ser mais rápido?

{descrever_virada('tempo_s')}

Esse é o valor observado entre os tamanhos exigidos pelo enunciado. Um limiar exato e universal
não pode ser obtido com essa amostragem: o hardware, a execução e o código influenciam os tempos.
Para investigar o intervalo, seria necessário medir também seus valores intermediários e repetir
o experimento. Diferenças pequenas devem ser avaliadas junto com a dispersão; não foi realizado
um teste de significância estatística.

## 6. Os gráficos apresentam a mesma virada?

{descrever_virada('comparacoes')}

{confronto}

Contar comparações e medir tempo descrevem aspectos diferentes. O tempo inclui movimentação de
elementos, criação de listas, chamadas recursivas, controle dos laços e atualização dos contadores.
O Merge pode economizar comparações, mas gastar mais tempo com essas outras operações em listas
pequenas. A decisão deve usar os dados observados, sem assumir previamente que as viradas coincidem
ou que ocorrem em um tamanho fixo.

## 7. Por que sorted() não decide sozinho qual algoritmo é mais eficiente?

O `sorted()` é uma referência prática do recurso disponível na linguagem. No CPython, sua
implementação nativa otimizada em C difere das nossas funções escritas em Python.
Ela é adaptativa e aproveita trechos ordenados. A documentação a descreve como Timsort;
versões modernas do CPython também usam a estratégia Powersort para decidir a ordem das intercalações.

Assim, essa medição mistura algoritmo, implementação e otimizações. Uma vantagem do `sorted()`
não prova, por si só, que nossa versão do Insertion ou do Merge tem determinada complexidade.
A análise dos dois algoritmos próprios considera suas comparações, o crescimento com n e os custos
de suas implementações. Além disso, eles contabilizam comparações durante a medição; o `sorted()`
com inteiros não executa o contador Python do desafio nesse trecho.

## 8. Continuação na etapa 6

O caso prático do Insertion Sort, a discussão detalhada do desafio extra, a síntese e
as referências serão acrescentados na revisão de Gabriela. Os resultados desta versão
já incluem as três ordenações e as contagens do desafio.
'''
    (pasta / 'RELATORIO.md').write_text(texto, encoding='utf-8')
