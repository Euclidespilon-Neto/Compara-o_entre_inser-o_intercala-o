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


def merge_sort(lista):
    """Divide a entrada e intercala as metades, somando suas comparações."""
    if len(lista) <= 1:
        return list(lista), 0

    meio = len(lista) // 2
    esquerda, cont_esquerda = merge_sort(lista[:meio])
    direita, cont_direita = merge_sort(lista[meio:])
    resultado = []
    i = j = 0
    comparacoes = cont_esquerda + cont_direita

    while i < len(esquerda) and j < len(direita):
        comparacoes += 1
        if direita[j] < esquerda[i]:
            resultado.append(direita[j])
            j += 1
        else:
            # Em um empate, mantém primeiro o elemento da metade esquerda.
            resultado.append(esquerda[i])
            i += 1

    # Sobras já estão ordenadas; copiá-las não compara valores.
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado, comparacoes
