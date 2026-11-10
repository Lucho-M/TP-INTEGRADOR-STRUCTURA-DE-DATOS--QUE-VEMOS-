# TP7 — Grafo de películas

## 1. Por qué un grafo acá

El TP0 eligió este dominio justamente por esto: las películas comparten director, actores y género, y esas relaciones forman una **red**, no una jerarquía. En el árbol del TP5, cada nodo tiene un único padre. Acá, El Origen se conecta con Interestelar (mismo director), con Titanic (mismo actor) y con Matrix (mismo género) al mismo tiempo, y ninguna es "padre" de otra. Esa estructura, con muchas conexiones en todas las direcciones, es un **grafo**.

Resuelve F4 ("Explorar conexiones") y es la base de los próximos TP: los recorridos BFS/DFS (TP8) y el camino mínimo para F5 (TP9).

## 2. Modelo del grafo

| Elemento | Definición |
|---|---|
| **Vértice** | Una película (el objeto `Pelicula`). |
| **Arista** | Dos películas que comparten **director**, **algún actor** o **género**. |
| **Peso** | El costo del vínculo más fuerte: director = 1, actor = 2, género = 3. |
| **Tipo** | **No dirigido** y **pesado**. |
| **Representación** | **Lista de adyacencia**. |

## 3. Decisiones de diseño

### 3.1 El peso de las aristas (pendiente declarado en el TP0)

El TP0 dejó abierta esta pregunta: *¿cuánto "cuesta" pasar de una película a otra según el vínculo?* La respuesta:

- **Menor costo = vínculo más fuerte = películas más parecidas.** Dos películas del mismo director se parecen más que dos del mismo género. Por eso el director cuesta 1, el actor 2 y el género 3. Se eligió "costo" y no "similitud" porque el camino mínimo del TP9 *minimiza*: así, un camino corto pasa por películas parecidas.
- **Una sola arista por par.** Si dos películas comparten varias cosas (El Origen e Interestelar comparten director y género), hay una sola arista. Su peso es el del vínculo más fuerte (1) y guarda **todos** los vínculos para mostrarlos, como pide F5: "indicando el vínculo de cada paso".
- **Por qué no se suman los vínculos:** con un peso como "1 / cantidad de vínculos", cada arista mezcla dos ideas, el tipo de vínculo y cuántos hay, y resulta más difícil de explicar. Además, el dataset tiene pocos pares con más de un vínculo. El mínimo es simple, predecible y fácil de justificar.

**Por qué entra el género**, si es el vínculo más débil: el CSV real tiene 31 pares que comparten director y 34 que comparten actor. Con solo esos dos vínculos hay 60 aristas, pero **17 de las 60 películas quedan aisladas**: F4 no les mostraría nada y F5 nunca podría llegar a ellas. El género suma 186 pares (235 aristas en total, contando una sola vez los pares que comparten más de una cosa) y no deja ninguna película aislada.

### 3.2 No dirigido

Los tres vínculos son simétricos: si A comparte director con B, B comparte director con A. Un grafo dirigido solo tendría sentido con relaciones de un solo sentido, como "secuela de" o "hay que ver X antes que Y". El dataset no tiene esos datos.

### 3.3 Lista de adyacencia, no matriz

Con los datos reales hay **60 vértices y 235 aristas, sobre 1.770 pares posibles: una densidad del 13 %**.

| | Matriz de adyacencia | Lista de adyacencia |
|---|---|---|
| Memoria | V² = **3.600** celdas (87 % vacías) | V + 2E = **530** entradas |
| ¿A y B son vecinos? | O(1) | O(1) (dict de vecinos) u O(grado) (lista) |
| Recorrer los vecinos de A | O(V): hay que mirar toda la fila | **O(grado)**: solo los vecinos reales |

El grafo es **disperso**, así que la lista ocupa unas 7 veces menos memoria. Además, la operación que más se usa (recorrer vecinos, la base de BFS, DFS y Dijkstra) cuesta O(grado) y no O(V).

En la implementación, cada vértice guarda un **diccionario** `{vecino: Arista}` en lugar de una lista. Sigue siendo una lista de adyacencia (se guardan solo las aristas que existen), pero la consulta "¿A y B son vecinos?" pasa de O(grado) a O(1).

### 3.4 El grafo se construye la primera vez que se usa

`Catalogo` no arma el grafo en `cargar_desde_csv`, sino la primera vez que se lo pide (`_obtener_grafo`). Las aristas por género crecen como n²: los CSV sintéticos del TP2 tienen 100.000 películas repartidas en solo 8 géneros, lo que daría unos **625 millones de aristas**. `medicion.py` carga esos CSV en un `Catalogo` y no usa el grafo, así que no tiene sentido construirlo ahí.

**Limitación reconocida:** con un catálogo real grande, la arista por género haría que el grafo deje de ser disperso (la densidad tiende a 1 / cantidad de géneros). En ese caso habría que limitarla, por ejemplo a "mismo género **y** mismo subgénero", o conectar solo con las k más parecidas. Para el tamaño de la demo no hace falta.

## 4. Implementación

- `estructuras/grafo.py`: es genérico y no sabe nada de películas.
  - `Arista`: `destino`, `peso` y `vinculos`.
  - `Grafo`: `agregar_vertice`, `agregar_arista` (la guarda en los dos sentidos e ignora los lazos), `vecinos`, `arista(a, b)`, `grado`, `vertices`, `cantidad_aristas` y `densidad`.
- `servicios/red_peliculas.py`: tiene la lógica del dominio.
  - `COSTO_VINCULO`: los pesos de cada tipo de vínculo.
  - `construir_grafo(peliculas)`: en lugar de comparar los 1.770 pares, **agrupa** por cada director, actor y género (un dict `(tipo, valor) → películas`) y conecta solo dentro de cada grupo. Así nunca compara dos películas que no tienen nada en común. Los nombres se comparan normalizados, con el mismo criterio que el resto del proyecto. Los directores múltiples ("Lana Wachowski|Lilly Wachowski") se separan.

## 5. Integración real en la app

- `Catalogo`:
  - `obtener_pelicula(titulo)`: búsqueda exacta con el BST del TP3.
  - `relacionadas(pelicula, plataformas)`: los vecinos, del vínculo más fuerte al más débil, filtrados por las plataformas del usuario.
  - `conexion_directa(a, b)`.
  - `mas_conectadas(n)`: usa el **heap del TP6** con prioridad igual a menos el grado.
  - `resumen_grafo()`.
- `Terminal`:
  - **opción 11 — Explorar conexiones**: pide un título y muestra sus películas relacionadas con el costo y el vínculo. Si el título no existe, sugiere coincidencias parciales.
  - **opción 12 — Películas más conectadas**: muestra el resumen de la red y el ranking por grado.
  - "Salir" pasó de la opción 11 a la 13. Las opciones 1 a 10 no se tocaron.

## 6. Ejemplos de consultas

Usuario con Netflix, opción 11, "el origen":

```text
🕸 Relacionadas con 'El Origen' (Netflix) — 6 conexiones:
[costo 1] Interestelar — director: Christopher Nolan · genero: Ciencia ficcion
[costo 2] Django Sin Cadenas — actor: Leonardo DiCaprio
[costo 3] Her — genero: Ciencia ficcion
[costo 3] Jurassic Park — genero: Ciencia ficcion
[costo 3] La Llegada — genero: Ciencia ficcion
[costo 3] Volver al Futuro — genero: Ciencia ficcion
```

Opción 12:

```text
🕸 Red de películas: 60 películas, 235 conexiones, densidad 13.3%
1. El Origen — 16 conexiones
2. Oppenheimer — 16 conexiones
3. Titanic — 14 conexiones
```

El Origen es la más conectada porque suma vínculos de los tres tipos: Nolan (4 películas), DiCaprio (3) y Ciencia ficción, que empata con Drama como el género con más películas (11).

## 7. Pruebas

- `tests/test_grafo.py` (16 tests):
  - **Grafo genérico:** vacío, que agregar una arista cree los vértices, que la arista exista en los dos sentidos, arista inexistente, vecinos y grado, vértice aislado, que las aristas no se cuenten dos veces, densidad y que no se permitan lazos.
  - **Construcción de la red:** peso 1, 2 y 3 según el vínculo; varios vínculos en una sola arista con el peso del más fuerte; un par sin nada en común no tiene arista; vértice aislado; directores múltiples.
- `tests/test_catalogo.py` (8 tests nuevos, contra el CSV real): que el grafo no se construya al cargar, el resumen (60 vértices, 235 aristas), `obtener_pelicula`, el orden de las relacionadas, el filtro por plataforma, la conexión directa con y sin arista, y las más conectadas.
- **85 tests en total**, todos pasan.

## 8. Complejidad

| Operación | Complejidad |
|---|---|
| Construir el grafo | O(n·k + Σ g²), donde k son las características de cada película y g el tamaño de cada grupo. Equivale a O(n + E): solo se recorren pares que tienen algo en común. |
| `agregar_arista`, `arista(a, b)`, `grado` | O(1) |
| `vecinos(v)` | O(grado(v)) |
| `relacionadas` | O(grado · log grado), por el ordenamiento de los vecinos |
| `mas_conectadas(n)` | O(V + n log V), con heapify y n extracciones (TP6) |
| `cantidad_aristas`, `densidad` | O(V) |
| Memoria | O(V + E) |

## 9. Conclusión

El grafo convierte las relaciones del dominio en una red explícita, donde cada película es un vértice y cada director, actor o género compartido es una arista. Es no dirigido, porque los vínculos son simétricos, y pesado, con costo según la fuerza del vínculo. Esto resuelve el pendiente del TP0 y prepara el terreno para el camino mínimo del TP9. Por la baja densidad (13 %), se eligió una lista de adyacencia. El grafo se integra con lo anterior: usa el BST para encontrar la película, el heap para el ranking por grado y el filtro por plataformas del usuario.
