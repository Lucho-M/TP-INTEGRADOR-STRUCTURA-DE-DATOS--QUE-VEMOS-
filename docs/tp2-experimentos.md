# TP2 — Análisis de complejidad: búsqueda secuencial vs. búsqueda binaria

## 1. Operación crítica

La operación elegida es la **búsqueda de una película por título**, ya que es la funcionalidad F1 del proyecto (`docs/TP00-que-vemos.md`) y la que más se repite en el uso normal del sistema.

## 2. Estrategias comparadas

| Estrategia | Método | Descripción |
|---|---|---|
| A · Secuencial | `Catalogo.buscar(texto)` (TP1) | Recorre la lista completa de películas comparando substring, case-insensitive. Coincidencia **parcial**. |
| B · Binaria | `Catalogo.buscar_binaria(titulo)` (TP2, nuevo) | Usa `bisect.bisect_left` sobre una lista de títulos ordenada una sola vez al cargar el catálogo (`_ordenar_por_titulo`). Coincidencia **exacta** (case-insensitive). |

**Diferencia importante:** la búsqueda binaria solo puede resolver coincidencia exacta de forma eficiente (no puede buscar "matr" y encontrar "Matrix" en O(log n), porque el orden alfabético no agrupa substrings). La secuencial sí soporta coincidencia parcial. Es un trade-off real, no una limitación de implementación: se gana velocidad a cambio de flexibilidad de búsqueda.

## 3. Datos de prueba

Datasets sintéticos generados con `datos/generar.py` (semilla fija `random.seed(271)`, reproducibles): `datos/peliculas_100.csv`, `_1000.csv`, `_10000.csv`, `_100000.csv`. Cada fila tiene un título único (`"Pelicula {i}"`), así se puede probar el peor caso pidiendo siempre la **última** película de la lista (la que más tarda en encontrar la búsqueda secuencial).

## 4. Método de medición

Script: `algoritmos/experimentos/medicion.py`. Por cada tamaño N:
1. Se carga el catálogo desde el CSV correspondiente (la carga y el ordenamiento para la binaria quedan **fuera** de la medición, se hacen una sola vez antes de medir).
2. Se mide cada estrategia con `timeit.repeat(lambda: func(titulo), number=20, repeat=5)`, y se toma el **mínimo** de las 5 repeticiones (no el promedio, para evitar que ruido del sistema infle el resultado).
3. El título buscado en ambos casos es el mismo: `"Pelicula {N-1}"` (existe siempre, y es el peor caso para la secuencial).

Reproducir:
```bash
python datos/generar.py
python algoritmos/experimentos/medicion.py
```

## 5. Resultados

| N | Secuencial (ms) | Binaria (ms) |
|---:|---:|---:|
| 100 | 0.0096 | 0.0003 |
| 1.000 | 0.1060 | 0.0004 |
| 10.000 | 1.1789 | 0.0004 |
| 100.000 | 20.3160 | 0.0009 |

*(Medido en la máquina de desarrollo, Python 3.11. Los valores absolutos varían según el equipo; lo relevante es cómo crece cada uno.)*

## 6. Análisis de complejidad

- **Secuencial:** peor caso **O(n)** (recorre toda la lista si el título buscado es el último o no existe), Ω(1) mejor caso (está primero), Θ(n) en promedio. Se ve clarísimo en la tabla: al multiplicar N por 10, el tiempo también se multiplica ~10 veces (0.0096 → 0.1060 → 1.1789 → 20.3160 ms) — crecimiento **lineal**.
- **Binaria:** O(log n) peor caso, Ω(1) mejor caso, Θ(log n). De 100 a 100.000 elementos (mil veces más datos) el tiempo apenas pasa de 0.0003 ms a 0.0009 ms — prácticamente plano, como corresponde a un crecimiento logarítmico (log₂(100.000) ≈ 17 pasos como máximo).
- **Costo de ordenar (no medido arriba):** ordenar la lista para poder usar `bisect` cuesta O(n log n), pero se paga **una sola vez** al cargar el catálogo, no en cada búsqueda. Por eso no se incluye en la medición por-búsqueda: sería como sumarle a la secuencial el tiempo de leer el CSV.

## 7. Conclusión

Para una operación que se repite muchas veces sobre un catálogo que no cambia todo el tiempo (F1: buscar película), la búsqueda binaria es claramente superior a partir de cualquier volumen de datos razonable para el proyecto: con 100.000 elementos, la secuencial tarda ~20 ms y la binaria menos de 0.001 ms, una diferencia de más de 4 órdenes de magnitud. La ventaja se paga con dos costos: (1) hay que mantener la lista ordenada (O(n log n) cada vez que se recarga el catálogo) y (2) se pierde la búsqueda por coincidencia parcial, que sigue siendo útil para el usuario final y por eso se conserva `buscar()` como alternativa.

Esto también anticipa el TP3: un árbol binario de búsqueda (BST) le daría la misma complejidad O(log n) que la búsqueda binaria **pero sin tener que reordenar todo el arreglo** cada vez que se inserta una película nueva (la binaria sobre lista/arreglo requiere reinsertar en la posición correcta, O(n) por inserción) — esa es la justificación real de por qué el TP3 introduce un árbol y no se conforma con lo que ya funciona acá.

## Estructuras y complejidad de las demás operaciones de TP1 (referencia)

| Operación | Complejidad | Notas |
|---|---|---|
| `listar()` | O(n) | Copia la lista completa. |
| `filtrar_por_genero()` / `filtrar_por_plataforma()` | O(n) | Recorren todo el catálogo; no se compararon estrategias alternativas en este TP porque no son la operación elegida. |
