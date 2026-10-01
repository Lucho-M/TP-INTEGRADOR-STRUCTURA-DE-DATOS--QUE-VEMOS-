"""TP2/TP3 - Compara búsqueda secuencial, binaria (bisect) y por árbol BST.

Uso: python algoritmos/experimentos/medicion.py
Requiere haber corrido antes: python datos/generar.py
"""
import sys
import timeit
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from servicios.catalogo import Catalogo  # noqa: E402

TAMANOS = (100, 1_000, 10_000, 100_000)
NUMERO = 20   # llamadas por repetición
REPETICIONES = 5  # repeticiones; nos quedamos con el mínimo (timeit.repeat)


def medir_ms(func, *args):
    tiempos = timeit.repeat(lambda: func(*args), number=NUMERO, repeat=REPETICIONES)
    return (min(tiempos) / NUMERO) * 1000  # ms por llamada, mínimo (no promedio)


def main():
    print(f"{'N':>10} | {'Secuencial (ms)':>16} | {'Binaria (ms)':>13} | {'Arbol BST (ms)':>14} | {'Altura':>6}")
    print("-" * 70)
    resultados = []
    for n in TAMANOS:
        catalogo = Catalogo()
        catalogo.cargar_desde_csv(str(REPO_ROOT / "datos" / f"peliculas_{n}.csv"))
        titulo_existente = f"Pelicula {n - 1}"  # última película: peor caso para la secuencial

        t_secuencial = medir_ms(catalogo.buscar, titulo_existente)
        t_binaria = medir_ms(catalogo.buscar_binaria, titulo_existente)
        t_arbol = medir_ms(catalogo.buscar_arbol, titulo_existente)
        altura = catalogo.altura_arbol()

        resultados.append((n, t_secuencial, t_binaria, t_arbol, altura))
        print(f"{n:>10} | {t_secuencial:>16.4f} | {t_binaria:>13.4f} | {t_arbol:>14.4f} | {altura:>6}")

    return resultados


if __name__ == "__main__":
    main()
