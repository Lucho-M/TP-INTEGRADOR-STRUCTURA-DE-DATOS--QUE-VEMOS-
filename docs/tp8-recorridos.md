# TP8 — Recorridos: BFS y DFS

> **Alcance:** el docente quitó el TP9 (camino mínimo con pesos), así que esta es la última etapa con código. El TP10 es la defensa. Por eso, **F5 ("encontrar el camino entre dos películas") se resuelve acá con BFS**: el camino con **menos pasos**, no el de menor costo total.

## 1. Qué se pidió y qué consulta resuelve cada recorrido

| Recorrido | Consulta del dominio | Por qué ese recorrido |
|---|---|---|
| **BFS** | **F5 — "¿Cómo se conectan El Origen y Toy Story?"** Muestra la cadena de películas y el vínculo de cada paso. | BFS visita por niveles: primero todo lo que está a 1 paso, después a 2, y así. La primera vez que llega a una película, llegó por el camino con **menos aristas**. Es la garantía que necesita "la conexión más corta". |
| **DFS** | **F4 ampliada — "¿Qué universo de películas sale de El Origen por directores y actores?"** Muestra todas las películas alcanzables siguiendo solo vínculos de personas, y desde cuál se llegó a cada una. | Se quiere **todo lo conectado** (la componente conexa), no lo más cercano. DFS sigue una cadena hasta el fondo (Nolan → Matt Damon → Scorsese → …) antes de volver atrás. Es la forma natural de "seguir el hilo" y recorre la componente completa con poca memoria extra. |

## 2. Implementación

`algoritmos/recorridos.py` es genérico y funciona con cualquier `Grafo` del TP7, no solo con películas.

- **`bfs(grafo, origen, destino=None, ...)`**: usa una **cola** (`collections.deque`; `popleft` es O(1), mientras que `list.pop(0)` sería O(n)). Un vértice se marca como visitado **al encolarlo**, no al sacarlo, así nunca entra dos veces a la cola. Si se le pasa `destino`, corta apenas lo saca de la cola.
- **`dfs(grafo, origen, ...)`**: usa una **pila explícita** (una lista con `append` y `pop`) en lugar de recursión. Es la misma lección del TP4: el BST degenerado chocaba con el límite de recursión de Python (1000). Con 5.000 películas encadenadas, un DFS recursivo fallaría (hay un test para eso). Los vecinos se apilan al revés para visitar en el mismo orden que la versión recursiva.
- Los dos devuelven `{vertice: Visita}` en orden de visita. Cada `Visita` guarda el **padre**, la **arista** por la que se llegó y el **nivel**: en BFS es la distancia al origen y en DFS la profundidad en el árbol DFS.
- **`reconstruir_camino(visitados, destino)`**: va de padre en padre desde el destino hasta el origen y después invierte la lista.
- **Filtros** (sirven para los dos recorridos):
  - `permitidos`: solo pasa por las películas de las plataformas del usuario. Es la funcionalidad transversal del TP0, que decía que F5 tenía que pasar solo por películas disponibles.
  - `peso_maximo`: ignora aristas caras.
  - `orden`: mira los vecinos del vínculo más fuerte al más débil y, si empatan, por título. Así el resultado es siempre el mismo. Como pide la consigna, **los pesos del TP7 siguen teniendo uso** sin Dijkstra: a igual cantidad de pasos, BFS prefiere el camino que se descubre primero por vínculos fuertes.

## 3. Integración en la app

- `Catalogo`:
  - `camino_entre(origen, destino, plataformas)`: usa BFS. Las películas intermedias tienen que estar en las plataformas del usuario; las dos puntas no, porque las eligió él.
  - `explorar_en_profundidad(origen, plataformas, peso_maximo=2)`: usa DFS solo por director y actor. Con el género, casi todo el catálogo queda conectado y el recorrido no dice nada.
- `Terminal`:
  - **opción 13 — Camino entre dos películas (BFS)**;
  - **opción 14 — Explorar en profundidad (DFS)**;
  - "Salir" pasó de la 13 a la 15. Las opciones 1 a 12 no se tocaron.

## 4. Casos de uso reales (salida del programa)

**BFS, sin filtro de plataformas:** `El Origen → Oppenheimer (director: Christopher Nolan) → Rescatando al Soldado Ryan (actor: Matt Damon) → Toy Story (actor: Tom Hanks)`, **3 pasos**.

**BFS con Netflix, opción 13, de El Origen a Zodiaco:**

```text
🎬 El Origen
   ↓ actor: Leonardo DiCaprio
🎬 Django Sin Cadenas
   ↓ director: Quentin Tarantino · actor: Christoph Waltz
🎬 Bastardos sin Gloria
   ↓ actor: Brad Pitt
🎬 Pecados Capitales
   ↓ director: David Fincher · genero: Thriller
🎬 Zodiaco

4 paso(s) — es el camino con menos pasos posible.
```

Con Netflix, **Matrix → Coco no tiene camino**. Coco solo se conecta por el género Animación. De esas películas, la única en Netflix es El Viaje de Chihiro, y Chihiro tampoco se conecta con nada fuera de Animación. No hay forma de entrar a ese grupo pasando solo por Netflix, así que el programa avisa que no hay camino.

**DFS, sin filtro, desde El Origen:** recorre **34 películas** conectadas por personas. Las primeras siguen la cadena hasta el fondo antes de volver atrás:

```text
1. Batman Inicia (prof. 1) ← El Origen · director: Christopher Nolan
2. El Caballero de la Noche (prof. 2) ← Batman Inicia · director: Christopher Nolan
3. Interestelar (prof. 3) ← El Caballero de la Noche · director: Christopher Nolan
4. Oppenheimer (prof. 4) ← Interestelar · director: Christopher Nolan
5. Los Infiltrados (prof. 5) ← Oppenheimer · actor: Matt Damon
6. Buenos Muchachos (prof. 6) ← Los Infiltrados · director: Martin Scorsese
...
```

**Componentes por vínculos de personas** (DFS desde cada película no visitada): el catálogo se divide en un "universo" grande de 35 películas, uno de 4, dos de 2 y **17 películas sin director ni actores en común con ninguna otra**. Es el mismo número de aisladas que justificó, en el TP7, sumar el género como vínculo.

## 5. BFS vs. DFS: diferencias

| | BFS | DFS |
|---|---|---|
| Estructura auxiliar | Cola (FIFO) | Pila (LIFO), o la pila de llamadas si es recursivo |
| Orden de visita | Por niveles: todos los vecinos y después los vecinos de los vecinos | Una rama hasta el fondo y después vuelve atrás (*backtracking*) |
| Camino que encuentra | **El de menos aristas** (en grafos sin pesos) | **Cualquiera**: no garantiza el más corto |
| Ejemplo real | El Origen → Toy Story en **3 pasos** | El árbol DFS llega a Toy Story en **31 pasos** |
| Memoria extra | Puede guardar un nivel entero en la cola (ancho del grafo) | Guarda la rama actual en la pila (profundidad del grafo) |
| Conviene para | Distancia o camino más corto en pasos, "lo más cercano" | Recorrer todo lo conectado, componentes, detectar ciclos, orden topológico |

**Qué no resuelve BFS:** minimiza **pasos**, no **costo**. Un camino de 2 pasos por género (costo 3 + 3 = 6) le gana a uno de 3 pasos por director (costo 1 + 1 + 1 = 3). Minimizar el costo total era el objetivo de Dijkstra en el TP9, que la cátedra quitó. Los pesos quedan en el grafo y se usan para ordenar vecinos y para filtrar en el DFS.

## 6. Complejidad

| Operación | Complejidad | Por qué |
|---|---|---|
| `bfs` / `dfs` (grafo completo) | **O(V + E)** | Cada vértice entra una vez a la cola o pila y se visita una vez. Cada arista se mira dos veces, una desde cada extremo, porque el grafo es no dirigido. |
| …con `orden` | O(V + E log Δ) | Ordena los vecinos de cada vértice (Δ = grado máximo). Con grados chicos, es prácticamente lineal. |
| `reconstruir_camino` | O(largo del camino) ≤ O(V) | |
| Memoria | O(V) | El dict de visitados, más la cola o la pila. |
| `camino_entre` | O(V + E) en el peor caso | BFS corta antes si encuentra el destino. |

Con lista de adyacencia, recorrer los vecinos cuesta O(grado). Con matriz de adyacencia, BFS y DFS serían **O(V²)**, porque habría que mirar la fila entera de cada vértice. Es el argumento del TP7 para elegir la lista.

**Medición** (`python algoritmos/experimentos/medicion_recorridos.py`: grafos al azar con unas 3 aristas por vértice, o sea grado promedio 6, recorrido completo desde el vértice 0):

| V | E | BFS | DFS | BFS, µs por (V+E) | DFS, µs por (V+E) |
|---:|---:|---:|---:|---:|---:|
| 1.000 | 2.994 | 1,2 ms | 1,4 ms | 0,29 | 0,35 |
| 10.000 | 29.990 | 32,2 ms | 36,5 ms | 0,81 | 0,91 |
| 100.000 | 299.991 | 445,5 ms | 455,2 ms | 1,11 | 1,14 |

Lectura honesta: si el costo fuera exactamente O(V + E), la última columna sería constante. No lo es, pero el crecimiento está lejos de cuadrático. Al pasar de 10.000 a 100.000 vértices, los elementos crecen 10 veces y el tiempo unas 14. El costo extra por elemento viene de la memoria: con grafos grandes, los diccionarios y objetos dejan de entrar en la memoria caché del procesador, y cada acceso es más lento. Es un efecto del hardware, no del algoritmo. BFS y DFS tardan casi lo mismo, como era de esperar, porque los dos miran cada vértice y cada arista una vez.

## 7. Pruebas

- `tests/test_recorridos.py` (14 tests sobre un grafo chico armado a mano):
  - **Orden de visita:** BFS por niveles; DFS hasta el fondo; nivel y padre en DFS.
  - **Alcance:** los dos recorren la componente completa y no el vértice aislado; un vértice aislado se visita solo a sí mismo; un origen inexistente devuelve vacío.
  - **Caminos:** el camino de BFS es el de menos aristas; el de DFS puede ser más largo; un destino no alcanzado da None; un camino a sí mismo; BFS corta al encontrar el destino.
  - **Filtros y límites:** `permitidos` y `peso_maximo`; DFS sobre una cadena de 5.000 vértices sin `RecursionError`.
- `tests/test_catalogo.py` (8 tests nuevos, contra el CSV real):
  - **`camino_entre`:** El Origen → Toy Story en 3 pasos, con los vínculos; el camino BFS es más corto que el del árbol DFS; una conexión directa es de 1 paso; las películas intermedias son solo de las plataformas del usuario; con plataformas sin conexión da None.
  - **`explorar_en_profundidad`:** desde El Origen recorre 34 películas, solo por director o actor; no incluye al origen; Coco no tiene vínculos de personas con nadie.
- **107 tests en total**, todos pasan.

## 8. Conclusión

BFS y DFS recorren el mismo grafo del TP7 con la misma complejidad, O(V + E), y responden preguntas distintas. BFS, con una cola, da **la conexión más corta** entre dos películas (F5). DFS, con una pila, recorre **todo lo conectado** a una película siguiendo los vínculos de personas hasta el fondo. El caso real lo muestra: El Origen → Toy Story en 3 pasos con BFS contra 31 en el árbol DFS. Con esta etapa, el sistema integra todas las estructuras de la materia: lista, búsqueda binaria, BST/AVL, árbol general, heap y grafo con BFS/DFS. Cada una resuelve una funcionalidad concreta del TP0.
