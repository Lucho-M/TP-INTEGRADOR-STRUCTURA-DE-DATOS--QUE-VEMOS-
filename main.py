import sys

from servicios.catalogo import Catalogo
from ui.terminal import Terminal


def main():
    if sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    catalogo = Catalogo()
    catalogo.cargar_desde_csv("datos/peliculas.csv")
    print("\n" + "=" * 55)
    print("             ¿Qué Vemos?")
    print("=" * 55)
    print(f"🎥 Catálogo cargado: {len(catalogo)} películas.")
    Terminal(catalogo).iniciar()


if __name__ == "__main__":
    main()
