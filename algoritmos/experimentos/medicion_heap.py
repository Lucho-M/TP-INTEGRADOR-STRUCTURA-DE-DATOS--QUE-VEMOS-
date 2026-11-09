"""TP6 - Top-N: heap (construir + extraer N) vs. ordenar todo el catálogo y cortar.

Uso: python algoritmos/experimentos/medicion_heap.py
Genera las películas en memoria con puntajes al azar (semilla fija), igual que
medicion_avl.py. Compara tres estrategias para obtener el Top-N:
- sorted(): ordenar todo con el sort de Python (escrito en C) y quedarse con N.
- Heap: construir el heap en O(n) y extraer N, O(n + N log n), en Python puro.
- Ordenar a mano: ordenar todo con un heap-sort propio (extraer las n), O(n log n),
  también en Python puro. Es la comparación justa contra el heap: mismo lenguaje,
  misma estructura, solo cambia cuántos elementos se extraen.
"""
import random
import sys
import timeit
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from estructuras.heap import Heap  # noqa: E402
from modelos.pelicula import Pelicula  # noqa: E402
from servicios.catalogo import prioridad_ranking  # noqa: E402

TAMANOS = (100, 1_000, 10_000, 100_000)
TOP = 10
NUMERO = 5
REPETICIONES = 3

random.seed(271)


def _peliculas(n):
    return [
        Pelicula(
            titulo=f"Pelicula {i}", anio=2000, genero="Drama", subgenero="",
            director="Director", actores=[], puntaje=round(random.uniform(1.0, 10.0), 1),
            duracion=100, plataformas=["Netflix"], fecha_retiro="",
        )
        for i in range(n)
    ]


def medir_ms(func, *args):
    tiempos = timeit.repeat(lambda: func(*args), number=NUMERO, repeat=REPETICIONES)
    return (min(tiempos) / NUMERO) * 1000


def top_sorted(peliculas, n):
    return sorted(peliculas, key=prioridad_ranking)[:n]


def top_heap(peliculas, n):
    heap = Heap(prioridad_ranking, peliculas)
    return [heap.extraer() for _ in range(min(n, len(heap)))]


def ordenar_todo_con_heap(peliculas, n):
    heap = Heap(prioridad_ranking, peliculas)
    ordenadas = [heap.extraer() for _ in range(len(heap))]
    return ordenadas[:n]


def main():
    encabezado = (
        f"{'N':>8} | {'sorted() en C (ms)':>18} | {'Heap Top-' + str(TOP) + ' (ms)':>17} "
        f"| {'Ordenar todo a mano (ms)':>24}"
    )
    print(encabezado)
    print("-" * len(encabezado))

    for n in TAMANOS:
        peliculas = _peliculas(n)
        assert [p.puntaje for p in top_heap(peliculas, TOP)] == [p.puntaje for p in top_sorted(peliculas, TOP)]
        t_sorted = medir_ms(top_sorted, peliculas, TOP)
        t_heap = medir_ms(top_heap, peliculas, TOP)
        t_todo = medir_ms(ordenar_todo_con_heap, peliculas, TOP)
        print(f"{n:>8} | {t_sorted:>18.3f} | {t_heap:>17.3f} | {t_todo:>24.3f}")


if __name__ == "__main__":
    main()
