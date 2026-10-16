"""Testes de resultado, contagem, estabilidade e preservação da entrada."""

import itertools
import random
import unittest

from ordenacao import insertion_sort, merge_sort

ALGORITMOS = (insertion_sort, merge_sort)


class Registro:
    """Compara só a chave; a etiqueta revela a ordem dos empates."""

    chamadas = 0

    def __init__(self, chave, etiqueta):
        self.chave = chave
        self.etiqueta = etiqueta

    def __lt__(self, outro):
        Registro.chamadas += 1
        return self.chave < outro.chave


class TestOrdenacao(unittest.TestCase):
    def verificar(self, entrada):
        for algoritmo in ALGORITMOS:
            with self.subTest(algoritmo=algoritmo.__name__, entrada=entrada):
                original = entrada.copy()
                resultado, comparacoes = algoritmo(entrada)
                self.assertEqual(resultado, sorted(original))
                self.assertEqual(entrada, original)
                self.assertIsNot(resultado, entrada)
                self.assertIsInstance(comparacoes, int)
                self.assertGreaterEqual(comparacoes, 0)

    def test_lista_vazia(self):
        self.verificar([])

    def test_elemento_unico(self):
        self.verificar([42])

    def test_elementos_iguais(self):
        self.verificar([7, 7, 7, 7])

    def test_lista_ordenada(self):
        self.verificar([1, 2, 3, 4, 5])

    def test_lista_invertida(self):
        self.verificar([5, 4, 3, 2, 1])

    def test_lista_aleatoria(self):
        self.verificar([8, 3, 9, 1, 6, 2, 7, 4, 5])

    def test_negativos_e_repetidos(self):
        self.verificar([0, -4, 3, -4, 2, 0, -1])

    def test_permutacoes_ate_seis(self):
        for n in range(7):
            for permutacao in itertools.permutations(range(n)):
                self.verificar(list(permutacao))

    def test_aleatorias_com_repeticoes(self):
        gerador = random.Random(123)
        for n in (2, 3, 17, 50, 100, 1000):
            self.verificar([gerador.randrange(-20, 21) for _ in range(n)])

    def test_contagens_triviais(self):
        for algoritmo in ALGORITMOS:
            for entrada in ([], [42]):
                with self.subTest(algoritmo=algoritmo.__name__, entrada=entrada):
                    self.assertEqual(algoritmo(entrada)[1], 0)

    def test_contagem_insertion_melhor_caso(self):
        for n in (1, 2, 5, 20):
            self.assertEqual(insertion_sort(list(range(n)))[1], n - 1)
            self.assertEqual(insertion_sort([7] * n)[1], n - 1)

    def test_contagem_insertion_pior_caso(self):
        for n in (0, 1, 2, 5, 20):
            self.assertEqual(insertion_sort(list(range(n, 0, -1)))[1], n * (n - 1) // 2)

    def test_contagens_manuais(self):
        # [3, 1, 2]: insertion faz 3; merge faz 1 + 2 = 3 comparações.
        for algoritmo in ALGORITMOS:
            self.assertEqual(algoritmo([3, 1, 2])[1], 3)

    def test_contagem_confere_com_operacoes_reais(self):
        for algoritmo in ALGORITMOS:
            for entrada in ([3, 1, 2], [2, 2, 1, 4, 1], list(range(9))):
                with self.subTest(algoritmo=algoritmo.__name__, entrada=entrada):
                    objetos = [Registro(valor, i) for i, valor in enumerate(entrada)]
                    Registro.chamadas = 0
                    resultado, contagem = algoritmo(objetos)
                    self.assertEqual(contagem, Registro.chamadas)
                    self.assertEqual([r.chave for r in resultado], sorted(entrada))

    def test_estabilidade(self):
        for algoritmo in ALGORITMOS:
            entrada = [Registro(2, 'a'), Registro(1, 'b'), Registro(2, 'c'), Registro(1, 'd')]
            resultado, _ = algoritmo(entrada)
            self.assertEqual([r.etiqueta for r in resultado], ['b', 'd', 'a', 'c'])


class TestSortedContador(unittest.TestCase):
    def test_contagens_conhecidas(self):
        from medir import contar_sorted
        for entrada, esperado in (([], 0), ([1], 0), ([1, 2, 3, 4], 3)):
            self.assertEqual(contar_sorted(entrada), esperado)

    def test_contador_reiniciado(self):
        from medir import contar_sorted
        primeira = contar_sorted([3, 1, 2, 5, 4])
        self.assertEqual(contar_sorted([3, 1, 2, 5, 4]), primeira)
        self.assertEqual(contar_sorted([]), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
