# ¿Qué Vemos?

Sistema de recomendación de películas según las plataformas de streaming
que el usuario tiene contratadas.

**Materia:** Estructuras de Datos — Grupo N°22, Comisión 2
**Integrantes:** Edgar Mendieta, Zoe Menegazzi

## Estado del proyecto

| TP | Estado |
|---|---|
| TP0 — Propuesta de proyecto | ✅ Ver `docs/TP00-que-vemos.md` |
| TP1 — Objetos y clases | ✅ Modelo, catálogo y terminal funcionando |
| TP2 — Análisis de algoritmos | ✅ Búsqueda secuencial vs. binaria. Ver `docs/tp2-experimentos.md` |
| TP3 — Árbol binario de búsqueda | ✅ BST por título. Ver `docs/tp3-arbolbst.md` |
| TP4 — AVL | ✅ Árbol auto-balanceado con rotaciones. Ver `docs/tp4-avl.md` |

## Estructura del repositorio

| Carpeta | Contenido |
|---|---|
| `modelos/` | Clases de dominio: `Pelicula`, `Usuario`, `Plataforma` |
| `estructuras/` | `ArbolBST` (árbol binario de búsqueda, TP3) y `ArbolAVL` (auto-balanceado, TP4) |
| `servicios/` | Lógica de negocio: `Catalogo` (carga, búsqueda, listado, filtros) |
| `ui/` | Interfaz de terminal (`Terminal`), sin lógica de negocio |
| `datos/` | Dataset real (`peliculas.csv`) y generador de datasets sintéticos (`generar.py`) |
| `algoritmos/experimentos/` | Scripts de medición de tiempos (`medicion.py` TP2/TP3, `medicion_avl.py` TP4) |
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

## Experimentos de complejidad (TP2-TP4)

```bash
python datos/generar.py              # genera los datasets sintéticos (100 a 100.000 películas)
python algoritmos/experimentos/medicion.py       # secuencial vs. binaria vs. árbol BST
python algoritmos/experimentos/medicion_avl.py   # BST vs. AVL insertando datos ya ordenados (peor caso)
```
Resultados y análisis completo en [`docs/tp2-experimentos.md`](docs/tp2-experimentos.md) (secuencial vs. binaria), [`docs/tp3-arbolbst.md`](docs/tp3-arbolbst.md) (se suma el árbol BST) y [`docs/tp4-avl.md`](docs/tp4-avl.md) (BST vs. AVL en el peor caso).