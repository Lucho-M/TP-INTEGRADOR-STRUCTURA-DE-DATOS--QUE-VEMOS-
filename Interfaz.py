from gestor_datos import Gestor

def imprimir_linea():
    print("-" * 55)

def mostrar_peliculas(lista):
    if not lista:
        print("⚠️ No hay películas para mostrar.")
        return
    for idx, p in enumerate(lista, 1):
        print(f"{idx}. {p}")

def menu():
    print("\n" + "=" * 55)
    print("          🎥  GESTOR DE PELÍCULAS")
    print("=" * 55)
    
    def GestorDatos():
        ...

    gestor = GestorDatos()
    gestor.cargar_desde_json("datos.json")
    
    while True:
        print("\n" + "=" * 55)
        print("                MENÚ PRINCIPAL")
        print("=" * 55)
        print("1. 📋 Listar todas las películas")
        print("2. 🔍 Buscar película por título")
        print("3. 🎬 Filtrar películas por género")
        print("4. 📺 Filtrar películas por plataforma")
        print("5. 👤 Ver plataformas contratadas por usuario")
        print("6. ❌ Salir")
        print("=" * 55)
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            print("\n📋 Lista completa de películas:")
            imprimir_linea()
            mostrar_peliculas(gestor.listar_peliculas())
        
        elif opcion == "2":
            busqueda = input("\n🔍 Escribe el título o parte: ")
            resultados = gestor.buscar_pelicula(busqueda)
            print(f"\n🔍 Resultados para: '{busqueda}'")
            imprimir_linea()
            mostrar_peliculas(resultados)
        
        elif opcion == "3":
            genero = input("\n🎬 Escribe el género: ")
            resultados = gestor.filtrar_por_genero(genero)
            print(f"\n🎬 Películas de: '{genero}'")
            imprimir_linea()
            mostrar_peliculas(resultados)
        
        elif opcion == "4":
            plataforma = input("\n📺 Escribe el nombre de la plataforma: ")
            resultados = gestor.filtrar_por_plataforma(plataforma)
            print(f"\n📺 En: '{plataforma}'")
            imprimir_linea()
            mostrar_peliculas(resultados)
        
        elif opcion == "5":
            print("\n👤 Lista de usuarios y sus plataformas:")
            imprimir_linea()
            for u in gestor.usuarios:
                print(f"\n👤 Usuario: {u.get_nombre()}")
                plataformas = ", ".join([p.get_nombre() for p in u.get_plataformas()])
                print(f"   📺 Plataformas: {plataformas}")
                historial = u.get_historial().get_peliculas()
                if historial:
                    print(f"   📜 Historial:")
                    for p in historial:
                        print(f"      • {p.get_titulo()}")
        
        elif opcion == "6":
            print("\n👋 ¡Gracias por usar el sistema! Hasta luego.")
            break
        
        else:
            print("\n⚠️ Opción inválida. Intenta nuevamente.")
        
        input("\nPresiona ENTER para continuar...")

class _name_:
    ...
    menu()