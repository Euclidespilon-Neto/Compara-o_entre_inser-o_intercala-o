# Comparação de algoritmos de ordenação

**Integrantes:** Euclides Carlos Pilon Neto e Gabriela de Araújo Reis.  
**Disciplina:** Estrutura de Dados Avançados.  
**Execução registrada (UTC):** 2026-10-16T00:21:43.657093+00:00.

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

- Tamanhos: `[5, 10, 20, 30, 50, 75, 100, 200, 500, 1000]`.
- Repetições: **30 entradas aleatórias por tamanho**, acima do mínimo de dez.
- Semente: **20261015**, usando um gerador `Random(semente + n)` para cada tamanho.
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

**Ambiente efetivo:** CPython 3.14.2;
Windows-11-10.0.26200-SP0; processador informado: Intel64 Family 6 Model 158 Stepping 9, GenuineIntel;
Matplotlib 3.11.2. Os detalhes estão em `ambiente.json`.
Os resultados descrevem esse ambiente, sem atribuí-los ao computador pessoal dos integrantes.

## 3. Tabela de resultados

Valores apresentados como **média ± desvio padrão amostral**. A tabela converte segundos para
microssegundos (1 µs = 10⁻⁶ s); o CSV e o gráfico de tempo usam segundos.
Uma contagem individual é inteira e exata. Sua média entre diferentes listas pode ser fracionária.

| n | Insertion: tempo (µs) | Merge: tempo (µs) | sorted: tempo (µs) | Insertion: comparações | Merge: comparações | sorted: comparações |
|---:|---:|---:|---:|---:|---:|---:|
| 5 | 1.148 ± 0.209 | 4.983 ± 0.574 | 0.208 ± 0.013 | 7.43 ± 1.81 | 7.00 ± 0.87 | 8.73 ± 1.55 |
| 10 | 3.199 ± 0.756 | 12.274 ± 0.987 | 0.309 ± 0.092 | 28.80 ± 5.93 | 22.57 ± 1.61 | 24.43 ± 1.30 |
| 20 | 11.115 ± 4.582 | 28.745 ± 1.782 | 0.485 ± 0.034 | 109.77 ± 13.01 | 63.37 ± 2.51 | 64.10 ± 2.01 |
| 30 | 21.403 ± 2.760 | 44.622 ± 2.018 | 0.711 ± 0.068 | 238.27 ± 26.97 | 111.83 ± 2.59 | 110.20 ± 2.48 |
| 50 | 62.943 ± 6.790 | 80.725 ± 3.415 | 1.337 ± 0.170 | 669.40 ± 67.12 | 221.27 ± 4.71 | 219.37 ± 2.94 |
| 75 | 135.716 ± 11.063 | 125.403 ± 3.127 | 2.263 ± 0.471 | 1471.07 ± 105.45 | 376.20 ± 5.39 | 372.87 ± 3.09 |
| 100 | 273.005 ± 86.612 | 190.926 ± 28.413 | 3.424 ± 1.280 | 2567.50 ± 170.66 | 540.30 ± 4.76 | 535.97 ± 4.99 |
| 200 | 991.489 ± 86.091 | 423.465 ± 41.286 | 12.001 ± 3.150 | 10149.33 ± 560.92 | 1282.43 ± 7.81 | 1271.63 ± 6.68 |
| 500 | 6393.415 ± 269.107 | 1181.395 ± 69.842 | 42.848 ± 7.604 | 62978.50 ± 1918.88 | 3855.57 ± 13.55 | 3834.13 ± 9.94 |
| 1000 | 27144.611 ± 1288.801 | 2596.707 ± 183.371 | 101.401 ± 12.956 | 250788.80 ± 3952.66 | 8703.60 ± 17.45 | 8656.37 ± 13.41 |

## 4. Gráficos

![Tempo de execução](grafico_tempos.png)

![Número de comparações](grafico_comparacoes.png)

O painel da esquerda usa escalas logarítmicas para mostrar todos os tamanhos e curvas.
O painel da direita usa escalas lineares e destaca as listas pequenas.
As linhas ligam os pontos medidos e não representam medições dos valores intermediários.
A linha n log₂ n é uma referência de crescimento, não um mínimo exato por entrada.

## 5. Em qual n o Merge passa a ser mais rápido?

O primeiro tamanho testado com média menor para o Merge Sort foi **n = 75**. A mudança observada está entre os pontos amostrados n = 50 e n = 75. Os inteiros intermediários não foram medidos; não é possível apontar uma fronteira exata nesse intervalo. A vantagem continuou nos demais tamanhos amostrados.

Esse é o valor observado entre os tamanhos exigidos pelo enunciado. Um limiar exato e universal
não pode ser obtido com essa amostragem: o hardware, a execução e o código influenciam os tempos.
Para investigar o intervalo, seria necessário medir também seus valores intermediários e repetir
o experimento. Diferenças pequenas devem ser avaliadas junto com a dispersão; não foi realizado
um teste de significância estatística.

## 6. Os gráficos apresentam a mesma virada?

O primeiro tamanho testado com média menor para o Merge Sort foi **n = 5**. Ele já teve vantagem no menor tamanho da amostra; uma virada anterior não foi observada. A vantagem continuou nos demais tamanhos amostrados.

Nesta execução, os pontos não coincidiram: **tempo em n = 75** e **comparações em n = 5**.

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
