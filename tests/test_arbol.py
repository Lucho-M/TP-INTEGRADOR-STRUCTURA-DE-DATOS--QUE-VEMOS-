import unittest

from estructuras.arbol import ArbolBST, normalizar_titulo
from modelos.pelicula import Pelicula


def _pelicula(titulo, puntaje=8.0):
    return Pelicula(
        titulo=titulo, anio=2000, genero="Drama", subgenero="",
        director="Director", actores=[], puntaje=puntaje,
        duracion=100, plataformas=["Netflix"], fecha_retiro="",
    )


class TestNormalizarTitulo(unittest.TestCase):
    def test_quita_mayusculas_y_tildes(self):
        self.assertEqual(normalizar_titulo("Interestelar"), "interestelar")
        self.assertEqual(normalizar_titulo("  El Señor de los Anillos  "), "el senor de los anillos")


class TestArbolBST(unittest.TestCase):
    def setUp(self):
        self.arbol = ArbolBST()
        for titulo in ["Matrix", "Interestelar", "El Origen", "Alien", "Zodiaco"]:
            self.arbol.insertar(_pelicula(titulo))

    def test_buscar_encuentra_titulo_exacto_case_insensitive(self):
        resultado = self.arbol.buscar("MATRIX")
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].titulo, "Matrix")

    def test_buscar_sin_coincidencia_devuelve_lista_vacia(self):
        self.assertEqual(self.arbol.buscar("No existe"), [])

    def test_insertar_titulo_repetido_lo_agrega_al_mismo_nodo(self):
        self.arbol.insertar(_pelicula("Matrix", puntaje=5.0))  # remake ficticio
        resultado = self.arbol.buscar("matrix")
        self.assertEqual(len(resultado), 2)

    def test_recorrido_inorder_devuelve_orden_alfabetico(self):
        titulos = [p.titulo for p in self.arbol.recorrido_inorder()]
        self.assertEqual(titulos, sorted(titulos, key=normalizar_titulo))

    def test_recorrido_preorder_empieza_por_la_raiz(self):
        preorder = self.arbol.recorrido_preorder()
        self.assertEqual(preorder[0].titulo, self.arbol.raiz.peliculas[0].titulo)

    def test_recorrido_postorder_termina_en_la_raiz(self):
        postorder = self.arbol.recorrido_postorder()
        self.assertEqual(postorder[-1].titulo, self.arbol.raiz.peliculas[0].titulo)

    def test_arbol_vacio_no_rompe_los_recorridos(self):
        vacio = ArbolBST()
        self.assertEqual(vacio.recorrido_inorder(), [])
        self.assertEqual(vacio.buscar("algo"), [])
        self.assertEqual(vacio.altura(), 0)


if __name__ == "__main__":
    unittest.main()
