# TP0 — Propuesta de proyecto

**Materia:** Estructuras de Datos
**Integrantes:** Lucho, Zoe, Ian

---

## 1. Nombre del proyecto

**¿Qué Vemos?**

---

## 2. Dominio elegido y justificación

Cine y series disponibles en plataformas de streaming.

Elegimos este dominio porque las películas forman una red de relaciones densa y natural: comparten director, actores, género, época, saga y temática. Esa red es lo que nos permite modelar el catálogo como un grafo real y no como una lista, y hace que preguntas como "¿qué conecta estas dos películas?" tengan sentido dentro del dominio.

Además, la disponibilidad por plataforma agrega una restricción concreta sobre las recomendaciones, lo que obliga a filtrar y priorizar en lugar de simplemente listar.

---

## 3. Problema que resuelve

El usuario paga varias plataformas de streaming pero igual no encuentra qué ver. Sabe qué le gustó en el pasado, pero no sabe cómo llegar desde eso hasta algo nuevo que también pueda mirar sin contratar un servicio más.

¿Qué Vemos? responde dos preguntas:

- **¿Qué veo esta noche, entre lo que ya puedo ver?** Recomendaciones filtradas por las plataformas que el usuario tiene contratadas.
- **¿Cómo llego desde una película que amé hasta otra que no conozco?** El sistema muestra la cadena de películas intermedias que las conecta, explicando el vínculo en cada paso.

---

## 4. Usuario objetivo

**Lucía, 28 años, Buenos Aires.**

Paga Netflix y Max. Llega cansada un jueves a la noche y tiene una hora antes de dormirse. Abre las apps, scrollea quince minutos entre catálogos que se le mezclan, y termina poniendo por tercera vez una serie que ya vio.

Lo que le pasa es doble: no quiere buscar un título específico, quiere que alguien le sugiera algo; y cuando encuentra algo interesante recomendado por un amigo, descubre que está en una plataforma que no tiene.

No es cinéfila ni le interesa serlo. Quiere decidir rápido y no arrepentirse.

---

## 5. Funcionalidades iniciales

| # | Funcionalidad | Descripción |
|---|---|---|
| F1 | Buscar película por título | Búsqueda eficiente sobre el catálogo. Devuelve ficha completa: año, género, director, puntaje y plataformas donde está disponible. |
| F2 | Explorar por categorías | Navegación jerárquica por género y subgénero (ej: Ciencia ficción → Distopía). |
| F3 | Ver Top N | Ranking de mejor puntuadas, con opción de filtrar solo por las plataformas del usuario. |
| F4 | Explorar conexiones | Dada una película, ver las relacionadas y recorrer la red de vínculos (mismo director, actores compartidos, género). |
| F5 | Encontrar camino entre dos películas | Dadas dos películas, mostrar la secuencia de títulos intermedios que las conecta, indicando el vínculo de cada paso. |

**Funcionalidad transversal:** el usuario declara qué plataformas tiene contratadas al iniciar, y eso filtra F3, F4 y F5.

### Estructuras que justifica cada funcionalidad

- F1 → Árbol binario de búsqueda / AVL
- F2 → Árbol general
- F3 → Heap
- F4 → Grafo + BFS / DFS
- F5 → Camino mínimo

### Fuera de alcance (declarado)

- No hay autenticación ni cuentas de usuario.
- Los datos de disponibilidad son un **snapshot manual**, no una consulta en vivo a las plataformas. La disponibilidad real cambia y varía por país.
- No se reproduce contenido: el sistema informa dónde está, no lo abre.

---

## 6. Ejemplo de interacción

```
========================================
             ¿Qué Vemos?
========================================
Tus plataformas: Netflix, Max

  6. Encontrar camino
----------------------------------------
Opción: 6

Película de origen: Matrix
Película de destino: Blade Runner 2049

Buscando conexión...

╔══════════════════════════════════════════════════╗
║  CAMINO ENCONTRADO — 3 pasos                     ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  Matrix (1999)                    [Netflix]      ║
║        │  mismo género: ciberpunk                ║
║        ▼                                         ║
║  Ghost in the Shell (1995)        [Max]          ║
║        │  temática: identidad artificial         ║
║        ▼                                         ║
║  Ex Machina (2014)                [Netflix]      ║
║        │  mismo director: Denis Villeneuve *     ║
║        ▼                                         ║
║  Blade Runner 2049 (2017)         [Max]          ║
║                                                  ║
║  Todas disponibles en tus plataformas.           ║
╚══════════════════════════════════════════════════╝

¿Ver detalle de alguna? (1-4 / 0 volver):
```

> \* Nota para el equipo: revisar este vínculo antes de entregar, el dato de ejemplo es inventado.

---

## 7. Boceto de la interfaz de terminal

```
========================================
             ¿Qué Vemos?
========================================
Tus plataformas: Netflix, Max

  1. Buscar película
  2. Explorar categorías
  3. Ver Top 10
  4. Ver relacionadas
  5. Explorar conexiones
  6. Encontrar camino
  7. Obtener recomendación
  8. Configurar mis plataformas
  0. Salir
----------------------------------------
Opción:
```

---

## 8. Componentes iniciales

```
        Datos (JSON)
             │
             ▼
    Catálogo de películas
             │
   ┌─────────┼─────────┐
   ▼         ▼         ▼
 Árbol      Heap      Grafo
(búsqueda) (ranking) (relaciones)
   └─────────┼─────────┘
             ▼
       Recomendador
             │
             ▼
   Filtro por plataformas
             │
             ▼
    Interfaz de terminal
```

### Clases de dominio previstas

- `Pelicula` — título, año, género, director, elenco, puntaje, duración, plataformas
- `Plataforma` — nombre, catálogo asociado
- `Usuario` — plataformas contratadas, historial
- `Catalogo` — colección de películas y punto de acceso a las estructuras

---

## Pendientes del equipo

- [ ] Confirmar el ángulo del proyecto entre los tres
- [ ] Definir origen del dataset (JSON armado a mano vs. dataset descargado)
- [ ] Definir cuántas películas mínimo para una demo real
- [ ] Definir los criterios de conexión del grafo y el peso de las aristas
- [ ] Crear el repositorio y sumar a los tres como colaboradores
- [ ] Crear el tablero (Trello / GitHub Projects)
