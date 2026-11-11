"""TP8 - Mide BFS y DFS sobre grafos aleatorios de tamaño creciente.

Uso: python algoritmos/experimentos/medicion_recorridos.py
Genera grafos dispersos en memoria (~3 aristas por vértice: una del camino base y
dos al azar, semilla fija) y recorre el grafo completo desde el vértice 0. Si BFS y DFS son O(V + E),
la columna "us por (V+E)" debería mantenerse aproximadamente constante.
"""
import random
import sys
import timeit
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from algoritmos.recorridos import bfs, dfs  # noqa: E402
from estructuras.grafo import Grafo  # noqa: E402

TAMANOS = (1_000, 10_000, 100_000)
ARISTAS_AL_AZAR_POR_VERTICE = 2
NUMERO = 3
REPETICIONES = 3

random.seed(271)


def grafo_aleatorio(v):
    """Un camino 0-1-2-...-(v-1) (para que todo sea alcanzable) más aristas al azar."""
    grafo = Grafo()
    for i in range(v - 1):
        grafo.agregar_arista(i, i + 1, 1)
    for i in range(v):
        for _ in range(ARISTAS_AL_AZAR_POR_VERTICE):
            grafo.agregar_arista(i, random.randrange(v), 1)
    return grafo


def medir_ms(func, *args):
    tiempos = timeit.repeat(lambda: func(*args), number=NUMERO, repeat=REPETICIONES)
    return (min(tiempos) / NUMERO) * 1000


def main():
    encabezado = (
        f"{'V':>8} | {'E':>8} | {'BFS (ms)':>9} | {'DFS (ms)':>9} "
        f"| {'BFS us por (V+E)':>16} | {'DFS us por (V+E)':>16}"
    )
    print(encabezado)
    print("-" * len(encabezado))

    for v in TAMANOS:
        grafo = grafo_aleatorio(v)
        e = grafo.cantidad_aristas()
        t_bfs = medir_ms(bfs, grafo, 0)
        t_dfs = medir_ms(dfs, grafo, 0)
        por_elemento_bfs = t_bfs * 1000 / (v + e)
        por_elemento_dfs = t_dfs * 1000 / (v + e)
        print(f"{v:>8} | {e:>8} | {t_bfs:>9.2f} | {t_dfs:>9.2f} "
              f"| {por_elemento_bfs:>16.3f} | {por_elemento_dfs:>16.3f}")


if __name__ == "__main__":
    main()
