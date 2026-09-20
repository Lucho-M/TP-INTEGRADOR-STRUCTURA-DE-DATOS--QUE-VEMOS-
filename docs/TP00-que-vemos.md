# TP00

**Materia:** Estructuras de Datos Comision 2 — Grupo N°22
**Integrantes:** Edgar Mendieta DNI:43583371, Zoe Menegazzi DNI:44958150, Ian Robledo
---

## 1. Nombre del proyecto

**¿Qué Vemos?**

---

## 2. Dominio elegido y justificación

Películas disponibles en plataformas de streaming.

Elegimos este dominio porque las películas comparten director, actores, género, época, saga y temática. Esas relaciones nos permiten modelar el catálogo como un grafo real y hacer preguntas como "¿qué conecta estas dos películas?" que tienen sentido dentro del dominio.

Además, la disponibilidad por plataforma agrega una restricción concreta sobre las recomendaciones, lo que obliga a filtrar y priorizar en lugar de simplemente listar.

---

## 3. Problema que resuelve

El usuario paga varias plataformas de streaming pero igual no encuentra qué ver. Sabe qué le gustó en el pasado, pero no sabe cómo llegar desde eso hasta algo nuevo que también pueda mirar sin contratar un servicio más.

**¿Qué Vemos?** responde tres preguntas:

- **¿Qué veo esta noche, entre lo que ya puedo ver?** Recomendaciones filtradas por las plataformas que el usuario tiene contratadas.
- **¿Cómo llego desde una película que me gustó hasta otra que no conozco?** El sistema muestra la cadena de películas intermedias que las conecta, explicando el vínculo en cada paso.
- **¿Qué se me está por escapar?** Aviso de las películas que salen pronto del catálogo, ordenadas por urgencia.

---

## 4. Usuario objetivo

**Lucho, 28 años, Buenos Aires.**

Paga Netflix, HBO Max y Disney+. Llega cansado un jueves a la noche y tiene una hora antes de dormirse. Abre las apps, scrollea quince minutos entre catálogos que se le mezclan, y termina poniendo por tercera vez una serie que ya vio.

Lo que le pasa es doble: no quiere buscar un título específico, quiere que alguien le sugiera algo; y cuando encuentra algo interesante recomendado por un amigo, descubre que está en una plataforma que no tiene.

No es cinéfilo ni le interesa serlo. Quiere decidir rápido y no arrepentirse.

---

## 5. Funcionalidades iniciales

| # | Funcionalidad | Descripción |
|---|---|---|
| F1 | Buscar película por título | Búsqueda eficiente sobre el catálogo. Devuelve ficha completa: año, género, director, puntaje y plataformas donde está disponible. |
| F2 | Explorar por categorías | Navegación jerárquica por género y subgénero (ej: Ciencia ficción → Distopía). |
| F3 | Ver Top N | Ranking de mejor puntuadas, con opción de filtrar solo por las plataformas del usuario. |
| F4 | Explorar conexiones | Dada una película, ver las relacionadas y recorrer la red de vínculos (mismo director, actores compartidos, género). |
| F5 | Encontrar camino entre dos películas | Dadas dos películas, mostrar la secuencia de títulos intermedios que las conecta, indicando el vínculo de cada paso. |
| F6 | Alertas de salida de catálogo | Listado de películas próximas a ser retiradas, ordenadas por cercanía de la fecha. Permite priorizar qué ver antes de que deje de estar disponible. |

**Funcionalidad transversal:** el usuario declara qué plataformas tiene contratadas al iniciar, y eso filtra F3, F4, F5 y F6.

### Estructuras que justifica cada funcionalidad

- F1 → Árbol binario de búsqueda / AVL
- F2 → Árbol general
- F3 → Heap
- F4 → Grafo + recorridos BFS / DFS
- F5 → Camino mínimo sobre el grafo
- F6 → Heap (cola de prioridad por fecha de retiro)

### Fuera de alcance (declarado)

- **Solo películas.** Las series quedan fuera de esta versión: sus temporadas y episodios exigen otro modelo de relaciones. Es una ampliación posible, no un objetivo actual.
- **Sin autenticación ni cuentas de usuario.**
- **Los datos son un snapshot manual**, no una consulta en vivo a las plataformas. La disponibilidad real cambia y varía por país.
- **La fecha de retiro es un dato simulado**, cargado por el equipo en el dataset. No proviene de las plataformas: sirve para demostrar el funcionamiento de la cola de prioridad.
- **No se reproduce contenido:** el sistema informa dónde está, no lo abre.

---

## 6. Ejemplo de interacción

```
========================================
             ¿Qué Vemos?
========================================
Tus plataformas: Netflix, HBO Max, Disney+

  5. Encontrar camino
----------------------------------------
Opción: 5

Película de origen: El Hombre Araña
Película de destino: El Caballero de la Noche

Buscando conexión...

╔══════════════════════════════════════════════════╗
║  CAMINO ENCONTRADO — 3 pasos                     ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  El Hombre Araña (2002)           [Netflix]      ║
║        │  mismo género: superhéroes              ║
║        ▼                                         ║
║  Los Increíbles (2004)            [Disney+]      ║
║        │  temática: identidad secreta            ║
║        ▼                                         ║
║  Batman Inicia (2005)             [HBO Max]      ║
║        │  mismo director: Christopher Nolan      ║
║        ▼                                         ║
║  El Caballero de la Noche (2008)  [HBO Max]      ║
║                                                  ║
║  Todas disponibles en tus plataformas.           ║
╚══════════════════════════════════════════════════╝

¿Ver detalle de alguna? (1-4 / 0 volver):
```

Segundo ejemplo, alertas de salida:

```
  7. Salen pronto del catálogo
----------------------------------------
Opción: 7

  URGENTE (menos de 7 días)
   • Ciudad de Dios (2002)        [Netflix]   sale en 3 días
   • Perfume de Mujer (1992)      [HBO Max]   sale en 6 días

  ESTE MES
   • El Gran Pez (2003)           [Disney+]   sale en 18 días
   • Zodíaco (2007)               [Netflix]   sale en 24 días

¿Ver detalle de alguna? (1-4 / 0 volver):
```

---

## 7. Boceto de la interfaz de terminal

```
========================================
             ¿Qué Vemos?
========================================
Tus plataformas: Netflix, HBO Max, Disney+

  1. Buscar película
  2. Explorar categorías
  3. Ver Top 10
  4. Explorar conexiones
  5. Encontrar camino
  6. Obtener recomendación
  7. Salen pronto del catálogo
  8. Configurar mis plataformas
  0. Salir
----------------------------------------
Opción:
```

---

## 8. Componentes iniciales

```
        Datos (CSV)
             │
             ▼
    Catálogo de películas
             │
   ┌─────────┼─────────┐
   ▼         ▼         ▼
 Árbol      Heap      Grafo
(búsqueda) (ranking) (relaciones)
            (retiro)
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

- `Pelicula` — título, año, género, director, elenco, puntaje, duración, plataformas, fecha de retiro
- `Plataforma` — nombre, catálogo asociado
- `Usuario` — plataformas contratadas, historial
- `Catalogo` — colección de películas y punto de acceso a las estructuras

---

## Estado del equipo

| Definición | Estado |
|---|---|
| Ángulo del proyecto | Confirmado por los tres |
| Origen del dataset | CSV cargado por el equipo |
| Tamaño mínimo de la demo | 50 películas |
| Repositorio | Creado, tres colaboradores |
| Tablero de gestión | Trello o Notion, a definir |
| Criterios de conexión y peso de las aristas del grafo | **Pendiente** |

El punto abierto es el peso de las aristas: qué tanto "cuesta" pasar de una película a otra según el tipo de vínculo (mismo director, actor compartido, mismo género). Es la decisión que condiciona el comportamiento del camino mínimo y la queremos resolver antes de avanzar con la implementación del grafo.
