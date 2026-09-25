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

## Estructura del repositorio

| Carpeta | Contenido |
|---|---|
| `modelos/` | Clases de dominio: `Pelicula`, `Usuario`, `Plataforma` |
| `servicios/` | Lógica de negocio: `Catalogo` (carga, búsqueda, listado, filtros) |
| `ui/` | Interfaz de terminal (`Terminal`), sin lógica de negocio |
| `datos/` | Dataset real (`peliculas.csv`) y generador de datasets sintéticos (`generar.py`) |
| `algoritmos/experimentos/` | Script de medición de tiempos (`medicion.py`, TP2) |
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

## Experimentos de complejidad (TP2)

```bash
python datos/generar.py              # genera los datasets sintéticos (100 a 100.000 películas)
python algoritmos/experimentos/medicion.py   # mide y compara ambas estrategias de búsqueda
```
Resultados y análisis completo en [`docs/tp2-experimentos.md`](docs/tp2-experimentos.md).