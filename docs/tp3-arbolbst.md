# TP3 — Árbol Binario de Búsqueda (BST)

## 1. Por qué un árbol acá

F1 del proyecto (`docs/TP00-que-vemos.md`) es "Buscar película por título", y en el TP0 ya estaba justificado con "Árbol binario de búsqueda / AVL". En el TP2 resolvimos esa misma búsqueda con una lista ordenada + `bisect` (O(log n), pero insertar en el medio de un arreglo ordenado cuesta O(n) porque hay que correr elementos). El árbol da la misma complejidad de búsqueda **sin pagar ese costo de reordenar todo el arreglo cada vez que entra una película nueva al catálogo**: insertar en un BST es, en el caso típico, O(log n).

## 2. Clave de ordenamiento

Se usa el **título normalizado**: minúscula y sin tildes (`estructuras/arbol.py::normalizar_titulo`, con `unicodedata`). Esto resuelve el punto pendiente que había quedado anotado desde el TP0 ("¿clave natural: título normalizado?") y evita que "Interestelar" y "interestelar" (o una tilde mal tipeada) terminen en nodos distintos.

**Decisión sobre remakes / títulos repetidos** (otro punto pendiente del TP0): cada nodo (`NodoArbol`) guarda una **lista** de películas, no una sola. Si dos películas normalizan a la misma clave (ej. un remake con el mismo título), ambas conviven en el mismo nodo en vez de que la segunda pise a la primera o se pierda.

## 3. Implementación

`estructuras/arbol.py`:
- `NodoArbol`: `clave`, `peliculas` (lista), `izq`, `der`.
- `ArbolBST.insertar(pelicula)`: recorre comparando la clave contra cada nodo; si es menor va a la izquierda, si es mayor a la derecha, si es igual se agrega a la lista del nodo existente.
- `ArbolBST.buscar(titulo)`: búsqueda **exacta** (no parcial, misma limitación ya discutida en el TP2 para la binaria). Devuelve la lista de coincidencias o `[]`.
- Recorridos: `recorrido_inorder` (izq, nodo, der — da las películas ordenadas alfabéticamente), `recorrido_preorder` (nodo, izq, der) y `recorrido_postorder` (izq, der, nodo), los tres implementados de forma recursiva.
- `altura()`: cuenta los niveles del árbol (se usa para medir qué tan balanceado quedó — ver sección 6).

## 4. Integración real en la app (no es un árbol aislado)

Se agregaron dos funcionalidades nuevas al menú de `ui/terminal.py`, además de las del TP1/TP2 (que se conservan sin tocar):
- **Opción 6 — Buscar por título exacto (árbol BST):** usa `Catalogo.buscar_arbol()`.
- **Opción 7 — Listar ordenado alfabéticamente:** usa `Catalogo.listar_ordenado_por_titulo()` (recorrido inorder) — es la demostración concreta de para qué sirve el recorrido inorder en este dominio: obtener el catálogo ordenado sin tener que ordenarlo de nuevo cada vez.

El árbol se construye una sola vez, al cargar el CSV (`Catalogo.cargar_desde_csv` inserta cada película también en el árbol, además de en la lista del TP1).

## 5. Pruebas

- `tests/test_arbol.py`: `normalizar_titulo`, inserción, búsqueda exacta (con y sin coincidencia), títulos repetidos en el mismo nodo, los 3 recorridos, árbol vacío.
- `tests/test_catalogo.py`: integración (`buscar_arbol`, `listar_ordenado_por_titulo`) contra el dataset real.
- 19 tests en total en el proyecto, todos verdes (`python -m unittest discover tests`).

## 6. Comparación de estrategias (secuencial vs. binaria vs. árbol)

Mismo método que en el TP2: `algoritmos/experimentos/medicion.py`, datasets sintéticos de `datos/generar.py`, `timeit` con mínimo de 5 repeticiones, buscando siempre `"Pelicula {N-1}"`.

| N | Secuencial (ms) | Binaria (ms) | Árbol BST (ms) | Altura del árbol |
|---:|---:|---:|---:|---:|
| 100 | 0.0095 | 0.0003 | 0.0025 | 20 |
| 1.000 | 0.0944 | 0.0004 | 0.0032 | 30 |
| 10.000 | 1.0013 | 0.0004 | 0.0040 | 40 |
| 100.000 | 15.3702 | 0.0005 | 0.0046 | 50 |

**Hallazgo importante — el árbol no quedó perfectamente balanceado:** con 100.000 elementos, la altura ideal de un árbol balanceado sería `log₂(100.000) ≈ 17`. La altura real que midió el programa es **50**, casi 3 veces más. Esto pasa porque los títulos sintéticos (`"Pelicula 0"`, `"Pelicula 1"`, ...) se insertan en un orden que, al compararlos como texto, no cae parejo para ambos lados del árbol — el BST "normal" (sin balanceo) es sensible al **orden de inserción**. Aun así, la búsqueda en el árbol sigue siendo muchísimo más rápida que la secuencial (0.0046 ms vs. 15.37 ms con 100.000 elementos), porque 50 pasos en el peor caso sigue siendo enormemente mejor que recorrer 100.000 elementos uno por uno.

## 7. Análisis de complejidad

- **Inserción:** O(log n) en el caso típico (árbol razonablemente balanceado); O(n) en el peor caso (si las claves llegan en un orden que degenera el árbol en algo parecido a una lista — ver el hallazgo de arriba).
- **Búsqueda:** misma lógica que la inserción — O(log n) típico, O(n) en el peor caso de desbalance.
- **Recorridos (inorder/preorder/postorder):** O(n) siempre, porque visitan cada nodo una vez.
- Esto es **exactamente** el problema que plantea la Guía/TP4: "qué pasa cuando un árbol pierde el equilibrio". Ya lo estamos viendo acá con datos sintéticos, no hace falta esperar al TP4 para notarlo — este resultado es la motivación concreta para implementar el AVL (que garantiza altura O(log n) siempre, rotando cuando hace falta).

## 8. Conclusión

El árbol BST resuelve la búsqueda por título con la misma complejidad teórica que la búsqueda binaria del TP2, pero sin el costo de reordenar un arreglo al insertar. Es la primera estructura "real" (no un array con una función auxiliar) del proyecto. Sin embargo, el experimento mostró su punto débil: un BST sin balanceo depende del orden de inserción de los datos, y con este dataset sintético la altura terminó siendo ~3 veces la ideal. Mantenemos la binaria del TP2 porque sigue siendo más rápida en este caso puntual (su "desbalance" no existe porque trabaja sobre un arreglo siempre ordenado), pero el árbol tiene la ventaja de permitir inserciones sin recalcular todo. El TP4 (AVL) va a resolver justamente la debilidad que encontramos acá.
