"""Genera datasets sintéticos de películas para medir tiempos de búsqueda (TP2).

Uso: python datos/generar.py
Crea datos/peliculas_{n}.csv para n = 100, 1.000, 10.000, 100.000.
"""
import csv
import random
from pathlib import Path

DATOS_DIR = Path(__file__).resolve().parent
TAMANOS = (100, 1_000, 10_000, 100_000)
GENEROS = ["Accion", "Drama", "Comedia", "Ciencia ficcion", "Terror", "Animacion", "Musical", "Thriller"]
PLATAFORMAS = ["Netflix", "HBO Max", "Disney+", "Amazon Prime"]

random.seed(271)  # semilla fija: datasets reproducibles entre corridas


def generar_dataset(n, ruta):
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([
            "id", "titulo", "anio", "genero", "subgenero", "director",
            "actores", "puntaje", "duracion", "plataformas", "fecha_retiro",
        ])
        for i in range(n):
            escritor.writerow([
                i + 1,
                f"Pelicula {i}",
                random.randint(1970, 2026),
                random.choice(GENEROS),
                "",
                f"Director {i % 500}",
                f"Actor {i % 300}|Actor {(i + 1) % 300}",
                round(random.uniform(1.0, 10.0), 1),
                random.randint(80, 200),
                random.choice(PLATAFORMAS),
                "",
            ])


if __name__ == "__main__":
    for n in TAMANOS:
        ruta = DATOS_DIR / f"peliculas_{n}.csv"
        generar_dataset(n, ruta)
        print(f"Generado {ruta.name} con {n} películas.")
