"""Ordenações estáveis: devolvem (nova_lista, comparacoes_entre_valores)."""


def insertion_sort(lista):
    """Insere cada elemento na parte já ordenada, sem alterar a entrada."""
    resultado = list(lista)
    comparacoes = 0
    for i in range(1, len(resultado)):
        chave = resultado[i]
        j = i - 1
        while j >= 0:
            # Conta inclusive a comparação falsa que encerra a busca.
            comparacoes += 1
            if not chave < resultado[j]:
                break
            resultado[j + 1] = resultado[j]
            j -= 1
        resultado[j + 1] = chave
    return resultado, comparacoes
