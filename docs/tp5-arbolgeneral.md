# TP5 — Árbol General (N-ario)

## 1. Por qué un árbol general acá

F2 del proyecto (`docs/TP00-que-vemos.md`) es "Explorar por categorías": navegación jerárquica por género y subgénero (ej: Ciencia ficción → Distopía). Esto es distinto de lo que resolvieron el BST (TP3) y el AVL (TP4): ahí cada nodo tenía como máximo 2 hijos, elegidos comparando una clave de orden. Acá no hay "menor o mayor": un género puede tener cualquier cantidad de subgéneros, y el lugar de cada uno lo da el dominio (la categoría a la que pertenece), no una comparación. Esa es exactamente la definición de **árbol general (N-ario)**.

## 2. Decisiones de diseño (quedaban pendientes desde el TP0)

El TP0 (`docs/TP00-que-vemos.md`, sección 1.1) dejó anotada la pregunta: *"F2 dice Género → Subgénero. ¿Una película puede estar en más de un subgénero?"*. Se resolvió revisando el dataset real (`datos/peliculas.csv`):

**Hallazgo:** cada película tiene un único par (género, subgénero) — no hay casos de múltiples subgéneros en los datos actuales. Pero el mismo *nombre* de subgénero se repite bajo géneros distintos: `"Epica"` aparece bajo Acción, Ciencia ficción y Fantasía; `"Superheroes"` bajo Acción y Animación; `"Thriller"` bajo Ciencia ficción, Crimen y Drama.

Dos decisiones, a partir de ese hallazgo:

1. **Cada subgénero es un nodo propio, colgado de su género padre — no un nodo compartido entre géneros.** "Épica" bajo Acción y "Épica" bajo Ciencia ficción son dos `NodoGeneral` distintos, cada uno con sus propias películas. La alternativa (un único nodo "Épica" al que apuntan varios géneros) deja de ser un árbol: un nodo con más de un padre es un **grafo**, otra estructura que se aborda recién en el TP7. Mantener esto como árbol es consistente con el alcance de la etapa.
2. **Una película cuelga de un solo subgénero.** Coincide con el dataset real y mantiene el diseño simple: cada `NodoGeneral` guarda una lista de películas (igual patrón que `NodoArbol`/`NodoAVL` para remakes en TP3/TP4), pero solo las hojas (nodos subgénero) la usan en la práctica. Si una película no tiene subgénero cargado, queda directamente en el nodo de su género.

## 3. Implementación

`estructuras/arbol_general.py`:
- `NodoGeneral`: `nombre`, `hijos` (lista, no 2 referencias fijas como en un árbol binario), `peliculas` (lista, igual patrón que TP3/TP4). `buscar_hijo(nombre)` recorre los hijos directos comparando con `normalizar_titulo` (reutilizada de `estructuras/arbol.py`, sin duplicar lógica) — case-insensitive y sin tildes, igual criterio que el resto del proyecto.
- `ArbolCategorias`: la raíz es un nodo `"Catalogo"` artificial; sus hijos son los géneros, y los hijos de cada género son sus subgéneros.
  - `insertar(pelicula)`: busca o crea el nodo género, después busca o crea el nodo subgénero colgado de ESE género puntual, y agrega la película a la lista del nodo hoja correspondiente.
  - `generos()` / `subgeneros(genero)`: nombres de los hijos directos de la raíz / de un género.
  - `peliculas_de_genero(genero)`: recolecta recursivamente todas las películas del subárbol completo de ese género (todos sus subgéneros).
  - `peliculas_de_subgenero(genero, subgenero)`: busca el camino género → subgénero y devuelve solo las películas de esa hoja puntual.
  - `recorrido_preorder()`: nodo, después sus hijos de izquierda a derecha — el recorrido natural de un árbol N-ario (no hay inorder con más de 2 hijos, ese concepto es específico de árboles binarios).
  - `altura()`: para este dataset es fija en 3 niveles (Catálogo → Género → Subgénero), pero se calculó de forma genérica (recorriendo hijos) para que siga funcionando si se agrega un nivel más de jerarquía en el futuro.

## 4. Integración real en la app

- `Catalogo` (`servicios/catalogo.py`) construye un `ArbolCategorias` al cargar el CSV, insertando cada película además de en la lista (TP1), el árbol BST (TP3) y el AVL. Expone `listar_generos()`, `listar_subgeneros()`, `explorar_genero()`, `explorar_subgenero()`.
- `Terminal` (`ui/terminal.py`): nueva **opción 8 — Explorar categorías**, que lista géneros, permite elegir uno, muestra sus subgéneros (con la opción de ver todas las películas del género sin filtrar por subgénero) y finalmente lista las películas. "Salir" pasó de la opción 8 a la 9; las opciones 1-7 no se tocaron.

## 5. Pruebas

- `tests/test_arbol_general.py` (10 tests): géneros de primer nivel, subgéneros de un género, el caso clave del diseño (mismo nombre de subgénero bajo géneros distintos no se mezcla), recolección recursiva por género, género/subgénero inexistente, película sin subgénero, recorrido preorder, altura, árbol vacío.
- `tests/test_catalogo.py`: 4 tests de integración nuevos (`listar_generos`, `listar_subgeneros`, `explorar_genero`, `explorar_subgenero`) contra el dataset real.
- 43 tests en total en el proyecto, todos pasan (`python -m unittest discover tests`).

## 6. Ejemplo de recorrido

Con el dataset real, `recorrido_preorder()` visita: `Catalogo` → cada género (en el orden en que aparece por primera vez en el CSV) → los subgéneros de cada uno. Por ejemplo, para el género "Acción": `Catalogo, Drama, ..., Accion, Epica, Superheroes, ...`. Sirve para depurar la forma del árbol o, a futuro, para listar la jerarquía completa de categorías en un solo recorrido en vez de pedir género por género.

## 7. Complejidad

- **Insertar una película:** O(g + s) para buscar/crear el nodo género y el nodo subgénero, donde *g* es la cantidad de géneros y *s* la cantidad de subgéneros de ese género — en la práctica, ambos números son chicos y fijos (no crecen con la cantidad de películas), así que es efectivamente O(1) por película.
- **Listar géneros/subgéneros:** O(1) y O(hijos directos) respectivamente, no se recorre el catálogo completo.
- **`peliculas_de_genero`:** O(tamaño del subárbol de ese género) — solo recorre las películas de ESE género, no las 32 (o 100.000) del catálogo completo.
- No se mide esta etapa contra las anteriores (TP2-TP4 comparan estrategias de búsqueda por título): el árbol general resuelve un problema distinto (navegación jerárquica, F2), no hay una "alternativa lenta" previa con la que compararlo en este proyecto.

## 8. Conclusión

El árbol general modela F2 ("Explorar por categorías") con la misma idea de fondo que el BST/AVL — nodos con hijos, recorridos recursivos — pero sin clave de orden ni límite de 2 hijos, porque la jerarquía Género→Subgénero no es comparable, es de pertenencia. La decisión de diseño más importante fue tratar cada subgénero como un nodo distinto por cada género padre (en vez de un nodo compartido): mantiene la estructura como árbol real, a costa de "duplicar" nombres como "Épica" en distintas ramas — una limitación aceptada a propósito para no adelantar el grafo del TP7.
