"""TP4 - Compara BST (TP3) vs AVL en el peor caso posible: insertar títulos ya ordenados.

Uso: python algoritmos/experimentos/medicion_avl.py
No depende de los CSV de datos/generar.py (esos están en orden aleatorio):
genera los títulos en memoria, ya ordenados alfabéticamente, que es
justamente el caso que degenera un BST común (ver docs/tp3-arbolbst.md,
secciones 6-7, y docs/tp4-avl.md).
"""
import math
import sys
import timeit
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from estructuras.arbol import ArbolBST  # noqa: E402
from estructuras.avl import ArbolAVL  # noqa: E402
from modelos.pelicula import Pelicula  # noqa: E402

TAMANOS = (10, 50, 100, 500, 1_000, 10_000, 100_000)
NUMERO = 20
REPETICIONES = 5


def _pelicula(titulo):
    return Pelicula(
        titulo=titulo, anio=2000, genero="Drama", subgenero="",
        director="Director", actores=[], puntaje=8.0,
        duracion=100, plataformas=["Netflix"], fecha_retiro="",
    )


def titulos_ordenados(n):
    """Títulos ya en orden alfabético: el peor caso posible para insertar en un BST."""
    ancho = len(str(n - 1))
    return [f"Pelicula {str(i).zfill(ancho)}" for i in range(n)]


def medir_ms(func, *args):
    tiempos = timeit.repeat(lambda: func(*args), number=NUMERO, repeat=REPETICIONES)
    return (min(tiempos) / NUMERO) * 1000


def construir_bst(titulos):
    arbol = ArbolBST()
    for titulo in titulos:
        arbol.insertar(_pelicula(titulo))
    return arbol


def construir_avl(titulos):
    arbol = ArbolAVL()
    for titulo in titulos:
        arbol.insertar(_pelicula(titulo))
    return arbol


def main():
    encabezado = (
        f"{'N':>8} | {'Altura BST':>14} | {'Altura AVL':>10} | {'log2(N) ideal':>13} "
        f"| {'Busqueda BST (ms)':>18} | {'Busqueda AVL (ms)':>18}"
    )
    print(encabezado)
    print("-" * len(encabezado))

    for n in TAMANOS:
        titulos = titulos_ordenados(n)
        ultimo = titulos[-1]
        ideal = f"{math.log2(n):.1f}"

        avl = construir_avl(titulos)
        altura_avl = str(avl.altura())
        t_avl = f"{medir_ms(avl.buscar, ultimo):.4f}"

        try:
            bst = construir_bst(titulos)
            altura_bst = str(bst.altura())
            t_bst = f"{medir_ms(bst.buscar, ultimo):.4f}"
        except RecursionError:
            # Esto ES el resultado, no un error del script: con datos ya
            # ordenados, el BST común degenera en una lista enlazada de
            # profundidad N. A partir de cierto N, insertar/buscar de forma
            # recursiva choca con el límite de recursión de Python
            # (sys.getrecursionlimit(), 1000 por defecto) antes de terminar.
            altura_bst = "RecursionError"
            t_bst = "N/A"

        fila = (
            f"{n:>8} | {altura_bst:>14} | {altura_avl:>10} | {ideal:>13} "
            f"| {t_bst:>18} | {t_avl:>18}"
        )
        print(fila)


if __name__ == "__main__":
    main()
