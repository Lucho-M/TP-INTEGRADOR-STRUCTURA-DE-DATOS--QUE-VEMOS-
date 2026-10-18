import unittest

from estructuras.arbol import ArbolBST
from estructuras.avl import ArbolAVL
from modelos.pelicula import Pelicula


def _pelicula(titulo, puntaje=8.0):
    return Pelicula(
        titulo=titulo, anio=2000, genero="Drama", subgenero="",
        director="Director", actores=[], puntaje=puntaje,
        duracion=100, plataformas=["Netflix"], fecha_retiro="",
    )


class TestArbolAVLBasico(unittest.TestCase):
    """Mismo comportamiento funcional que ArbolBST (TP3): buscar, recorridos, remakes."""

    def setUp(self):
        self.arbol = ArbolAVL()
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
        from estructuras.arbol import normalizar_titulo
        titulos = [p.titulo for p in self.arbol.recorrido_inorder()]
        self.assertEqual(titulos, sorted(titulos, key=normalizar_titulo))

    def test_arbol_vacio_no_rompe_nada(self):
        vacio = ArbolAVL()
        self.assertEqual(vacio.recorrido_inorder(), [])
        self.assertEqual(vacio.buscar("algo"), [])
        self.assertEqual(vacio.altura(), 0)


class TestRotaciones(unittest.TestCase):
    """Casos mínimos y conocidos de cada rotación, para verificar que reacomodan bien el árbol."""

    def test_rotacion_simple_izquierda_caso_derecha_derecha(self):
        # Insertar en orden creciente (a, b, c) desbalancea a la derecha:
        # la raíz pasa a ser "b", con "a" a la izquierda y "c" a la derecha.
        arbol = ArbolAVL()
        for titulo in ["a", "b", "c"]:
            arbol.insertar(_pelicula(titulo))
        self.assertEqual(arbol.raiz.clave, "b")
        self.assertEqual(arbol.raiz.izq.clave, "a")
        self.assertEqual(arbol.raiz.der.clave, "c")
        self.assertEqual(arbol.altura(), 2)

    def test_rotacion_simple_derecha_caso_izquierda_izquierda(self):
        # Espejo del anterior: orden decreciente (c, b, a).
        arbol = ArbolAVL()
        for titulo in ["c", "b", "a"]:
            arbol.insertar(_pelicula(titulo))
        self.assertEqual(arbol.raiz.clave, "b")
        self.assertEqual(arbol.raiz.izq.clave, "a")
        self.assertEqual(arbol.raiz.der.clave, "c")
        self.assertEqual(arbol.altura(), 2)

    def test_rotacion_doble_derecha_izquierda(self):
        # a, c, b: el subárbol derecho ("c") queda pesado, y "b" entra como
        # hijo IZQUIERDO de ese subárbol derecho -> caso doble Derecha-Izquierda.
        arbol = ArbolAVL()
        for titulo in ["a", "c", "b"]:
            arbol.insertar(_pelicula(titulo))
        self.assertEqual(arbol.raiz.clave, "b")
        self.assertEqual(arbol.raiz.izq.clave, "a")
        self.assertEqual(arbol.raiz.der.clave, "c")

    def test_rotacion_doble_izquierda_derecha(self):
        # c, a, b: el subárbol izquierdo ("a") queda pesado, y "b" entra como
        # hijo DERECHO de ese subárbol izquierdo -> caso doble Izquierda-Derecha.
        arbol = ArbolAVL()
        for titulo in ["c", "a", "b"]:
            arbol.insertar(_pelicula(titulo))
        self.assertEqual(arbol.raiz.clave, "b")
        self.assertEqual(arbol.raiz.izq.clave, "a")
        self.assertEqual(arbol.raiz.der.clave, "c")


class TestComparacionConBSTDesbalanceado(unittest.TestCase):
    """El caso que motiva todo el TP4: insertar datos ya ordenados degenera el BST, no al AVL."""

    def test_insercion_ordenada_degenera_bst_pero_no_avl(self):
        titulos = [chr(ord("a") + i) for i in range(20)]  # "a".."t", ya ordenados

        bst = ArbolBST()
        avl = ArbolAVL()
        for titulo in titulos:
            bst.insertar(_pelicula(titulo))
            avl.insertar(_pelicula(titulo))

        # El BST común degenera en algo parecido a una lista: altura == cantidad de nodos.
        self.assertEqual(bst.altura(), len(titulos))

        # El AVL se mantiene cerca de log2(n): con 20 nodos, nunca más de 6 niveles.
        self.assertLessEqual(avl.altura(), 6)
        self.assertLess(avl.altura(), bst.altura())


if __name__ == "__main__":
    unittest.main()
