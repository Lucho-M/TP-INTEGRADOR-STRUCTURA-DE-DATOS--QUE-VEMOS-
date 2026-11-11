"""Recorridos de grafos: BFS y DFS, implementados a mano (TP8).

Los dos devuelven un dict {vertice: Visita} en el ORDEN en que se visitó cada
vértice (los dict de Python mantienen el orden de inserción). Cada Visita guarda
desde qué vértice se llegó y por qué arista, así se puede reconstruir el camino.

Filtros opcionales (los dos recorridos los aceptan):
- permitidos: conjunto de vértices por los que se puede pasar (ej: películas de las
  plataformas del usuario). El origen siempre se visita.
- peso_maximo: ignora aristas más "caras" (ej: 2 = solo director o actor, sin género).
- orden: función clave para decidir en qué orden se miran los vecinos, así el
  resultado es siempre el mismo (sin ella, depende del orden de carga).
"""
from collections import deque


class Visita:
    """Cómo se llegó a un vértice durante un recorrido."""

    def __init__(self, padre, arista, nivel):
        self.padre = padre      # vértice desde el que se llegó (None para el origen)
        self.arista = arista    # arista padre -> este vértice (None para el origen)
        self.nivel = nivel      # BFS: distancia en aristas al origen. DFS: profundidad en el árbol DFS.

    def __repr__(self):
        return f"Visita(padre={self.padre!r}, nivel={self.nivel})"


def bfs(grafo, origen, destino=None, permitidos=None, peso_maximo=None, orden=None):
    """Recorrido en ANCHURA: visita por niveles, primero los vecinos, después los vecinos de los vecinos.

    Usa una COLA (FIFO). Garantiza que cada vértice se alcanza con la MENOR cantidad de aristas
    posible. Si se pasa `destino`, corta apenas lo encuentra. O(V + E).
    """
    if origen not in grafo:
        return {}
    visitados = {origen: Visita(None, None, 0)}
    cola = deque([origen])
    while cola:
        actual = cola.popleft()
        if actual is destino:
            break
        for arista in _vecinos_validos(grafo, actual, permitidos, peso_maximo, orden):
            if arista.destino not in visitados:
                visitados[arista.destino] = Visita(actual, arista, visitados[actual].nivel + 1)
                cola.append(arista.destino)
    return visitados


def dfs(grafo, origen, permitidos=None, peso_maximo=None, orden=None):
    """Recorrido en PROFUNDIDAD: sigue un camino hasta el fondo antes de volver atrás.

    Usa una PILA (LIFO) explícita en vez de recursión: así no choca con el límite de
    recursión de Python en grafos grandes (el mismo problema que tuvo el BST del TP4).
    Visita los vecinos en el mismo orden que la versión recursiva. O(V + E).
    """
    if origen not in grafo:
        return {}
    visitados = {}
    pila = [(origen, None, None, 0)]
    while pila:
        actual, padre, arista, profundidad = pila.pop()
        if actual in visitados:
            continue
        visitados[actual] = Visita(padre, arista, profundidad)
        # Se apilan al revés para que el primer vecino (según `orden`) sea el primero en salir.
        for siguiente in reversed(_vecinos_validos(grafo, actual, permitidos, peso_maximo, orden)):
            if siguiente.destino not in visitados:
                pila.append((siguiente.destino, actual, siguiente, profundidad + 1))
    return visitados


def reconstruir_camino(visitados, destino):
    """Camino origen -> destino como lista de (vertice, arista con la que se llegó). None si no se alcanzó."""
    if destino not in visitados:
        return None
    camino = []
    actual = destino
    while actual is not None:
        visita = visitados[actual]
        camino.append((actual, visita.arista))
        actual = visita.padre
    camino.reverse()
    return camino


def _vecinos_validos(grafo, vertice, permitidos, peso_maximo, orden):
    aristas = [
        a for a in grafo.vecinos(vertice)
        if (permitidos is None or a.destino in permitidos)
        and (peso_maximo is None or a.peso <= peso_maximo)
    ]
    if orden is not None:
        aristas.sort(key=lambda a: (a.peso, orden(a.destino)))
    return aristas
