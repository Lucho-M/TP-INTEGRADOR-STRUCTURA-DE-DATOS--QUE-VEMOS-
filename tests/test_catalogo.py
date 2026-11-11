import unittest
from datetime import date

from servicios.catalogo import Catalogo


class TestCatalogo(unittest.TestCase):
    def setUp(self):
        self.catalogo = Catalogo()
        self.catalogo.cargar_desde_csv("datos/peliculas.csv")

    def test_carga_peliculas(self):
        self.assertEqual(len(self.catalogo), 60)

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

    def test_buscar_arbol_encuentra_titulo_exacto_sin_tildes(self):
        resultado = self.catalogo.buscar_arbol("interestelar")
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].titulo, "Interestelar")

    def test_buscar_arbol_sin_coincidencia_devuelve_lista_vacia(self):
        self.assertEqual(self.catalogo.buscar_arbol("pelicula que no existe"), [])

    def test_listar_ordenado_por_titulo_devuelve_todas_ordenadas(self):
        ordenadas = self.catalogo.listar_ordenado_por_titulo()
        self.assertEqual(len(ordenadas), len(self.catalogo))
        titulos = [p.titulo.lower() for p in ordenadas]
        self.assertEqual(titulos, sorted(titulos))

    def test_listar_generos_no_esta_vacio(self):
        self.assertTrue(len(self.catalogo.listar_generos()) > 0)

    def test_listar_subgeneros_de_un_genero_real(self):
        subgeneros = self.catalogo.listar_subgeneros("Ciencia ficcion")
        self.assertIn("Ciberpunk", subgeneros)

    def test_explorar_genero_devuelve_solo_peliculas_de_ese_genero(self):
        resultados = self.catalogo.explorar_genero("Ciencia ficcion")
        self.assertTrue(len(resultados) > 0)
        for pelicula in resultados:
            self.assertEqual(pelicula.genero.lower(), "ciencia ficcion")

    def test_explorar_subgenero_devuelve_solo_ese_subgenero(self):
        resultados = self.catalogo.explorar_subgenero("Ciencia ficcion", "Ciberpunk")
        self.assertTrue(len(resultados) > 0)
        for pelicula in resultados:
            self.assertEqual(pelicula.subgenero.lower(), "ciberpunk")

    def test_top_n_devuelve_las_mejor_puntuadas_en_orden(self):
        titulos = [p.titulo for p in self.catalogo.top_n(5)]
        self.assertEqual(titulos, [
            "Suenos de Libertad",                           # 9.3
            "El Padrino",                                   # 9.2
            "El Caballero de la Noche",                     # 9.0 (tres empatadas: van por título)
            "El Senor de los Anillos: El Retorno del Rey",  # 9.0
            "La Lista de Schindler",                        # 9.0
        ])

    def test_top_n_coincide_con_ordenar_todo(self):
        esperado = sorted(self.catalogo.listar(), key=lambda p: p.puntaje, reverse=True)[:10]
        obtenido = self.catalogo.top_n(10)
        self.assertEqual([p.puntaje for p in obtenido], [p.puntaje for p in esperado])

    def test_top_n_filtra_por_plataformas(self):
        titulos = [p.titulo for p in self.catalogo.top_n(3, ["netflix"])]
        self.assertEqual(titulos, ["El Padrino", "Pulp Fiction", "Forrest Gump"])

    def test_top_n_mayor_que_el_catalogo_devuelve_todas(self):
        self.assertEqual(len(self.catalogo.top_n(1000)), len(self.catalogo))

    def test_top_n_no_altera_el_catalogo(self):
        cantidad = len(self.catalogo)
        self.catalogo.top_n(5)
        self.assertEqual(len(self.catalogo.listar()), cantidad)

    def test_proximos_retiros_en_orden_de_fecha(self):
        titulos = [p.titulo for p in self.catalogo.proximos_retiros(5, desde=date(2026, 9, 1))]
        self.assertEqual(titulos, [
            "Ciudad de Dios",                # 2026-11-20
            "El Conjuro",                    # 2026-12-01
            "La Llegada",                    # 2026-12-05
            "Pulp Fiction",                  # 2026-12-15
            "El Silencio de los Inocentes",  # 2026-12-20
        ])

    def test_proximos_retiros_ignora_fechas_pasadas(self):
        titulos = [p.titulo for p in self.catalogo.proximos_retiros(10, desde=date(2027, 1, 1))]
        self.assertEqual(titulos, ["Zodiaco", "Mad Max: Furia en el Camino", "Batman Inicia"])

    def test_proximos_retiros_filtra_por_plataformas(self):
        titulos = [p.titulo for p in self.catalogo.proximos_retiros(10, ["HBO Max"], desde=date(2026, 9, 1))]
        self.assertEqual(titulos, ["El Conjuro", "Mad Max: Furia en el Camino", "Batman Inicia"])

    def test_el_grafo_no_se_construye_al_cargar(self):
        self.assertIsNone(self.catalogo._grafo)
        self.catalogo.resumen_grafo()
        self.assertIsNotNone(self.catalogo._grafo)

    def test_resumen_grafo_dataset_real(self):
        vertices, aristas, densidad = self.catalogo.resumen_grafo()
        self.assertEqual(vertices, 60)
        self.assertEqual(aristas, 235)
        self.assertAlmostEqual(densidad, 235 / 1770)

    def test_obtener_pelicula_exacta_y_case_insensitive(self):
        self.assertEqual(self.catalogo.obtener_pelicula("el origen").titulo, "El Origen")
        self.assertIsNone(self.catalogo.obtener_pelicula("No Existe"))

    def test_relacionadas_ordena_del_vinculo_mas_fuerte_al_mas_debil(self):
        origen = self.catalogo.obtener_pelicula("El Origen")
        aristas = self.catalogo.relacionadas(origen)
        self.assertEqual([a.destino.titulo for a in aristas[:4]],
                         ["Batman Inicia", "El Caballero de la Noche", "Interestelar", "Oppenheimer"])
        pesos = [a.peso for a in aristas]
        self.assertEqual(pesos, sorted(pesos))

    def test_relacionadas_filtra_por_plataformas(self):
        origen = self.catalogo.obtener_pelicula("El Origen")
        for arista in self.catalogo.relacionadas(origen, ["Netflix"]):
            self.assertIn("Netflix", arista.destino.plataformas)

    def test_conexion_directa_muestra_todos_los_vinculos(self):
        arista = self.catalogo.conexion_directa(
            self.catalogo.obtener_pelicula("El Origen"), self.catalogo.obtener_pelicula("Interestelar"))
        self.assertEqual(arista.peso, 1)
        self.assertEqual(arista.vinculos, ["director: Christopher Nolan", "genero: Ciencia ficcion"])

    def test_conexion_directa_inexistente(self):
        self.assertIsNone(self.catalogo.conexion_directa(
            self.catalogo.obtener_pelicula("El Origen"), self.catalogo.obtener_pelicula("Toy Story")))

    def test_mas_conectadas(self):
        resultado = self.catalogo.mas_conectadas(2)
        self.assertEqual([(p.titulo, grado) for p, grado in resultado], [("El Origen", 16), ("Oppenheimer", 16)])

    def _titulos_camino(self, camino):
        return [pelicula.titulo for pelicula, _ in camino]

    def test_camino_entre_dos_peliculas_con_bfs(self):
        camino = self.catalogo.camino_entre(
            self.catalogo.obtener_pelicula("El Origen"), self.catalogo.obtener_pelicula("Toy Story"))
        self.assertEqual(self._titulos_camino(camino),
                         ["El Origen", "Oppenheimer", "Rescatando al Soldado Ryan", "Toy Story"])
        self.assertEqual([a.vinculos[0] for _, a in camino[1:]],
                         ["director: Christopher Nolan", "actor: Matt Damon", "actor: Tom Hanks"])

    def test_camino_bfs_es_mas_corto_que_el_arbol_dfs(self):
        from algoritmos.recorridos import dfs, reconstruir_camino
        origen = self.catalogo.obtener_pelicula("El Origen")
        destino = self.catalogo.obtener_pelicula("Toy Story")
        camino_dfs = reconstruir_camino(dfs(self.catalogo._obtener_grafo(), origen), destino)
        self.assertLess(len(self.catalogo.camino_entre(origen, destino)), len(camino_dfs))

    def test_camino_directo_es_de_un_paso(self):
        camino = self.catalogo.camino_entre(
            self.catalogo.obtener_pelicula("El Origen"), self.catalogo.obtener_pelicula("Titanic"))
        self.assertEqual(self._titulos_camino(camino), ["El Origen", "Titanic"])

    def test_camino_intermedias_solo_de_las_plataformas_del_usuario(self):
        camino = self.catalogo.camino_entre(
            self.catalogo.obtener_pelicula("Matrix"), self.catalogo.obtener_pelicula("Toy Story"), ["Netflix"])
        for pelicula, _ in camino[1:-1]:
            self.assertIn("Netflix", pelicula.plataformas)

    def test_camino_sin_conexion_por_plataformas_es_none(self):
        self.assertIsNone(self.catalogo.camino_entre(
            self.catalogo.obtener_pelicula("Matrix"), self.catalogo.obtener_pelicula("Coco"), ["Netflix"]))

    def test_explorar_en_profundidad_sigue_solo_directores_y_actores(self):
        recorrido = self.catalogo.explorar_en_profundidad(self.catalogo.obtener_pelicula("El Origen"))
        self.assertEqual(len(recorrido), 34)
        self.assertEqual(recorrido[0][0].titulo, "Batman Inicia")   # primero va al fondo por Nolan
        for _, visita in recorrido:
            self.assertLessEqual(visita.arista.peso, 2)

    def test_explorar_en_profundidad_no_incluye_al_origen(self):
        origen = self.catalogo.obtener_pelicula("El Origen")
        self.assertNotIn(origen, [p for p, _ in self.catalogo.explorar_en_profundidad(origen)])

    def test_explorar_en_profundidad_pelicula_sin_vinculos_fuertes(self):
        # Coco no comparte director ni actores con ninguna otra película del catálogo.
        self.assertEqual(self.catalogo.explorar_en_profundidad(self.catalogo.obtener_pelicula("Coco")), [])


if __name__ == "__main__":
    unittest.main()
