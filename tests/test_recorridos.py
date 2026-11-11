import unittest

from algoritmos.recorridos import bfs, dfs, reconstruir_camino
from estructuras.grafo import Grafo


def _orden_alfabetico(vertice):
    return vertice


class TestRecorridos(unittest.TestCase):
    """Grafo de prueba (todas las aristas peso 1, salvo A-E):

        A - B - D - F
        |   |
        C --+       E (A-E peso 3)      G (aislado)
    """

    def setUp(self):
        self.grafo = Grafo()
        self.grafo.agregar_arista("A", "B", 1)
        self.grafo.agregar_arista("A", "C", 1)
        self.grafo.agregar_arista("B", "C", 1)
        self.grafo.agregar_arista("B", "D", 1)
        self.grafo.agregar_arista("D", "F", 1)
        self.grafo.agregar_arista("A", "E", 3)
        self.grafo.agregar_vertice("G")

    def test_bfs_visita_por_niveles(self):
        visitados = bfs(self.grafo, "A", orden=_orden_alfabetico)
        self.assertEqual(list(visitados), ["A", "B", "C", "E", "D", "F"])
        self.assertEqual({v: visita.nivel for v, visita in visitados.items()},
                         {"A": 0, "B": 1, "C": 1, "E": 1, "D": 2, "F": 3})

    def test_dfs_va_hasta_el_fondo_antes_de_volver(self):
        visitados = dfs(self.grafo, "A", orden=_orden_alfabetico)
        self.assertEqual(list(visitados), ["A", "B", "C", "D", "F", "E"])

    def test_dfs_profundidad_es_la_del_arbol_dfs(self):
        visitados = dfs(self.grafo, "A", orden=_orden_alfabetico)
        self.assertEqual(visitados["C"].nivel, 2)   # A -> B -> C (BFS lo encuentra en 1)
        self.assertEqual(visitados["C"].padre, "B")

    def test_los_dos_visitan_toda_la_componente_y_no_el_aislado(self):
        esperados = {"A", "B", "C", "D", "E", "F"}
        self.assertEqual(set(bfs(self.grafo, "A")), esperados)
        self.assertEqual(set(dfs(self.grafo, "A")), esperados)

    def test_vertice_aislado_solo_se_visita_a_si_mismo(self):
        self.assertEqual(list(bfs(self.grafo, "G")), ["G"])
        self.assertEqual(list(dfs(self.grafo, "G")), ["G"])

    def test_origen_inexistente_devuelve_vacio(self):
        self.assertEqual(bfs(self.grafo, "Z"), {})
        self.assertEqual(dfs(self.grafo, "Z"), {})

    def test_camino_bfs_es_el_de_menos_aristas(self):
        camino = reconstruir_camino(bfs(self.grafo, "A", "F", orden=_orden_alfabetico), "F")
        self.assertEqual([v for v, _ in camino], ["A", "B", "D", "F"])
        self.assertIsNone(camino[0][1])
        self.assertEqual(camino[1][1].destino, "B")

    def test_camino_dfs_puede_ser_mas_largo_que_el_de_bfs(self):
        camino_bfs = reconstruir_camino(bfs(self.grafo, "A", orden=_orden_alfabetico), "C")
        camino_dfs = reconstruir_camino(dfs(self.grafo, "A", orden=_orden_alfabetico), "C")
        self.assertEqual(len(camino_bfs), 2)   # A -> C
        self.assertEqual(len(camino_dfs), 3)   # A -> B -> C

    def test_camino_a_vertice_no_alcanzado_es_none(self):
        self.assertIsNone(reconstruir_camino(bfs(self.grafo, "A"), "G"))

    def test_camino_de_un_vertice_a_si_mismo(self):
        camino = reconstruir_camino(bfs(self.grafo, "A", "A"), "A")
        self.assertEqual([v for v, _ in camino], ["A"])

    def test_bfs_corta_al_encontrar_el_destino(self):
        visitados = bfs(self.grafo, "A", "B", orden=_orden_alfabetico)
        self.assertNotIn("F", visitados)

    def test_filtro_permitidos(self):
        # Sin pasar por B, D y F quedan inalcanzables.
        visitados = bfs(self.grafo, "A", permitidos={"A", "C", "D", "E", "F"})
        self.assertEqual(set(visitados), {"A", "C", "E"})
        self.assertEqual(set(dfs(self.grafo, "A", permitidos={"A", "C", "D", "E", "F"})), {"A", "C", "E"})

    def test_filtro_peso_maximo(self):
        self.assertNotIn("E", bfs(self.grafo, "A", peso_maximo=2))
        self.assertNotIn("E", dfs(self.grafo, "A", peso_maximo=2))

    def test_dfs_iterativo_no_choca_con_el_limite_de_recursion(self):
        grafo = Grafo()
        for i in range(5_000):  # cadena de 5.000 vértices: profundidad 4.999
            grafo.agregar_arista(i, i + 1, 1)
        visitados = dfs(grafo, 0)
        self.assertEqual(len(visitados), 5_001)
        self.assertEqual(visitados[5_000].nivel, 5_000)


if __name__ == "__main__":
    unittest.main()
