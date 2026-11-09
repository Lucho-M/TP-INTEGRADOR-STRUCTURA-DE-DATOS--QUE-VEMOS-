import random
import unittest

from estructuras.heap import Heap
from modelos.pelicula import Pelicula
from servicios.catalogo import prioridad_ranking, prioridad_retiro


def _pelicula(titulo, puntaje=8.0, fecha_retiro=""):
    return Pelicula(
        titulo=titulo, anio=2000, genero="Drama", subgenero="",
        director="Director", actores=[], puntaje=puntaje,
        duracion=100, plataformas=["Netflix"], fecha_retiro=fecha_retiro,
    )


def _vaciar(heap):
    resultado = []
    while heap:
        resultado.append(heap.extraer())
    return resultado


class TestHeap(unittest.TestCase):
    def test_heap_vacio(self):
        heap = Heap(lambda x: x)
        self.assertEqual(len(heap), 0)
        self.assertIsNone(heap.ver_tope())
        self.assertIsNone(heap.extraer())

    def test_un_elemento(self):
        heap = Heap(lambda x: x)
        heap.insertar(7)
        self.assertEqual(heap.ver_tope(), 7)
        self.assertEqual(heap.extraer(), 7)
        self.assertEqual(len(heap), 0)

    def test_ver_tope_no_saca_el_elemento(self):
        heap = Heap(lambda x: x, [5, 1, 3])
        self.assertEqual(heap.ver_tope(), 1)
        self.assertEqual(len(heap), 3)

    def test_insertar_de_a_uno_extrae_en_orden(self):
        heap = Heap(lambda x: x)
        for valor in [5, 3, 8, 1, 9, 2]:
            heap.insertar(valor)
        self.assertEqual(_vaciar(heap), [1, 2, 3, 5, 8, 9])

    def test_construir_desde_lista_extrae_en_orden(self):
        valores = list(range(200))
        random.Random(271).shuffle(valores)
        self.assertEqual(_vaciar(Heap(lambda x: x, valores)), sorted(valores))

    def test_no_modifica_la_lista_original(self):
        original = [3, 1, 2]
        _vaciar(Heap(lambda x: x, original))
        self.assertEqual(original, [3, 1, 2])

    def test_valores_repetidos(self):
        self.assertEqual(_vaciar(Heap(lambda x: x, [2, 1, 2, 1, 2])), [1, 1, 2, 2, 2])

    def test_prioridad_negada_funciona_como_max_heap(self):
        self.assertEqual(_vaciar(Heap(lambda x: -x, [4, 9, 1, 7])), [9, 7, 4, 1])

    def test_prioridad_ranking_mayor_puntaje_primero_y_desempata_por_titulo(self):
        peliculas = [_pelicula("Zodiaco", 8.8), _pelicula("Matrix", 8.7), _pelicula("El Origen", 8.8)]
        titulos = [p.titulo for p in _vaciar(Heap(prioridad_ranking, peliculas))]
        self.assertEqual(titulos, ["El Origen", "Zodiaco", "Matrix"])

    def test_prioridad_retiro_fecha_mas_cercana_primero(self):
        peliculas = [
            _pelicula("A", fecha_retiro="2026-12-01"),
            _pelicula("B", fecha_retiro="2026-10-15"),
            _pelicula("C", fecha_retiro="2027-01-20"),
        ]
        titulos = [p.titulo for p in _vaciar(Heap(prioridad_retiro, peliculas))]
        self.assertEqual(titulos, ["B", "A", "C"])


if __name__ == "__main__":
    unittest.main()
