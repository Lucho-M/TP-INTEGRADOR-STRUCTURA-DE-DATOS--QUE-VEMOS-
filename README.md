# ¿Qué Vemos?

Sistema de recomendación de películas según las plataformas de streaming
que el usuario tiene contratadas.

**Materia:** Estructuras de Datos — Grupo N°22, Comisión 2
**Integrantes:** Edgar Mendieta, Zoe Menegazzi

## Estado del proyecto

| TP | Estado | Detalle |
|---|---|---|
| TP0 — Propuesta de proyecto | Entregado | Ver `docs/TP00-que-vemos.md` |
| TP1 — Objetos y clases | Entregado | Modelo, catálogo y terminal funcionando |
| TP2 — Análisis de algoritmos | Entregado | Búsqueda secuencial vs. binaria. Ver `docs/tp2-experimentos.md` |
| TP3 — Árbol binario de búsqueda | Entregado | BST por título. Ver `docs/tp3-arbolbst.md` |
| TP4 — AVL | Entregado | Árbol auto-balanceado con rotaciones. Ver `docs/tp4-avl.md` |
| TP5 — Árbol general (N-ario) | Entregado | Categorías Género → Subgénero. Ver `docs/tp5-arbolgeneral.md` |
| TP6 — Heap (cola de prioridad) | Entregado | Top N por puntaje y alertas de retiro. Ver `docs/tp6-heap.md` |
| TP7 — Grafos | Entregado | Red de películas por director, actor y género. Ver `docs/tp7-grafo.md` |
| TP8 — Recorridos (BFS y DFS) | Entregado | Camino entre dos películas (BFS) y exploración en profundidad (DFS). Ver `docs/tp8-recorridos.md` |
| TP9 — Camino mínimo | No aplica | Quitado por la cátedra. F5 se resuelve con BFS en el TP8 |
| TP10 — Demo Day | Pendiente | Defensa oral del proyecto |

## Estructura del repositorio

| Carpeta | Contenido |
|---|---|
| `modelos/` | Clases de dominio: `Pelicula`, `Usuario`, `Plataforma` |
| `estructuras/` | `ArbolBST` (árbol binario de búsqueda, TP3), `ArbolAVL` (auto-balanceado, TP4), `ArbolCategorias` (árbol general Género→Subgénero, TP5), `Heap` (cola de prioridad genérica, TP6) y `Grafo` (no dirigido y pesado, lista de adyacencia, TP7) |
| `servicios/` | Lógica de negocio: `Catalogo` (carga, búsqueda, listado, filtros, Top N, alertas de retiro, conexiones, camino entre películas y exploración en profundidad) y `red_peliculas` (construcción del grafo) |
| `ui/` | Interfaz de terminal (`Terminal`), sin lógica de negocio |
| `datos/` | Dataset real (`peliculas.csv`) y generador de datasets sintéticos (`generar.py`) |
| `algoritmos/` | Recorridos de grafos: `bfs`, `dfs` y `reconstruir_camino` (TP8) |
| `algoritmos/experimentos/` | Scripts de medición de tiempos (`medicion.py` TP2/TP3, `medicion_avl.py` TP4, `medicion_heap.py` TP6, `medicion_recorridos.py` TP8) |
| `tests/` | Pruebas unitarias (`unittest`) |
| `docs/` | Documentación del proyecto (Parte VII de la consigna) |

## Ejecución

```bash
python main.py
```

## Pruebas

```bash
python -m unittest discover tests
```

## Experimentos de complejidad (TP2-TP4, TP6, TP8)

```bash
python datos/generar.py              # genera los datasets sintéticos (100 a 100.000 películas)
python algoritmos/experimentos/medicion.py       # secuencial vs. binaria vs. árbol BST
python algoritmos/experimentos/medicion_avl.py   # BST vs. AVL insertando datos ya ordenados (peor caso)
python algoritmos/experimentos/medicion_heap.py  # Top-N con heap vs. ordenar todo el catálogo
python algoritmos/experimentos/medicion_recorridos.py  # BFS y DFS sobre grafos de 1.000 a 100.000 vértices
```
Resultados y análisis completo en [`docs/tp2-experimentos.md`](docs/tp2-experimentos.md) (secuencial vs. binaria), [`docs/tp3-arbolbst.md`](docs/tp3-arbolbst.md) (se suma el árbol BST), [`docs/tp4-avl.md`](docs/tp4-avl.md) (BST vs. AVL en el peor caso), [`docs/tp6-heap.md`](docs/tp6-heap.md) (heap vs. ordenar todo) y [`docs/tp8-recorridos.md`](docs/tp8-recorridos.md) (BFS y DFS, O(V + E)).

El TP5 (árbol general de categorías) no tiene script de medición propio: resuelve una navegación jerárquica (F2), no una comparación de estrategias de búsqueda. Ver análisis en [`docs/tp5-arbolgeneral.md`](docs/tp5-arbolgeneral.md).

El TP7 (grafo) tampoco tiene script de medición: la comparación es entre representaciones (lista vs. matriz de adyacencia según la densidad), y está analizada en [`docs/tp7-grafo.md`](docs/tp7-grafo.md).