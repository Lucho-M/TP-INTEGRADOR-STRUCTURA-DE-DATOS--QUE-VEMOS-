import bisect
import csv

from modelos.pelicula import Pelicula
from modelos.plataforma import Plataforma


class Catalogo:
    """Carga el dataset de películas y resuelve búsquedas, listados y filtros."""

    def __init__(self):
        self._peliculas = []
        # Lista paralela ordenada por título (minúscula), para la búsqueda binaria (TP2).
        self._peliculas_por_titulo = []
        self._titulos_ordenados = []

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
