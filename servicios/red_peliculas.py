from estructuras.arbol import normalizar_titulo
from estructuras.grafo import Grafo

# Costo de cada tipo de vínculo (TP7). Menor costo = vínculo más fuerte = películas más parecidas.
# Lo usa el camino mínimo del TP9: prefiere pasar por vínculos de director antes que de género.
COSTO_VINCULO = {"director": 1, "actor": 2, "genero": 3}


def construir_grafo(peliculas):
    """Arma la red de películas: una arista por cada par que comparte director, actor o género.

    Si un par comparte varias cosas, sigue siendo UNA arista: el peso es el del vínculo
    más fuerte (el menor costo) y se guardan todos los vínculos para poder mostrarlos.

    En vez de comparar todos los pares (n² comparaciones, la mayoría sin nada en común),
    agrupa por cada director, actor y género, y solo conecta dentro de cada grupo.
    """
    grupos = {}
    for pelicula in peliculas:
        for tipo, valor in _caracteristicas(pelicula):
            grupos.setdefault((tipo, normalizar_titulo(valor)), (valor, []))[1].append(pelicula)

    vinculos_por_par = {}
    for (tipo, _), (valor, miembros) in grupos.items():
        for i in range(len(miembros)):
            for j in range(i + 1, len(miembros)):
                par = (miembros[i], miembros[j])
                vinculos_por_par.setdefault(par, []).append((tipo, valor))

    grafo = Grafo()
    for pelicula in peliculas:
        grafo.agregar_vertice(pelicula)
    for (a, b), vinculos in vinculos_por_par.items():
        vinculos.sort(key=lambda v: COSTO_VINCULO[v[0]])
        peso = COSTO_VINCULO[vinculos[0][0]]
        grafo.agregar_arista(a, b, peso, [f"{tipo}: {valor}" for tipo, valor in vinculos])
    return grafo


def _caracteristicas(pelicula):
    """Los (tipo, valor) por los que una película se puede conectar con otra."""
    for director in pelicula.director.split("|"):
        if director.strip():
            yield "director", director.strip()
    for actor in pelicula.actores:
        if actor.strip():
            yield "actor", actor.strip()
    if pelicula.genero.strip():
        yield "genero", pelicula.genero.strip()
