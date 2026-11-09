class Heap:
    """Heap binaria (min-heap) guardada en una lista, implementada a mano (TP6).

    Arriba queda siempre el elemento con MENOR prioridad(elemento). La función de
    prioridad la elige quien usa el heap, así la misma clase sirve para F3 y F6:
    - Top-N por puntaje (max-heap): prioridad = lambda p: -p.puntaje
    - Alertas de retiro (min-heap): prioridad = lambda p: fecha de retiro

    Árbol completo en lista: para la posición i, el padre está en (i - 1) // 2
    y los hijos en 2*i + 1 y 2*i + 2.
    """

    def __init__(self, prioridad, elementos=None):
        self._prioridad = prioridad
        self._datos = list(elementos) if elementos else []
        self._construir()

    def insertar(self, elemento):
        """Agrega al final y lo hace subir hasta su lugar. O(log n)."""
        self._datos.append(elemento)
        self._subir(len(self._datos) - 1)

    def extraer(self):
        """Saca y devuelve el tope (el de menor prioridad). O(log n). None si está vacío."""
        if not self._datos:
            return None
        self._intercambiar(0, len(self._datos) - 1)
        tope = self._datos.pop()
        if self._datos:
            self._bajar(0)
        return tope

    def ver_tope(self):
        """Devuelve el tope sin sacarlo. O(1). None si está vacío."""
        return self._datos[0] if self._datos else None

    def _construir(self):
        """Heapify de abajo hacia arriba: O(n), más barato que n inserciones (O(n log n)).

        Las hojas (segunda mitad de la lista) ya son heaps de un elemento, así que
        alcanza con hacer bajar a cada nodo interno, del último al primero.
        """
        for i in range(len(self._datos) // 2 - 1, -1, -1):
            self._bajar(i)

    def _subir(self, i):
        """Mientras sea "menor" que su padre, intercambia con él."""
        while i > 0:
            padre = (i - 1) // 2
            if not self._es_menor(i, padre):
                break
            self._intercambiar(i, padre)
            i = padre

    def _bajar(self, i):
        """Mientras algún hijo sea "menor", intercambia con el menor de los dos."""
        n = len(self._datos)
        while True:
            izquierdo = 2 * i + 1
            derecho = 2 * i + 2
            menor = i
            if izquierdo < n and self._es_menor(izquierdo, menor):
                menor = izquierdo
            if derecho < n and self._es_menor(derecho, menor):
                menor = derecho
            if menor == i:
                break
            self._intercambiar(i, menor)
            i = menor

    def _es_menor(self, i, j):
        return self._prioridad(self._datos[i]) < self._prioridad(self._datos[j])

    def _intercambiar(self, i, j):
        self._datos[i], self._datos[j] = self._datos[j], self._datos[i]

    def __len__(self):
        return len(self._datos)

    def __repr__(self):
        return f"Heap({len(self._datos)} elementos, tope={self.ver_tope()!r})"
