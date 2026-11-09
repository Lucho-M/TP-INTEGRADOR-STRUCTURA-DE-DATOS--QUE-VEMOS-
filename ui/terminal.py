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
                titulo = input("\n🌳 Escribí el título EXACTO (usa el árbol BST): ")
                resultados = self._catalogo.buscar_arbol(titulo)
                print(f"\n🌳 Resultado exacto para: '{titulo}'")
                _imprimir_linea()
                _mostrar_peliculas(resultados)

            elif opcion == "7":
                print("\n🌳 Catálogo ordenado alfabéticamente (recorrido inorder del árbol):")
                _imprimir_linea()
                _mostrar_peliculas(self._catalogo.listar_ordenado_por_titulo())

            elif opcion == "8":
                self._explorar_categorias()

            elif opcion == "9":
                self._mostrar_top_n()

            elif opcion == "10":
                self._mostrar_alertas_retiro()

            elif opcion == "11":
                print("\n👋 ¡Gracias por usar el sistema! Hasta luego.")
                break

            else:
                print("\n⚠️ Opción inválida. Intentá nuevamente.")

            input("\nPresioná ENTER para continuar...")

    def _explorar_categorias(self):
        """Navega Género -> Subgénero (árbol general, TP5)."""
        generos = self._catalogo.listar_generos()
        print("\n📂 Géneros disponibles:")
        _imprimir_linea()
        for idx, genero in enumerate(generos, 1):
            print(f"{idx}. {genero}")

        seleccion = input("\nElegí un género (número, ENTER para volver): ").strip()
        if not seleccion.isdigit() or not (1 <= int(seleccion) <= len(generos)):
            return
        genero = generos[int(seleccion) - 1]

        subgeneros = self._catalogo.listar_subgeneros(genero)
        if not subgeneros:
            print(f"\n📂 '{genero}' no tiene subgéneros cargados. Películas del género:")
            _imprimir_linea()
            _mostrar_peliculas(self._catalogo.explorar_genero(genero))
            return

        print(f"\n📂 Subgéneros de '{genero}':")
        _imprimir_linea()
        print("0. (ver todas las películas de este género)")
        for idx, subgenero in enumerate(subgeneros, 1):
            print(f"{idx}. {subgenero}")

        seleccion = input("\nElegí un subgénero (número, ENTER para volver): ").strip()
        if not seleccion.isdigit() or not (0 <= int(seleccion) <= len(subgeneros)):
            return

        if seleccion == "0":
            print(f"\n📂 Todas las películas de '{genero}':")
            _imprimir_linea()
            _mostrar_peliculas(self._catalogo.explorar_genero(genero))
        else:
            subgenero = subgeneros[int(seleccion) - 1]
            print(f"\n📂 '{genero}' -> '{subgenero}':")
            _imprimir_linea()
            _mostrar_peliculas(self._catalogo.explorar_subgenero(genero, subgenero))

    def _pedir_cantidad(self, mensaje, por_defecto=5):
        entrada = input(f"\n{mensaje} (ENTER = {por_defecto}): ").strip()
        return int(entrada) if entrada.isdigit() and int(entrada) > 0 else por_defecto

    def _mostrar_top_n(self):
        """Ranking por puntaje (heap, TP6), filtrado por las plataformas del usuario."""
        n = self._pedir_cantidad("🏆 ¿Cuántas películas querés en el ranking?")
        plataformas = self._usuario.plataformas_contratadas
        ranking = self._catalogo.top_n(n, plataformas)
        donde = ", ".join(plataformas) if plataformas else "todas las plataformas"
        print(f"\n🏆 TOP {n} — {donde}")
        _imprimir_linea()
        if not ranking:
            print("⚠️ No hay películas para mostrar.")
        medallas = {1: "🥇", 2: "🥈", 3: "🥉"}
        for idx, pelicula in enumerate(ranking, 1):
            print(f"{medallas.get(idx, f'{idx}.')} {pelicula.titulo} ⭐{pelicula.puntaje} [{', '.join(pelicula.plataformas)}]")

    def _mostrar_alertas_retiro(self):
        """Próximas películas en salir del catálogo (heap por fecha, TP6)."""
        n = self._pedir_cantidad("⏰ ¿Cuántas alertas querés ver?")
        alertas = self._catalogo.proximos_retiros(n, self._usuario.plataformas_contratadas)
        print("\n⏰ Se van pronto de tus plataformas:")
        _imprimir_linea()
        if not alertas:
            print("⚠️ No hay películas con fecha de retiro próxima.")
        for pelicula in alertas:
            print(f"📅 {pelicula.fecha_retiro} — {pelicula}")

    def _mostrar_menu(self):
        print("\n" + "=" * 55)
        print("                MENÚ PRINCIPAL")
        print("=" * 55)
        print("1. 📋 Listar todas las películas")
        print("2. 🔍 Buscar película por título (parcial)")
        print("3. 🎬 Filtrar películas por género")
        print("4. 📺 Filtrar películas por plataforma")
        print("5. 👤 Ver mis plataformas")
        print("6. 🌳 Buscar por título exacto (árbol BST)")
        print("7. 🌳 Listar ordenado alfabéticamente (árbol BST)")
        print("8. 📂 Explorar categorías (Género -> Subgénero)")
        print("9. 🏆 Top N mejor puntuadas en mis plataformas (heap)")
        print("10. ⏰ Alertas: próximas en salir del catálogo (heap)")
        print("11. ❌ Salir")
        print("=" * 55)
