# TP4 — Árbol AVL

## 1. Por qué un AVL acá

El TP3 (`docs/tp3-arbolbst.md`, secciones 6-7) ya dejó planteado el problema: el `ArbolBST` resuelve la búsqueda por título en O(log n) **en el caso típico**, pero esa garantía depende del orden en que entran los títulos. Con el dataset sintético de 100.000 elementos la altura terminó en 50 en lugar de los ~17 ideales. Un BST común no tiene ningún mecanismo para corregir eso: si los datos entran en un orden desfavorable (por ejemplo, ya ordenados alfabéticamente), degenera hasta parecerse a una lista enlazada.

El AVL es la misma idea de árbol binario de búsqueda, pero con una regla extra: después de cada inserción, se verifica que ningún nodo quede con sus dos subárboles demasiado desparejos, y si eso pasa, se reacomoda con una rotación. Esto garantiza que la altura sea siempre O(log n), **sin importar el orden de inserción**.

## 2. El factor de balance

Cada nodo AVL (`NodoAVL`, en `estructuras/avl.py`) guarda su propia **altura** (`self.altura`), además de clave, lista de películas e hijos — igual que `NodoArbol` del TP3, con ese único campo extra. Guardarla en el nodo (en vez de recalcularla recorriendo el subárbol cada vez) es necesario para que el chequeo de balance siga siendo O(1): si hubiera que recorrer todo el subárbol para saber su altura, cada inserción pasaría de O(log n) a O(n) y se perdería toda la ventaja de balancear.

El **factor de balance** de un nodo es `altura(subárbol izquierdo) − altura(subárbol derecho)`. Mientras esté en `-1`, `0` o `1`, el nodo está bien. Si después de insertar queda en `-2` o `+2`, hay que rotar.

## 3. Las cuatro rotaciones

`ArbolAVL._rebalancear` distingue cuatro casos, comparando el factor de balance del nodo con la clave recién insertada:

| Caso | Condición | Qué hace |
|---|---|---|
| Izquierda-Izquierda (LL) | balance > 1, la clave entró por la izquierda del hijo izquierdo | una rotación simple a la derecha |
| Derecha-Derecha (RR) | balance < -1, la clave entró por la derecha del hijo derecho | una rotación simple a la izquierda (espejo de la anterior) |
| Izquierda-Derecha (LR) | balance > 1, pero la clave entró por la derecha del hijo izquierdo | rotación izquierda sobre el hijo izquierdo, y después rotación derecha sobre el nodo (doble) |
| Derecha-Izquierda (RL) | balance < -1, pero la clave entró por la izquierda del hijo derecho | rotación derecha sobre el hijo derecho, y después rotación izquierda sobre el nodo (doble) |

Las rotaciones simples (`_rotacion_derecha`, `_rotacion_izquierda`) son O(1): solo reacomodan 3 referencias y recalculan la altura de los 2 nodos involucrados, no tocan el resto del árbol. Los casos dobles son simplemente dos rotaciones simples encadenadas.

## 4. Qué se mantiene igual que el BST del TP3

A propósito, `ArbolAVL` tiene la misma clave de ordenamiento (título normalizado, `normalizar_titulo` de `estructuras/arbol.py`, reutilizada sin duplicar código), la misma forma de manejar remakes/títulos repetidos (lista de películas por nodo) y la misma interfaz pública (`insertar`, `buscar`, los tres recorridos, `altura`). Esto es intencional: permite comparar ambas estructuras con el mismo dataset y el mismo código de medición, cambiando solo qué clase se instancia.

Integración a la UI: la consigna del TP4 pide "código AVL, experimentos de desbalance, comparación, conclusión técnica" — no pide reemplazar la búsqueda del menú (eso ya lo resuelve la opción 6 con el BST desde el TP3). Por ahora el AVL se valida con tests y con el script de experimentos; si más adelante conviene usarlo en vez del BST para alguna funcionalidad (por ejemplo si el dataset real crece y el orden de carga del CSV resulta desfavorable), es un cambio de una línea en `servicios/catalogo.py` gracias a que la interfaz es idéntica.

## 5. Pruebas

`tests/test_avl.py`:
- Mismos casos funcionales que `test_arbol.py` (búsqueda exacta, sin coincidencia, remakes, recorrido inorder, árbol vacío) para confirmar que el AVL se comporta igual que el BST de cara al resto del sistema.
- Casos mínimos de las 4 rotaciones (LL, RR, LR, RL), insertando 3 títulos de una letra cada uno y verificando que la raíz y los hijos queden donde corresponde.
- Un test que inserta 20 títulos ya ordenados ("a".."t") en un `ArbolBST` y en un `ArbolAVL` en paralelo y confirma que el BST degenera (altura == 20, igual a la cantidad de nodos) mientras el AVL se mantiene en 6 niveles o menos.

29 tests en total en el proyecto (19 del TP0-TP3 + 10 nuevos), todos verdes (`python -m unittest discover tests`).

## 6. Comparación de estrategias: BST vs AVL en el peor caso

`algoritmos/experimentos/medicion_avl.py` genera títulos **ya ordenados alfabéticamente** (a diferencia de `datos/generar.py`, que los deja en orden de carga) — es el peor caso posible para un BST sin balanceo, porque cada título nuevo es siempre mayor que el anterior y el árbol crece en línea recta hacia la derecha.

| N | Altura BST | Altura AVL | log₂(N) ideal | Búsqueda BST (ms) | Búsqueda AVL (ms) |
|---:|---:|---:|---:|---:|---:|
| 10 | 10 | 4 | 3.3 | 0.0017 | 0.0014 |
| 50 | 50 | 6 | 5.6 | 0.0044 | 0.0015 |
| 100 | 100 | 7 | 6.6 | 0.0077 | 0.0016 |
| 500 | 500 | 9 | 9.0 | 0.0739 | 0.0018 |
| 1.000 | **RecursionError** | 10 | 10.0 | N/A | 0.0019 |
| 10.000 | **RecursionError** | 14 | 13.3 | N/A | 0.0022 |
| 100.000 | **RecursionError** | 17 | 16.6 | N/A | 0.0031 |

**Hallazgo clave:** con datos ya ordenados, la altura del BST es exactamente igual a la cantidad de elementos (10, 50, 100, 500) — se convirtió en una lista enlazada disfrazada de árbol. A partir de N=1.000, insertar de forma recursiva en ese BST degenerado choca contra el límite de recursión de Python (`sys.getrecursionlimit()`, 1000 por defecto) y el programa **ni siquiera termina de cargar los datos**: no es un error del experimento, es la demostración más concreta posible de qué significa "O(n) en el peor caso" en la práctica.

El AVL, en cambio, mantiene la altura pegada al ideal teórico `log₂(n)` en todos los tamaños, sin importar que los datos vengan en el peor orden posible. La búsqueda se mantiene en milisegundos prácticamente constantes incluso con 100.000 elementos.

## 7. Análisis de complejidad

- **Inserción en AVL:** O(log n) **siempre** (mejor, promedio y peor caso), porque la altura nunca supera ~1.44 · log₂(n) gracias a las rotaciones. Cada inserción hace, como mucho, una rotación simple o doble (O(1)) por cada nivel que recorre hacia atrás.
- **Búsqueda en AVL:** O(log n) siempre, por la misma razón.
- **Inserción/búsqueda en BST común:** O(log n) en el caso promedio, pero **O(n) en el peor caso** (datos que llegan en un orden que degenera el árbol) — y como mostró la tabla, ese peor caso no es solo lento: en Python, con recursión, directamente puede no completarse.
- El costo que paga el AVL por esta garantía es la verificación de balance y las rotaciones en cada inserción — trabajo extra O(1) por nivel, insignificante frente a lo que evita.

## 8. Conclusión

El TP3 dejó planteada la pregunta ("¿qué pasa si el BST pierde el equilibrio?") y este TP4 la responde con un experimento que lo muestra en su forma más extrema: un BST al que se le insertan datos ya ordenados no solo pierde su ventaja de O(log n), sino que puede fallar directamente por límite de recursión antes de los 1.000 elementos. El AVL resuelve esto balanceando el árbol después de cada inserción con rotaciones O(1), manteniendo la altura pegada al ideal teórico en cualquier escenario. La contrapartida es algo de trabajo extra en cada inserción, pero es una garantía que vale la pena pagar: para este proyecto, donde el catálogo puede crecer con películas cargadas en cualquier orden (por ejemplo, alfabético si se importa un dataset ya ordenado), el AVL es la opción más robusta frente al BST simple del TP3.
