from modelos.usuario import Usuario


def _imprimir_linea():
    print("-" * 55)


def _mostrar_peliculas(lista):
    if not lista:
        print("⚠️ No hay películas para mostrar.")
        return
    for idx, pelicula in enumerate(lista, 1):
        print(f"{idx}. {pelicula}")


class Terminal:
    """Interfaz de línea de comandos. No contiene lógica de negocio: todo se lo pide al Catalogo."""

    def __init__(self, catalogo):
        self._catalogo = catalogo
        self._usuario = self._pedir_plataformas()

    def _pedir_plataformas(self):
        print("\n👤 ¿Qué plataformas tenés contratadas? (separadas por coma, ENTER para omitir)")
        entrada = input("Plataformas: ").strip()
        plataformas = [p.strip() for p in entrada.split(",") if p.strip()]
        return Usuario("Vos", plataformas)

    def iniciar(self):
        while True:
            self._mostrar_menu()
            opcion = input("Selecciona una opción: ").strip()

            if opcion == "1":
                print("\n📋 Lista completa de películas:")
                _imprimir_linea()
                _mostrar_peliculas(self._catalogo.listar())

            elif opcion == "2":
                busqueda = input("\n🔍 Escribí el título o parte: ")
                resultados = self._catalogo.buscar(busqueda)
                print(f"\n🔍 Resultados para: '{busqueda}'")
                _imprimir_linea()
                _mostrar_peliculas(resultados)

            elif opcion == "3":
                genero = input("\n🎬 Escribí el género: ")
                resultados = self._catalogo.filtrar_por_genero(genero)
                print(f"\n🎬 Películas de género: '{genero}'")
                _imprimir_linea()
                _mostrar_peliculas(resultados)

            elif opcion == "4":
                plataforma = input("\n📺 Escribí el nombre de la plataforma: ")
                resultados = self._catalogo.filtrar_por_plataforma(plataforma)
                print(f"\n📺 Disponibles en: '{plataforma}'")
                _imprimir_linea()
                _mostrar_peliculas(resultados)

            elif opcion == "5":
                plataformas = ", ".join(self._usuario.plataformas_contratadas) or "ninguna declarada"
                print(f"\n👤 Tus plataformas: {plataformas}")

            elif opcion == "6":
                print("\n👋 ¡Gracias por usar el sistema! Hasta luego.")
                break

            else:
                print("\n⚠️ Opción inválida. Intentá nuevamente.")

            input("\nPresioná ENTER para continuar...")

    def _mostrar_menu(self):
        print("\n" + "=" * 55)
        print("                MENÚ PRINCIPAL")
        print("=" * 55)
        print("1. 📋 Listar todas las películas")
        print("2. 🔍 Buscar película por título")
        print("3. 🎬 Filtrar películas por género")
        print("4. 📺 Filtrar películas por plataforma")
        print("5. 👤 Ver mis plataformas")
        print("6. ❌ Salir")
        print("=" * 55)
