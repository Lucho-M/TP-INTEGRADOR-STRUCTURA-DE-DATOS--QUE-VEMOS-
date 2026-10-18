from estructuras.arbol import normalizar_titulo


class NodoAVL:
    """Nodo del árbol AVL.

    Además de clave/películas/hijos (igual que NodoArbol del TP3), guarda la
    altura del subárbol que cuelga de él. Guardarla acá evita recorrer todo
    el subárbol cada vez que hace falta el factor de balance: sin esto, cada
    inserción pasaría de O(log n) a O(n) y se perdería la ventaja de balancear.
    """

    def __init__(self, clave, pelicula):
        self.clave = clave
        self.peliculas = [pelicula]
        self.izq = None
        self.der = None
        self.altura = 1


class ArbolAVL:
    """Árbol binario de búsqueda auto-balanceado (AVL), ordenado por título normalizado.

    Misma clave e interfaz que ArbolBST (TP3): se puede usar uno u otro para
    comparar (ver algoritmos/experimentos/medicion_avl.py). La diferencia es
    que después de cada inserción se revisa el factor de balance de los
    nodos en el camino de vuelta a la raíz y se rota si hace falta, lo que
    garantiza altura O(log n) sin importar el orden de inserción (a
    diferencia del BST común: ver docs/tp3-arbolbst.md, secciones 6-7).
    """

    def __init__(self):
        self.raiz = None

    # ---------- inserción ----------

    def insertar(self, pelicula):
        clave = normalizar_titulo(pelicula.titulo)
        self.raiz = self._insertar(self.raiz, clave, pelicula)

    def _insertar(self, nodo, clave, pelicula):
        if nodo is None:
            return NodoAVL(clave, pelicula)

        if clave < nodo.clave:
            nodo.izq = self._insertar(nodo.izq, clave, pelicula)
        elif clave > nodo.clave:
            nodo.der = self._insertar(nodo.der, clave, pelicula)
        else:
            # Mismo título normalizado (remake): se agrega al mismo nodo.
            # No cambia la forma del árbol, así que no hace falta rebalancear.
            nodo.peliculas.append(pelicula)
            return nodo

        nodo.altura = 1 + max(self._altura_nodo(nodo.izq), self._altura_nodo(nodo.der))
        return self._rebalancear(nodo, clave)

    # ---------- balance y rotaciones ----------

    def _altura_nodo(self, nodo):
        if nodo is None:
            return 0
        return nodo.altura

    def _factor_balance(self, nodo):
        return self._altura_nodo(nodo.izq) - self._altura_nodo(nodo.der)

    def _rebalancear(self, nodo, clave):
        """Chequea el factor de balance de `nodo` tras insertar `clave` y rota si hace falta.

        Los cuatro casos clásicos de AVL:
        - Izquierda-Izquierda: balance > 1 y la clave entró por la izquierda del hijo izquierdo.
        - Derecha-Derecha: balance < -1 y la clave entró por la derecha del hijo derecho.
        - Izquierda-Derecha: balance > 1 pero la clave entró por la derecha del hijo izquierdo (caso doble).
        - Derecha-Izquierda: balance < -1 pero la clave entró por la izquierda del hijo derecho (caso doble).
        """
        balance = self._factor_balance(nodo)

        if balance > 1 and clave < nodo.izq.clave:
            return self._rotacion_derecha(nodo)

        if balance < -1 and clave > nodo.der.clave:
            return self._rotacion_izquierda(nodo)

        if balance > 1 and clave > nodo.izq.clave:
            nodo.izq = self._rotacion_izquierda(nodo.izq)
            return self._rotacion_derecha(nodo)

        if balance < -1 and clave < nodo.der.clave:
            nodo.der = self._rotacion_derecha(nodo.der)
            return self._rotacion_izquierda(nodo)

        return nodo

    def _rotacion_derecha(self, z):
        """Rotación simple a la derecha (resuelve el caso Izquierda-Izquierda).

              z                  y
             / \                / \
            y   T3   -->       x   z
           / \                    / \
          x   T2                T2  T3
        """
        y = z.izq
        t2 = y.der

        y.der = z
        z.izq = t2

        z.altura = 1 + max(self._altura_nodo(z.izq), self._altura_nodo(z.der))
        y.altura = 1 + max(self._altura_nodo(y.izq), self._altura_nodo(y.der))
        return y

    def _rotacion_izquierda(self, z):
        """Rotación simple a la izquierda (resuelve el caso Derecha-Derecha). Espejo de la anterior."""
        y = z.der
        t2 = y.izq

        y.izq = z
        z.der = t2

        z.altura = 1 + max(self._altura_nodo(z.izq), self._altura_nodo(z.der))
        y.altura = 1 + max(self._altura_nodo(y.izq), self._altura_nodo(y.der))
        return y

    # ---------- búsqueda ----------

    def buscar(self, titulo):
        """Búsqueda exacta (case-insensitive, sin tildes). O(log n) garantizado (nunca degenera)."""
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

    # ---------- recorridos ----------

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
        """Altura del árbol. A diferencia del ArbolBST, no hace falta recorrerlo: ya está en la raíz."""
        return self._altura_nodo(self.raiz)
