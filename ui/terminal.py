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
                self._explorar_conexiones()

            elif opcion == "12":
                self._mostrar_mas_conectadas()

            elif opcion == "13":
                self._mostrar_camino()

            elif opcion == "14":
                self._explorar_en_profundidad()

            elif opcion == "15":
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

    def _pedir_pelicula(self, mensaje):
        """Pide un título exacto. Si no existe, sugiere coincidencias parciales y devuelve None."""
        titulo = input(f"\n{mensaje}: ").strip()
        pelicula = self._catalogo.obtener_pelicula(titulo)
        if pelicula is None:
            print(f"\n⚠️ No hay una película llamada '{titulo}'.")
            sugerencias = self._catalogo.buscar(titulo)
            if sugerencias:
                print("¿Quisiste decir alguna de estas?")
                for sugerida in sugerencias[:5]:
                    print(f"   - {sugerida.titulo}")
        return pelicula

    def _explorar_conexiones(self):
        """Vecinos de una película en el grafo (F4, TP7), con el vínculo que los une."""
        pelicula = self._pedir_pelicula("🕸 Escribí el título de la película")
        if pelicula is None:
            return
        plataformas = self._usuario.plataformas_contratadas
        aristas = self._catalogo.relacionadas(pelicula, plataformas)
        donde = ", ".join(plataformas) if plataformas else "todas las plataformas"
        print(f"\n🕸 Relacionadas con '{pelicula.titulo}' ({donde}) — {len(aristas)} conexiones:")
        _imprimir_linea()
        if not aristas:
            print("⚠️ No hay películas relacionadas disponibles.")
        for arista in aristas:
            print(f"[costo {arista.peso}] {arista.destino.titulo} — {' · '.join(arista.vinculos)}")

    def _mostrar_mas_conectadas(self):
        """Las películas con más vínculos de la red (grado del vértice), vía heap."""
        vertices, aristas, densidad = self._catalogo.resumen_grafo()
        print(f"\n🕸 Red de películas: {vertices} películas, {aristas} conexiones, densidad {densidad:.1%}")
        n = self._pedir_cantidad("¿Cuántas películas querés ver?")
        print(f"\n🕸 Las {n} películas más conectadas:")
        _imprimir_linea()
        for idx, (pelicula, grado) in enumerate(self._catalogo.mas_conectadas(n), 1):
            print(f"{idx}. {pelicula.titulo} — {grado} conexiones")

    def _mostrar_camino(self):
        """F5: cómo se conectan dos películas, en la menor cantidad de pasos (BFS, TP8)."""
        origen = self._pedir_pelicula("🧭 Película de origen")
        if origen is None:
            return
        destino = self._pedir_pelicula("🧭 Película de destino")
        if destino is None:
            return
        camino = self._catalogo.camino_entre(origen, destino, self._usuario.plataformas_contratadas)
        print(f"\n🧭 De '{origen.titulo}' a '{destino.titulo}':")
        _imprimir_linea()
        if camino is None:
            print("⚠️ No hay forma de conectarlas pasando solo por películas de tus plataformas.")
            return
        print(f"🎬 {camino[0][0].titulo}")
        for pelicula, arista in camino[1:]:
            print(f"   ↓ {' · '.join(arista.vinculos)}")
            print(f"🎬 {pelicula.titulo}")
        print(f"\n{len(camino) - 1} paso(s) — es el camino con menos pasos posible.")

    def _explorar_en_profundidad(self):
        """Todo el "universo" de una película por directores y actores (DFS, TP8)."""
        origen = self._pedir_pelicula("🔎 Película desde la que explorar")
        if origen is None:
            return
        recorrido = self._catalogo.explorar_en_profundidad(origen, self._usuario.plataformas_contratadas)
        print(f"\n🔎 Desde '{origen.titulo}', siguiendo directores y actores en profundidad:")
        _imprimir_linea()
        if not recorrido:
            print("⚠️ No comparte director ni actores con otra película de tus plataformas.")
            return
        for idx, (pelicula, visita) in enumerate(recorrido, 1):
            print(f"{idx}. {pelicula.titulo} (prof. {visita.nivel}) ← {visita.padre.titulo} · {visita.arista.vinculos[0]}")
        print(f"\n{len(recorrido)} película(s) conectadas por personas con '{origen.titulo}'.")

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
        print("11. 🕸 Explorar conexiones de una película (grafo)")
        print("12. 🕸 Películas más conectadas (grafo)")
        print("13. 🧭 Camino entre dos películas (BFS)")
        print("14. 🔎 Explorar en profundidad por directores y actores (DFS)")
        print("15. ❌ Salir")
        print("=" * 55)
