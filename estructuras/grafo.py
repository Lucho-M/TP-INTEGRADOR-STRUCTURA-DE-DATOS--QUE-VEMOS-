class Arista:
    """Conexión hacia un vecino: a quién llega, cuánto cuesta y por qué existe."""

    def __init__(self, destino, peso, vinculos=None):
        self.destino = destino
        self.peso = peso
        self.vinculos = list(vinculos) if vinculos else []

    def __repr__(self):
        return f"Arista({self.destino!r}, peso={self.peso}, vinculos={self.vinculos})"


class Grafo:
    """Grafo NO dirigido y pesado, representado con lista de adyacencia (TP7).

    Cada vértice tiene un diccionario {vecino: Arista}. Es la "lista" de adyacencia,
    pero guardada en un dict para responder "¿a y b son vecinos?" en O(1) en vez de
    recorrer la lista. Memoria O(V + E): solo se guardan las aristas que existen, a
    diferencia de una matriz V x V, que reserva lugar para todos los pares.

    Los vértices pueden ser cualquier objeto hasheable (acá, objetos Pelicula).
    """

    def __init__(self):
        self._adyacencia = {}

    def agregar_vertice(self, vertice):
        """O(1). Si ya existe, no hace nada."""
        if vertice not in self._adyacencia:
            self._adyacencia[vertice] = {}

    def agregar_arista(self, origen, destino, peso, vinculos=None):
        """O(1). No dirigido: se guarda en los dos sentidos, con el mismo peso y vínculos."""
        if origen is destino:
            return
        self.agregar_vertice(origen)
        self.agregar_vertice(destino)
        self._adyacencia[origen][destino] = Arista(destino, peso, vinculos)
        self._adyacencia[destino][origen] = Arista(origen, peso, vinculos)

    def vecinos(self, vertice):
        """Aristas que salen del vértice. O(grado). Lista vacía si el vértice no existe."""
        return list(self._adyacencia.get(vertice, {}).values())

    def arista(self, origen, destino):
        """La arista entre dos vértices, o None si no son adyacentes. O(1)."""
        return self._adyacencia.get(origen, {}).get(destino)

    def grado(self, vertice):
        """Cantidad de vecinos. O(1)."""
        return len(self._adyacencia.get(vertice, {}))

    def vertices(self):
        return list(self._adyacencia)

    def cantidad_aristas(self):
        """O(V). Cada arista está guardada dos veces (una por extremo), por eso se divide."""
        return sum(len(vecinos) for vecinos in self._adyacencia.values()) // 2

    def densidad(self):
        """Aristas existentes / aristas posibles, V(V-1)/2. Entre 0 (sin aristas) y 1 (completo)."""
        v = len(self._adyacencia)
        if v < 2:
            return 0.0
        return self.cantidad_aristas() / (v * (v - 1) / 2)

    def __contains__(self, vertice):
        return vertice in self._adyacencia

    def __len__(self):
        return len(self._adyacencia)

    def __repr__(self):
        return f"Grafo({len(self)} vértices, {self.cantidad_aristas()} aristas)"
