# TP6 — Heap (Cola de prioridad)

## 1. Por qué un heap acá

El TP0 (`docs/TP00-que-vemos.md`) asignó el heap a dos funcionalidades:

- **F3 — Top N:** las N películas mejor puntuadas entre las plataformas que tiene el usuario.
- **F6 — Alertas de salida del catálogo:** las películas que se van antes, según la fecha de retiro (dato simulado).

Las dos piden lo mismo: **"dame primero la más importante"**, sin necesidad de ordenar el resto. Eso es exactamente una **cola de prioridad**. Las estructuras anteriores no lo resuelven bien: el BST/AVL ordena por título (no por puntaje ni por fecha) y el árbol general agrupa por categoría, sin ningún orden de importancia.

## 2. Función de prioridad

Están definidas en `servicios/catalogo.py`, como funciones sueltas para poder testearlas y reutilizarlas:

| Funcionalidad | Función | Criterio | Desempate |
|---|---|---|---|
| F3 Top N | `prioridad_ranking` | mayor `puntaje` primero (se devuelve `-puntaje`) | título alfabético |
| F6 Alertas | `prioridad_retiro` | `fecha_retiro` más cercana primero | título alfabético |

**Por qué solo el puntaje y no una combinación** (puntaje + popularidad + año): el dataset no tiene un dato de popularidad (cantidad de votos o vistas), y combinar el puntaje con el año sería inventar un peso sin justificación. El desempate por título hace que el resultado sea **determinístico**: ante el mismo puntaje, siempre sale el mismo orden. Esto se nota en el dataset real, donde El Señor de los Anillos y Pulp Fiction tienen los dos 8.9.

## 3. Decisiones de diseño

1. **Una sola clase `Heap` genérica, que recibe la función de prioridad.** Es un min-heap: arriba queda el elemento con la prioridad *menor*. Para que funcione como max-heap del puntaje alcanza con negarlo (`-9.2 < -8.7`, así que la de 9.2 queda arriba). Así no hay dos clases casi iguales (`MaxHeap` y `MinHeap`) y la misma estructura, ya testeada, resuelve F3 y F6.
2. **El heap se construye en cada consulta y no se guarda como atributo del catálogo.** Para sacar el Top-N hay que *extraer*, y extraer **vacía** el heap. Si fuera un atributo, después de la primera consulta habría que reconstruirlo igual. Además, cada consulta tiene un conjunto distinto de candidatas (depende de las plataformas del usuario). Construirlo cuesta O(n) (ver la sección 4), lo mismo que recorrer la lista una vez.
3. **El filtro por plataformas se aplica antes de insertar.** Solo entran al heap las películas disponibles en alguna plataforma del usuario. El heap queda más chico y nunca hay que extraer y descartar películas que el usuario no puede ver.
4. **Las películas sin `fecha_retiro`, o con una fecha que ya pasó, no entran al heap de alertas.** Una película que no se va, o que ya se fue, no genera alerta. "Hoy" se puede reemplazar con el parámetro `desde`, así los tests no dependen del día en que se corren.
5. **Dataset actualizado.** Las 5 fechas de retiro simuladas del CSV (sept.–nov. 2026) ya habían pasado, y las alertas salían vacías. Se corrieron hacia adelante (nov. 2026 a feb. 2027) manteniendo su orden relativo. Además, el catálogo pasó de 32 a **60 películas** reales: se sumó la plataforma Prime Video, géneros nuevos (Bélico, Western) y 4 fechas de retiro más (9 en total).

## 4. Implementación

`estructuras/heap.py`, hecha a mano, sin `heapq`:

- **Árbol binario completo guardado en una lista.** Para la posición `i`, el padre está en `(i - 1) // 2` y los hijos en `2*i + 1` y `2*i + 2`. No hacen falta nodos ni punteros, como en el BST: la forma del árbol la da la posición en la lista.
- `insertar(x)`: agrega al final y lo hace **subir** (`_subir`), intercambiándolo con su padre mientras sea menor. O(log n).
- `extraer()`: intercambia la raíz con el último, lo saca con `pop()` (O(1)) y hace **bajar** (`_bajar`) la nueva raíz, intercambiándola con el menor de sus hijos. O(log n).
- `ver_tope()`: devuelve `datos[0]` sin sacarlo. O(1).
- **Construcción desde una lista (`_construir`, heapify):** recorre los nodos internos del último al primero y hace bajar a cada uno. Cuesta **O(n)**, no O(n log n): la mayoría de los nodos están cerca de las hojas y bajan muy poco.

## 5. Integración real en la app

- `Catalogo` (`servicios/catalogo.py`): `top_n(n, plataformas=None)` y `proximos_retiros(n, plataformas=None, desde=None)`.
- `Terminal` (`ui/terminal.py`):
  - **opción 9 — Top N**: pide N (ENTER = 5) y muestra el ranking con medallas, filtrado por las plataformas que el usuario cargó al iniciar.
  - **opción 10 — Alertas**: las próximas N películas en salir de sus plataformas, con su fecha.
  - "Salir" pasó de la opción 9 a la 11. Las opciones 1 a 8 no se tocaron.

## 6. Pruebas

- `tests/test_heap.py` (10 tests): heap vacío, un elemento, `ver_tope` no saca el elemento, inserción de a uno, construcción desde una lista de 200 valores mezclados, que no se modifique la lista original, valores repetidos, la prioridad negada como max-heap, y las dos funciones de prioridad con sus desempates.
- `tests/test_catalogo.py` (8 tests nuevos, contra el CSV real): Top 5 exacto con un empate, Top-N igual a "ordenar todo y cortar", filtro por plataforma, N mayor que el catálogo, que el catálogo no se altere, alertas en orden de fecha, que se ignoren las fechas pasadas y el filtro por plataforma en las alertas.
- 61 tests en total en el proyecto, todos pasan (`python -m unittest discover tests`).

## 7. Ejemplo de salida

Usuario con Netflix, opción 9, ENTER (N = 5):

```text
🏆 TOP 5 — Netflix
-------------------------------------------------------
🥇 El Padrino ⭐9.2 [Netflix]
🥈 Pulp Fiction ⭐8.9 [Netflix]
🥉 Forrest Gump ⭐8.8 [Netflix]
4. Buenos Muchachos ⭐8.7 [Netflix]
5. Interestelar ⭐8.7 [Netflix]
```

Buenos Muchachos e Interestelar empatan en 8.7: Buenos Muchachos va primero por el desempate alfabético.

## 8. Por qué un heap y no ordenar todo cada vez

**En teoría:** ordenar todo cuesta O(n log n) y ordena las n películas aunque solo se muestren N. El heap cuesta O(n) para construirse y O(N log n) para extraer las N primeras: O(n + N log n). Con N chico y fijo (5 o 10), eso es prácticamente **O(n)**.

**En la práctica** (`python algoritmos/experimentos/medicion_heap.py`, Top-10, mejor de 3 repeticiones):

| N | `sorted()` de Python (C) | Heap Top-10 (Python) | Ordenar todo con el heap (Python) |
|---:|---:|---:|---:|
| 100 | 0.12 ms | 0.76 ms | 2.6 ms |
| 1.000 | 1.35 ms | 5.6 ms | 44.9 ms |
| 10.000 | 18.0 ms | 61.8 ms | 708.6 ms |
| 100.000 | 234.3 ms | 614.7 ms | 9.882,9 ms |

Lectura honesta de los resultados:

- **Comparación justa (mismo lenguaje y misma estructura):** extraer solo 10 contra extraer las 100.000 da **16 veces menos tiempo**, y la diferencia crece con n. Esto confirma O(n + N log n) contra O(n log n).
- **Contra `sorted()`, el heap pierde.** `sorted()` está escrito en C y nuestro heap en Python puro, así que la diferencia de constantes (unas 3 a 6 veces) le gana a la ventaja asintótica en estos tamaños. Aun así, la brecha **se achica** a medida que crece n (6,2× con 100 películas y 2,6× con 100.000), que es lo que predice el análisis. Es el mismo tema de la pregunta de parcial sobre O(n) contra O(n log n): la complejidad dice cómo **escala** un algoritmo, no cuál gana para un n concreto.
- **Para qué más sirve el heap:** además, es **dinámico**. Agregar una película a un ranking ya armado cuesta O(log n) con `insertar`, mientras que con una lista ordenada habría que reordenar o insertar desplazando elementos (O(n)). Para F6 es la estructura natural: siempre interesa solo "la próxima que se va".

## 9. Complejidad

| Operación | Complejidad |
|---|---|
| `insertar` | O(log n) |
| `extraer` | O(log n) |
| `ver_tope` | O(1) |
| construir desde una lista (heapify) | O(n) |
| `top_n(N)` / `proximos_retiros(N)` | O(n) filtro + O(n) construcción + O(N log n) extracciones = **O(n + N log n)** |
| Alternativa: ordenar todo y cortar | O(n log n) |

## 10. Conclusión

El heap resuelve F3 y F6 con una sola clase genérica: la función de prioridad decide si se comporta como max-heap (puntaje negado) o como min-heap (fecha). Se construye en O(n) con heapify y solo se extraen las N películas que se van a mostrar, en lugar de ordenar el catálogo entero. La medición confirma la ventaja frente a ordenar todo con la misma estructura (16 veces menos con 100.000 películas), y también muestra que el `sorted()` de Python, escrito en C, sigue siendo más rápido en estos tamaños por diferencia de constantes. Con eso quedan integradas al sistema tres familias de estructuras que conviven: los árboles de búsqueda (F1), el árbol general (F2) y el heap (F3 y F6).
