# Ordenação: Insertion Sort, Merge Sort e sorted()

Trabalho da disciplina de Estrutura de Dados Avançados desenvolvido por **Euclides Carlos Pilon Neto** e **Gabriela de Araújo Reis**, incluindo o desafio extra de contabilizar as comparações da função nativa `sorted()`.

## Preparar o ambiente

O projeto requer Python 3.10 ou superior e o gerenciador `pip` (verifique a versão instalada com `python --version`; no Windows, caso necessário, substitua `python` por `py`). Com o terminal aberto na raiz do repositório, onde fica o arquivo `ordenacao.py`, basta rodar os comandos abaixo para instalar as dependências, executar a bateria de testes e gerar as medições:

```powershell
python -m pip install -r requirements.txt
python -m unittest testes.py -v
python medir.py
```

Não é necessário abrir janela gráfica durante a execução, já que o Matplotlib está configurado no modo `Agg`, e todos os arquivos gerados são salvos diretamente na mesma pasta do `medir.py`.

Caso prefira isolar a instalação em um ambiente virtual antes de rodar o projeto:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m unittest testes.py -v
.venv\Scripts\python.exe medir.py
```

No Linux ou macOS, basta usar `.venv/bin/python` no lugar de `.venv\Scripts\python.exe`, o que permite rodar tudo direto sem depender da ativação do ambiente no terminal.

## O que cada arquivo faz

| Arquivo | Responsabilidade |
|---|---|
| `ordenacao.py` | Implementa os algoritmos de ordenação e seus contadores de comparações. |
| `testes.py` | Valida resultados, casos críticos, contagem, estabilidade e preservação da lista original. |
| `medir.py` | Executa os experimentos, agrega os dados, gera o CSV e os gráficos e aciona o relatório. |
| `relatorio.py` | Monta a tabela de resultados e preenche o relatório com base nos dados coletados. |
| `dados.csv` | Armazena tanto as medições brutas quanto as médias e desvios calculados. |
| `ambiente.json` | Registra a data de execução, versão do Python, sistema operacional e parâmetros usados. |
| `grafico_tempos.png` | Gráfico comparativo do tempo de execução dos três algoritmos. |
| `grafico_comparacoes.png` | Gráfico com a contagem de comparações junto à curva de referência n log₂ n. |
| `RELATORIO.md` | Documento final com a metodologia, tabelas, gráficos e análise dos resultados. |
| `requirements.txt` | Lista as bibliotecas necessárias para gerar os gráficos. |

## Como funciona a medição

Os testes foram configurados para os tamanhos `n = 5, 10, 20, 30, 50, 75, 100, 200, 500 e 1000`, rodando 30 entradas aleatórias para cada tamanho. Cada entrada é gerada como uma permutação de `range(n)` e repassada com exatamente o mesmo conteúdo para os três algoritmos, sendo que as funções implementadas sempre retornam uma nova lista sem alterar a entrada original.

Para evitar distorções em listas muito pequenas, a medição cronometra um lote de chamadas com `perf_counter_ns()` e divide o tempo total pelo tamanho do lote, usando 50 chamadas para `n` até 100 e 5 chamadas para valores maiores. As 30 repetições testam listas diferentes, enquanto as chamadas dentro de um mesmo lote repetem a mesma entrada. A criação das listas e a validação ficam de fora do cronômetro, mas a cópia dos dados e os contadores internos do Insertion Sort e do Merge Sort entram na conta.

No caso do `sorted()`, o tempo de execução é medido direto com números inteiros, enquanto a contagem de comparações é feita em uma execução separada usando a classe `ElementoContador`. Dessa forma, apenas as comparações diretas entre valores da lista são contabilizadas, deixando de fora verificações internas de índices e laços.

Caso queira rodar o experimento alterando a quantidade de repetições (mínimo de 10) ou fixando outra semente para reproduzir as entradas:

```powershell
python medir.py --repeticoes 50 --semente 123
```

Vale considerar que a semente garante a mesma sequência de listas geradas, mas os tempos de execução variam conforme o hardware e os processos abertos na máquina, assim como a contagem do `sorted()` pode ter pequenas variações dependendo da versão do Python.

## Leitura dos resultados

O arquivo `RELATORIO.md` pode ser visualizado diretamente no GitHub ou pela prévia de Markdown do VS Code, mantendo os arquivos PNG na mesma pasta. Na tabela do relatório os tempos são exibidos em microssegundos para facilitar a leitura, enquanto o CSV e os gráficos trabalham em segundos.

Nos resultados obtidos, o Merge Sort já leva vantagem no número de comparações desde `n = 5`, e passa a ser mais rápido em tempo de execução a partir de `n = 75`. Como a bateria padrão avalia saltos específicos de tamanho, esse ponto de virada representa o primeiro tamanho medido em que o Merge Sort supera o Insertion Sort (já que os valores inteiros intermediários entre 50 e 75 não fazem parte da grade padrão de testes).

Dentro do `dados.csv`, as linhas com `tipo=bruto` representam cada execução individual, onde a coluna `comparacoes` traz um valor inteiro exato, enquanto as linhas com `tipo=media` trazem o resumo de cada tamanho com a média e o desvio padrão amostral. O arquivo utiliza vírgula como separador de colunas e ponto para casas decimais.

## Reprodução dos dados e histórico

Ao executar `python medir.py`, o script atualiza automaticamente os arquivos `dados.csv`, `ambiente.json`, os dois gráficos em PNG e o `RELATORIO.md`. Por isso, qualquer ajuste no texto base do relatório é feito diretamente no arquivo `relatorio.py` antes de rodar o medidor.

Os dados e conclusões presentes neste repositório foram gerados nas execuções realizadas pela dupla, cujas especificações de máquina e sistema estão registradas no arquivo `ambiente.json`, e todo o histórico de desenvolvimento e autoria está registrado nos commits feitos por cada integrante no repositório.