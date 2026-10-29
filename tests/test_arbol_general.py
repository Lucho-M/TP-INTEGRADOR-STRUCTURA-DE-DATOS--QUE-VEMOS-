import unittest

from estructuras.arbol_general import ArbolCategorias
from modelos.pelicula import Pelicula


def _pelicula(titulo, genero, subgenero=""):
    return Pelicula(
        titulo=titulo, anio=2000, genero=genero, subgenero=subgenero,
        director="Director", actores=[], puntaje=8.0,
        duracion=100, plataformas=["Netflix"], fecha_retiro="",
    )


class TestArbolCategorias(unittest.TestCase):
    def setUp(self):
        self.arbol = ArbolCategorias()
        self.arbol.insertar(_pelicula("El Hombre Arana", "Accion", "Superheroes"))
        self.arbol.insertar(_pelicula("Los Increibles", "Animacion", "Superheroes"))
        self.arbol.insertar(_pelicula("Matrix", "Ciencia ficcion", "Ciberpunk"))
        self.arbol.insertar(_pelicula("Interestelar", "Ciencia ficcion", "Espacial"))
        self.arbol.insertar(_pelicula("Gladiador", "Accion", "Epica"))

    def test_generos_de_primer_nivel(self):
        self.assertEqual(set(self.arbol.generos()), {"Accion", "Animacion", "Ciencia ficcion"})

    def test_subgeneros_de_un_genero(self):
        self.assertEqual(set(self.arbol.subgeneros("Accion")), {"Superheroes", "Epica"})

    def test_subgenero_mismo_nombre_bajo_generos_distintos_no_se_mezcla(self):
        # "Superheroes" existe bajo Accion y bajo Animacion: son nodos distintos,
        # cada uno con SU propia película, no deberían pisarse ni mezclarse.
        accion = self.arbol.peliculas_de_subgenero("Accion", "Superheroes")
        animacion = self.arbol.peliculas_de_subgenero("Animacion", "Superheroes")
        self.assertEqual([p.titulo for p in accion], ["El Hombre Arana"])
        self.assertEqual([p.titulo for p in animacion], ["Los Increibles"])

    def test_peliculas_de_genero_recorre_todos_los_subgeneros(self):
        resultado = self.arbol.peliculas_de_genero("Accion")
        titulos = {p.titulo for p in resultado}
        self.assertEqual(titulos, {"El Hombre Arana", "Gladiador"})

    def test_genero_inexistente_devuelve_vacio(self):
        self.assertEqual(self.arbol.subgeneros("No existe"), [])
        self.assertEqual(self.arbol.peliculas_de_genero("No existe"), [])

    def test_subgenero_inexistente_devuelve_vacio(self):
        self.assertEqual(self.arbol.peliculas_de_subgenero("Accion", "No existe"), [])

    def test_pelicula_sin_subgenero_queda_en_el_nodo_genero(self):
        self.arbol.insertar(_pelicula("Pelicula Suelta", "Drama", ""))
        self.assertEqual(self.arbol.subgeneros("Drama"), [])
        resultado = self.arbol.peliculas_de_genero("Drama")
        self.assertEqual([p.titulo for p in resultado], ["Pelicula Suelta"])

    def test_recorrido_preorder_visita_raiz_generos_y_subgeneros(self):
        nombres = [nodo.nombre for nodo in self.arbol.recorrido_preorder()]
        self.assertEqual(nombres[0], "Catalogo")
        self.assertIn("Accion", nombres)
        self.assertIn("Superheroes", nombres)

    def test_altura_con_subgeneros_es_tres(self):
        # Catalogo (nivel 1) -> Genero (nivel 2) -> Subgenero (nivel 3)
        self.assertEqual(self.arbol.altura(), 3)

    def test_arbol_vacio(self):
        vacio = ArbolCategorias()
        self.assertEqual(vacio.generos(), [])
        self.assertEqual(vacio.altura(), 1)


if __name__ == "__main__":
    unittest.main()
