# Ordenação: Insertion Sort, Merge Sort e sorted()

Trabalho de Estrutura de Dados Avançados de **Euclides Carlos Pilon Neto** e
**Gabriela de Araújo Reis**. Inclui o desafio extra de contar as comparações de `sorted()`.

## Preparar o ambiente

Requisitos: Python 3.10 ou superior e pip. Verifique com `python --version`.
No Windows, se o comando disponível for `py`, substitua `python` por `py`.
Abra o terminal na raiz do repositório, onde está `ordenacao.py`.

```powershell
python -m pip install -r requirements.txt
python -m unittest testes.py -v
python medir.py
```

Não é necessário abrir uma janela gráfica: o Matplotlib usa o modo `Agg`.
Os arquivos gerados ficam ao lado de `medir.py`, mesmo se o comando for chamado a partir de outra pasta.

Opcionalmente, crie um ambiente virtual antes de instalar as dependências:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m unittest testes.py -v
.venv\Scripts\python.exe medir.py
```

No Linux/macOS, use `.venv/bin/python` no lugar de `.venv\Scripts\python.exe`.
Essa forma não depende da ativação do ambiente no PowerShell.

## O que cada arquivo faz

| Arquivo | Responsabilidade |
|---|---|
| `ordenacao.py` | Implementa as duas ordenações e seus contadores. |
| `testes.py` | Testa resultados, casos críticos, contagem, estabilidade e preservação da entrada. |
| `medir.py` | Executa experimentos, agrega dados, gera CSV e gráficos e chama o gerador de relatório. |
| `relatorio.py` | Produz a tabela e as respostas do relatório usando os resultados reais. |
| `dados.csv` | Guarda dados brutos e estatísticas. |
| `ambiente.json` | Registra data, Python, sistema, dependências e parâmetros. |
| `grafico_tempos.png` | Compara o tempo dos três algoritmos. |
| `grafico_comparacoes.png` | Compara as contagens e inclui a referência n log₂ n. |
| `RELATORIO.md` | Apresenta método, tabela, gráficos, respostas e limitações. |
| `requirements.txt` | Declara a dependência de gráficos. |

## Como funciona a medição

São usados n = 5, 10, 20, 30, 50, 75, 100, 200, 500 e 1000, com 30 entradas
aleatórias por tamanho. Cada entrada é uma permutação de `range(n)`; os três algoritmos
recebem o mesmo conteúdo. As funções próprias retornam uma nova lista e não modificam a entrada.

Cada medição cronometra um lote de chamadas e divide a duração pelo tamanho do lote:
50 chamadas até n = 100 e cinco acima disso. As 30 repetições usam entradas diferentes;
as chamadas de um mesmo lote repetem a mesma entrada. O cronômetro é `perf_counter_ns()`.
A geração e a validação ficam fora do cronômetro. A cópia e os contadores internos
de Insertion/Merge fazem parte do tempo. `sorted()` é cronometrado com inteiros.

As comparações de `sorted()` são contadas em outra execução com `ElementoContador`.
Somente comparações entre valores entram na contagem. Testes de índices e laços não entram.

```powershell
python medir.py --repeticoes 50 --semente 123
```

O programa rejeita menos de dez repetições. A semente reproduz as entradas; os tempos
podem mudar por causa do computador e de processos concorrentes.
As contagens do `sorted()` também podem depender da versão da implementação do Python.

## Ler os resultados

Abra `RELATORIO.md` no GitHub ou na prévia Markdown do VS Code. Os gráficos precisam
estar na mesma pasta. A tabela usa microssegundos; o CSV e o gráfico usam segundos.
O primeiro n favorável ao Merge é o primeiro **entre os tamanhos medidos**.
Não deve ser interpretado como fronteira universal ou como medição de inteiros intermediários.

No CSV, `tipo=bruto` identifica uma entrada/repetição; `tipo=media` identifica a média
de um algoritmo para um tamanho. `comparacoes` é uma contagem exata inteira nas linhas
brutas e uma média nas linhas de resumo. Os desvios são amostrais. O arquivo usa vírgula
como separador e ponto decimal; ao importar no Excel, escolha essas opções.

## Regenerar e entregar

`python medir.py` substitui `dados.csv`, `ambiente.json`, os dois PNGs e `RELATORIO.md`.
Para manter uma alteração no texto do relatório, edite `relatorio.py` antes de executar.
Os resultados incluídos no pacote foram produzidos no ambiente descrito em `ambiente.json`;
a dupla deve executar novamente no computador usado para a entrega e revisar as conclusões.

Depois de rodar os testes e o experimento, confira o diff e inclua os arquivos gerados
no commit. O histórico da dupla será construído com os commits feitos por cada integrante;
este pacote não contém commits nem simula a autoria de nenhum dos dois.
