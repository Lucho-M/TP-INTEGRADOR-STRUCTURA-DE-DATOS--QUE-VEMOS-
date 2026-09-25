import unittest

from servicios.catalogo import Catalogo


class TestCatalogo(unittest.TestCase):
    def setUp(self):
        self.catalogo = Catalogo()
        self.catalogo.cargar_desde_csv("datos/peliculas.csv")

    def test_carga_peliculas(self):
        self.assertEqual(len(self.catalogo), 32)

    def test_buscar_encuentra_por_coincidencia_parcial_case_insensitive(self):
        resultados = self.catalogo.buscar("matrix")
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0].titulo, "Matrix")

    def test_buscar_sin_coincidencias_devuelve_lista_vacia(self):
        resultados = self.catalogo.buscar("pelicula que no existe")
        self.assertEqual(resultados, [])

    def test_listar_devuelve_todas_las_peliculas(self):
        self.assertEqual(len(self.catalogo.listar()), len(self.catalogo))

    def test_filtrar_por_genero(self):
        resultados = self.catalogo.filtrar_por_genero("Ciencia ficcion")
        self.assertTrue(len(resultados) > 0)
        for pelicula in resultados:
            self.assertEqual(pelicula.genero.lower(), "ciencia ficcion")

    def test_filtrar_por_plataforma(self):
        resultados = self.catalogo.filtrar_por_plataforma("Netflix")
        self.assertTrue(len(resultados) > 0)
        for pelicula in resultados:
            self.assertIn("Netflix", pelicula.plataformas)

    def test_buscar_binaria_encuentra_titulo_exacto_case_insensitive(self):
        resultado = self.catalogo.buscar_binaria("MATRIX")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.titulo, "Matrix")

    def test_buscar_binaria_sin_coincidencia_devuelve_none(self):
        self.assertIsNone(self.catalogo.buscar_binaria("pelicula que no existe"))


if __name__ == "__main__":
    unittest.main()
