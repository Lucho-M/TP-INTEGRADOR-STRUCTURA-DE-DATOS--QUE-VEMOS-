import unicodedata


def normalizar_titulo(titulo):
    """Clave de ordenamiento del árbol: título en minúscula y sin tildes.

    Así "Interestelar" e "interestelar" (o con tilde mal tipeada) caen en
    la misma posición del árbol.
    """
    titulo = titulo.strip().lower()
    sin_tildes = unicodedata.normalize("NFKD", titulo)
    return "".join(c for c in sin_tildes if not unicodedata.combining(c))


class NodoArbol:
    """Nodo del árbol binario de búsqueda.

    Guarda una LISTA de películas (no una sola) para poder resolver remakes
    o títulos repetidos: si dos películas normalizan a la misma clave,
    conviven en el mismo nodo en vez de perderse una.
    """

    def __init__(self, clave, pelicula):
        self.clave = clave
        self.peliculas = [pelicula]
        self.izq = None
        self.der = None


class ArbolBST:
    """Árbol binario de búsqueda, ordenado por título normalizado de película."""

    def __init__(self):
        self.raiz = None

    def insertar(self, pelicula):
        clave = normalizar_titulo(pelicula.titulo)
        self.raiz = self._insertar(self.raiz, clave, pelicula)

    def _insertar(self, nodo, clave, pelicula):
        if nodo is None:
            return NodoArbol(clave, pelicula)
        if clave < nodo.clave:
            nodo.izq = self._insertar(nodo.izq, clave, pelicula)
        elif clave > nodo.clave:
            nodo.der = self._insertar(nodo.der, clave, pelicula)
        else:
            # Mismo título normalizado (remake): se agrega al mismo nodo.
            nodo.peliculas.append(pelicula)
        return nodo

    def buscar(self, titulo):
        """Búsqueda EXACTA (case-insensitive, sin tildes). O(log n) promedio.

        Devuelve la lista de películas con ese título (puede haber más de
        una si es un remake), o [] si no está.
        """
        clave = normalizar_titulo(titulo)
        nodo = self._buscar(self.raiz, clave)
        return list(nodo.peliculas) if nodo else []

    def _buscar(self, nodo, clave):
        if nodo is None:
            return None
        if clave == nodo.clave:
            return nodo
        if clave < nodo.clave:
            return self._buscar(nodo.izq, clave)
        return self._buscar(nodo.der, clave)

    def recorrido_inorder(self):
        """Izq, nodo, der: devuelve las películas ordenadas por título."""
        resultado = []
        self._inorder(self.raiz, resultado)
        return resultado

    def _inorder(self, nodo, resultado):
        if nodo is None:
            return
        self._inorder(nodo.izq, resultado)
        resultado.extend(nodo.peliculas)
        self._inorder(nodo.der, resultado)

    def recorrido_preorder(self):
        """Nodo, izq, der."""
        resultado = []
        self._preorder(self.raiz, resultado)
        return resultado

    def _preorder(self, nodo, resultado):
        if nodo is None:
            return
        resultado.extend(nodo.peliculas)
        self._preorder(nodo.izq, resultado)
        self._preorder(nodo.der, resultado)

    def recorrido_postorder(self):
        """Izq, der, nodo."""
        resultado = []
        self._postorder(self.raiz, resultado)
        return resultado

    def _postorder(self, nodo, resultado):
        if nodo is None:
            return
        self._postorder(nodo.izq, resultado)
        self._postorder(nodo.der, resultado)
        resultado.extend(nodo.peliculas)

    def altura(self):
        """Altura del árbol (cantidad de niveles). Útil para ver desbalance (TP4)."""
        return self._altura(self.raiz)

    def _altura(self, nodo):
        if nodo is None:
            return 0
        return 1 + max(self._altura(nodo.izq), self._altura(nodo.der))
