from estructuras.arbol import normalizar_titulo


class NodoGeneral:
    """Nodo de un árbol general (N-ario): cualquier cantidad de hijos, sin orden por clave.

    Guarda su nombre (género o subgénero), la lista de sus hijos y las
    películas que pertenecen directamente a este nodo (no a sus hijos).
    En la jerarquía Género -> Subgénero, las películas quedan en el nodo
    subgénero (la hoja); el nodo género solo agrupa a sus subgéneros.
    """

    def __init__(self, nombre):
        self.nombre = nombre
        self.hijos = []
        self.peliculas = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def buscar_hijo(self, nombre):
        """Busca un hijo directo por nombre (case-insensitive, sin tildes). O(hijos), no O(n)."""
        clave = normalizar_titulo(nombre)
        for hijo in self.hijos:
            if normalizar_titulo(hijo.nombre) == clave:
                return hijo
        return None

    def __repr__(self):
        return f"NodoGeneral({self.nombre!r}, hijos={len(self.hijos)}, peliculas={len(self.peliculas)})"


class ArbolCategorias:
    """Árbol general de categorías: Catálogo -> Género -> Subgénero -> películas.

    Decisiones de diseño (ver docs/tp5-arbolgeneral.md):
    - Cada subgénero es un nodo propio COLGADO DE SU GÉNERO, no un nodo
      compartido entre géneros. Dos subgéneros con el mismo nombre bajo
      géneros distintos (ej. "Epica" en Acción y en Ciencia ficción) son
      dos nodos distintos con sus propias películas: así sigue siendo un
      árbol (cada nodo tiene un único padre), no un grafo.
    - Una película cuelga de un solo subgénero (coincide con el dataset
      real: cada fila del CSV tiene un único par género/subgénero). Si una
      película no tiene subgénero cargado, queda directamente en su nodo
      de género.
    """

    def __init__(self):
        self.raiz = NodoGeneral("Catalogo")

    def insertar(self, pelicula):
        nodo_genero = self._obtener_o_crear_hijo(self.raiz, pelicula.genero)
        if pelicula.subgenero:
            nodo_subgenero = self._obtener_o_crear_hijo(nodo_genero, pelicula.subgenero)
            nodo_subgenero.peliculas.append(pelicula)
        else:
            nodo_genero.peliculas.append(pelicula)

    def _obtener_o_crear_hijo(self, nodo, nombre):
        hijo = nodo.buscar_hijo(nombre)
        if hijo is None:
            hijo = NodoGeneral(nombre)
            nodo.agregar_hijo(hijo)
        return hijo

    # ---------- consultas (las usa Catalogo / la terminal) ----------

    def generos(self):
        """Nombres de los géneros de primer nivel, en el orden en que se cargaron."""
        return [hijo.nombre for hijo in self.raiz.hijos]

    def subgeneros(self, genero):
        """Nombres de los subgéneros de un género dado, o [] si el género no existe."""
        nodo = self.raiz.buscar_hijo(genero)
        return [hijo.nombre for hijo in nodo.hijos] if nodo else []

    def peliculas_de_genero(self, genero):
        """Todas las películas bajo un género (recorre todos sus subgéneros)."""
        nodo = self.raiz.buscar_hijo(genero)
        return self._recolectar_peliculas(nodo) if nodo else []

    def peliculas_de_subgenero(self, genero, subgenero):
        """Películas de un subgénero puntual dentro de un género puntual."""
        nodo_genero = self.raiz.buscar_hijo(genero)
        if nodo_genero is None:
            return []
        nodo_subgenero = nodo_genero.buscar_hijo(subgenero)
        return list(nodo_subgenero.peliculas) if nodo_subgenero else []

    def _recolectar_peliculas(self, nodo):
        resultado = list(nodo.peliculas)
        for hijo in nodo.hijos:
            resultado.extend(self._recolectar_peliculas(hijo))
        return resultado

    # ---------- recorridos ----------

    def recorrido_preorder(self):
        """Nodo, después sus hijos de izquierda a derecha (DFS). Recorrido natural de un árbol N-ario."""
        resultado = []
        self._preorder(self.raiz, resultado)
        return resultado

    def _preorder(self, nodo, resultado):
        resultado.append(nodo)
        for hijo in nodo.hijos:
            self._preorder(hijo, resultado)

    def altura(self):
        return self._altura(self.raiz)

    def _altura(self, nodo):
        if not nodo.hijos:
            return 1
        return 1 + max(self._altura(hijo) for hijo in nodo.hijos)
