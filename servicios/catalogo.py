import bisect
import csv
from datetime import date

from estructuras.arbol import ArbolBST, normalizar_titulo
from estructuras.arbol_general import ArbolCategorias
from estructuras.heap import Heap
from modelos.pelicula import Pelicula
from modelos.plataforma import Plataforma


def prioridad_ranking(pelicula):
    """Prioridad del Top-N (F3): mayor puntaje primero; si empatan, orden alfabético.

    El puntaje va negado porque Heap es un min-heap: -9.2 < -8.7, así que la de 9.2 queda arriba.
    """
    return (-pelicula.puntaje, normalizar_titulo(pelicula.titulo))


def prioridad_retiro(pelicula):
    """Prioridad de las alertas (F6): la fecha de retiro más cercana primero."""
    return (date.fromisoformat(pelicula.fecha_retiro), normalizar_titulo(pelicula.titulo))


class Catalogo:
    """Carga el dataset de películas y resuelve búsquedas, listados y filtros."""

    def __init__(self):
        self._peliculas = []
        # Lista paralela ordenada por título (minúscula), para la búsqueda binaria (TP2).
        self._peliculas_por_titulo = []
        self._titulos_ordenados = []
        # Árbol binario de búsqueda por título normalizado (TP3).
        self._arbol = ArbolBST()
        # Árbol general de categorías: Género -> Subgénero (TP5).
        self._categorias = ArbolCategorias()

    def cargar_desde_csv(self, ruta):
        with open(ruta, encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                pelicula = Pelicula(
                    titulo=fila["titulo"],
                    anio=int(fila["anio"]),
                    genero=fila["genero"],
                    subgenero=fila["subgenero"],
                    director=fila["director"],
                    actores=fila["actores"].split("|") if fila["actores"] else [],
                    puntaje=float(fila["puntaje"]),
                    duracion=int(fila["duracion"]),
                    plataformas=fila["plataformas"].split("|") if fila["plataformas"] else [],
                    fecha_retiro=fila["fecha_retiro"],
                )
                self._peliculas.append(pelicula)
                self._arbol.insertar(pelicula)
                self._categorias.insertar(pelicula)
        self._ordenar_por_titulo()

    def _ordenar_por_titulo(self):
        """Ordena una sola vez (O(n log n)), para no pagar ese costo en cada búsqueda binaria."""
        self._peliculas_por_titulo = sorted(self._peliculas, key=lambda p: p.titulo.lower())
        self._titulos_ordenados = [p.titulo.lower() for p in self._peliculas_por_titulo]

    def listar(self):
        return list(self._peliculas)

    def buscar(self, texto):
        """Búsqueda secuencial, coincidencia parcial. O(n): recorre toda la lista."""
        texto = texto.strip().lower()
        return [p for p in self._peliculas if texto in p.titulo.lower()]

    def buscar_binaria(self, titulo):
        """Búsqueda binaria por título EXACTO (case-insensitive) sobre la lista ordenada. O(log n)."""
        titulo = titulo.strip().lower()
        idx = bisect.bisect_left(self._titulos_ordenados, titulo)
        if idx < len(self._titulos_ordenados) and self._titulos_ordenados[idx] == titulo:
            return self._peliculas_por_titulo[idx]
        return None

    def buscar_arbol(self, titulo):
        """Búsqueda exacta (sin tildes, case-insensitive) usando el árbol BST. O(log n) promedio."""
        return self._arbol.buscar(titulo)

    def listar_ordenado_por_titulo(self):
        """Recorrido inorder del árbol: devuelve todas las películas ordenadas por título."""
        return self._arbol.recorrido_inorder()

    def altura_arbol(self):
        return self._arbol.altura()

    def listar_generos(self):
        """Géneros de primer nivel del árbol de categorías (TP5)."""
        return self._categorias.generos()

    def listar_subgeneros(self, genero):
        return self._categorias.subgeneros(genero)

    def explorar_genero(self, genero):
        """Todas las películas de un género, sin importar el subgénero."""
        return self._categorias.peliculas_de_genero(genero)

    def explorar_subgenero(self, genero, subgenero):
        return self._categorias.peliculas_de_subgenero(genero, subgenero)

    def top_n(self, n, plataformas=None):
        """Las n mejor puntuadas, usando un heap (TP6). O(m + n log m), m = candidatas.

        Si se pasan plataformas, solo entran al heap las películas disponibles en alguna.
        """
        return self._extraer_n(Heap(prioridad_ranking, self._disponibles(plataformas)), n)

    def proximos_retiros(self, n, plataformas=None, desde=None):
        """Las n películas que se van antes del catálogo, desde hoy (o `desde`) en adelante (TP6).

        Las que no tienen fecha de retiro no entran al heap: no hay nada que alertar.
        """
        desde = desde or date.today()
        candidatas = [
            p for p in self._disponibles(plataformas)
            if p.fecha_retiro and date.fromisoformat(p.fecha_retiro) >= desde
        ]
        return self._extraer_n(Heap(prioridad_retiro, candidatas), n)

    def _disponibles(self, plataformas):
        if not plataformas:
            return self._peliculas
        buscadas = {pl.strip().lower() for pl in plataformas}
        return [p for p in self._peliculas if any(pl.lower() in buscadas for pl in p.plataformas)]

    @staticmethod
    def _extraer_n(heap, n):
        """Saca del heap los n primeros (o todos, si hay menos de n)."""
        resultado = []
        while heap and len(resultado) < n:
            resultado.append(heap.extraer())
        return resultado

    def filtrar_por_genero(self, genero):
        genero = genero.strip().lower()
        return [p for p in self._peliculas if p.genero.lower() == genero]

    def filtrar_por_plataforma(self, plataforma):
        plataforma = plataforma.strip().lower()
        return [p for p in self._peliculas if plataforma in [pl.lower() for pl in p.plataformas]]

    def obtener_plataformas(self):
        plataformas = {}
        for pelicula in self._peliculas:
            for nombre in pelicula.plataformas:
                if nombre not in plataformas:
                    plataformas[nombre] = Plataforma(nombre)
                plataformas[nombre].agregar_pelicula(pelicula)
        return list(plataformas.values())

    def __len__(self):
        return len(self._peliculas)
