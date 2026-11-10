import unittest

from estructuras.grafo import Grafo
from modelos.pelicula import Pelicula
from servicios.red_peliculas import COSTO_VINCULO, construir_grafo


def _pelicula(titulo, genero="Drama", director="Director X", actores=None):
    return Pelicula(
        titulo=titulo, anio=2000, genero=genero, subgenero="",
        director=director, actores=actores or [], puntaje=8.0,
        duracion=100, plataformas=["Netflix"], fecha_retiro="",
    )


class TestGrafo(unittest.TestCase):
    def setUp(self):
        self.grafo = Grafo()
        self.grafo.agregar_arista("A", "B", 1)
        self.grafo.agregar_arista("A", "C", 3)
        self.grafo.agregar_vertice("D")  # aislado

    def test_grafo_vacio(self):
        grafo = Grafo()
        self.assertEqual(len(grafo), 0)
        self.assertEqual(grafo.cantidad_aristas(), 0)
        self.assertEqual(grafo.densidad(), 0.0)

    def test_agregar_arista_crea_los_vertices(self):
        self.assertIn("A", self.grafo)
        self.assertIn("B", self.grafo)
        self.assertEqual(len(self.grafo), 4)

    def test_no_dirigido_la_arista_existe_en_los_dos_sentidos(self):
        self.assertEqual(self.grafo.arista("A", "B").peso, 1)
        self.assertEqual(self.grafo.arista("B", "A").peso, 1)

    def test_arista_inexistente_devuelve_none(self):
        self.assertIsNone(self.grafo.arista("B", "C"))
        self.assertIsNone(self.grafo.arista("A", "Z"))

    def test_vecinos_y_grado(self):
        self.assertEqual({a.destino for a in self.grafo.vecinos("A")}, {"B", "C"})
        self.assertEqual(self.grafo.grado("A"), 2)
        self.assertEqual(self.grafo.grado("D"), 0)
        self.assertEqual(self.grafo.vecinos("D"), [])

    def test_vecinos_de_vertice_inexistente_es_lista_vacia(self):
        self.assertEqual(self.grafo.vecinos("Z"), [])

    def test_cantidad_aristas_no_cuenta_doble(self):
        self.assertEqual(self.grafo.cantidad_aristas(), 2)

    def test_densidad(self):
        # 4 vértices -> 6 pares posibles; hay 2 aristas.
        self.assertAlmostEqual(self.grafo.densidad(), 2 / 6)

    def test_no_permite_lazos(self):
        self.grafo.agregar_arista("A", "A", 1)
        self.assertIsNone(self.grafo.arista("A", "A"))
        self.assertEqual(self.grafo.cantidad_aristas(), 2)


class TestConstruirGrafo(unittest.TestCase):
    def setUp(self):
        self.origen = _pelicula("El Origen", "Ciencia ficcion", "Christopher Nolan", ["Leonardo DiCaprio"])
        self.interestelar = _pelicula("Interestelar", "Ciencia ficcion", "Christopher Nolan", ["Matthew McConaughey"])
        self.titanic = _pelicula("Titanic", "Drama", "James Cameron", ["Leonardo DiCaprio"])
        self.matrix = _pelicula("Matrix", "Ciencia ficcion", "Lana Wachowski|Lilly Wachowski", ["Keanu Reeves"])
        self.coco = _pelicula("Coco", "Animacion", "Lee Unkrich", ["Gael Garcia Bernal"])
        self.grafo = construir_grafo([self.origen, self.interestelar, self.titanic, self.matrix, self.coco])

    def test_mismo_director_peso_1(self):
        self.assertEqual(self.grafo.arista(self.origen, self.interestelar).peso, COSTO_VINCULO["director"])

    def test_mismo_actor_peso_2(self):
        self.assertEqual(self.grafo.arista(self.origen, self.titanic).peso, COSTO_VINCULO["actor"])

    def test_mismo_genero_peso_3(self):
        self.assertEqual(self.grafo.arista(self.origen, self.matrix).peso, COSTO_VINCULO["genero"])

    def test_varios_vinculos_una_sola_arista_con_el_peso_del_mas_fuerte(self):
        arista = self.grafo.arista(self.origen, self.interestelar)
        self.assertEqual(arista.peso, 1)
        self.assertEqual(arista.vinculos, ["director: Christopher Nolan", "genero: Ciencia ficcion"])
        self.assertEqual(self.grafo.cantidad_aristas(), 4)

    def test_sin_nada_en_comun_no_hay_arista(self):
        self.assertIsNone(self.grafo.arista(self.titanic, self.matrix))

    def test_pelicula_sin_vinculos_queda_como_vertice_aislado(self):
        self.assertIn(self.coco, self.grafo)
        self.assertEqual(self.grafo.grado(self.coco), 0)

    def test_directores_multiples_se_separan(self):
        otra = _pelicula("Speed Racer", "Accion", "Lana Wachowski|Lilly Wachowski")
        grafo = construir_grafo([self.matrix, otra])
        self.assertEqual(grafo.arista(self.matrix, otra).vinculos,
                         ["director: Lana Wachowski", "director: Lilly Wachowski"])


if __name__ == "__main__":
    unittest.main()
