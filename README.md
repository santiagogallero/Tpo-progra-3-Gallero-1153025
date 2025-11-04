# TP Algoritmos - Trabajo Práctico Integrador

**Programación 3 - UADE**

Este proyecto implementa soluciones a cuatro problemas clásicos de algoritmia utilizando diferentes paradigmas de programación.

## 📋 Contenido

1. **Divide & Conquer**: Par de puntos más cercanos
2. **Greedy**: Selección de actividades
3. **Programación Dinámica**: Mochila 0/1
4. **Grafos**: Floyd-Warshall

## 🚀 Requisitos

- Python 3.10+
- pip (gestor de paquetes)

## 📦 Instalación

### 1. Clonar el repositorio

```bash
cd "Tpo progra 3"
```

### 2. Crear entorno virtual

```bash
python3 -m venv .venv
```

### 3. Activar entorno virtual

**En macOS/Linux:**
```bash
source .venv/bin/activate
```

**En Windows:**
```bash
.venv\Scripts\activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🎯 Uso

### Ejecutar el programa principal

```bash
python -m src.tp_algos.main
```

El programa muestra un menú interactivo donde puedes elegir qué demostración ejecutar:

```
1. Parte 1: Par de puntos más cercanos (Divide & Conquer)
2. Parte 2: Selección de actividades (Greedy)
3. Parte 3: Mochila 0/1 (Programación Dinámica)
4. Parte 4: Floyd-Warshall (Grafos)
5. Ejecutar todas las demostraciones
0. Salir
```

### Ejecutar tests

```bash
# Todos los tests
pytest tests/ -v

# Tests específicos
pytest tests/test_closest_pair.py -v
pytest tests/test_interval_scheduling.py -v
pytest tests/test_knapsack.py -v
pytest tests/test_floyd_warshall.py -v
```

## 📁 Estructura del Proyecto

```
.
├── README.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── src/
│   └── tp_algos/
│       ├── __init__.py
│       ├── main.py                 # Punto de entrada principal
│       ├── io_utils.py
│       ├── structures/
│       │   ├── __init__.py
│       │   ├── union_find.py
│       │   └── priority_queue.py
│       └── algorithms/
│           ├── __init__.py
│           ├── greedy/
│           │   ├── __init__.py
│           │   └── interval_scheduling.py
│           ├── divide_conquer/
│           │   ├── __init__.py
│           │   ├── closest_pair.py
│           │   └── count_inversions.py
│           ├── dp/
│           │   ├── __init__.py
│           │   └── knapsack_01.py
│           ├── graphs/
│           │   ├── __init__.py
│           │   ├── dijkstra.py
│           │   ├── floyd_warshall.py
│           │   ├── prim.py
│           │   └── kruskal.py
│           ├── backtracking/
│           │   ├── __init__.py
│           │   └── n_queens.py
│           └── branch_and_bound/
│               ├── __init__.py
│               └── tsp_bnb.py
├── tests/
│   ├── __init__.py
│   ├── test_closest_pair.py
│   ├── test_interval_scheduling.py
│   ├── test_knapsack.py
│   ├── test_floyd_warshall.py
│   ├── test_dijkstra.py
│   └── test_union_find.py
├── data/
│   ├── samples/
│   └── outputs/
└── docs/
    ├── enunciado.pdf
    ├── analisis-complejidad.md
    └── decisiones-de-diseno.md
```

## 🔍 Descripción de Algoritmos

### 1. Par de Puntos Más Cercanos (Divide & Conquer)

Encuentra el par de puntos con menor distancia euclidiana en un conjunto de puntos en el plano.

- **Complejidad**: O(n log n)
- **Archivo**: `src/tp_algos/algorithms/divide_conquer/closest_pair.py`
- **Tests**: `tests/test_closest_pair.py`

**Características:**
- Implementación de fuerza bruta O(n²) para comparación
- Solución optimizada usando Divide & Conquer
- Medición de tiempos de ejecución
- 5+ ejemplos de prueba

### 2. Selección de Actividades (Greedy)

Selecciona la máxima cantidad de actividades no superpuestas dado un conjunto de actividades con tiempos de inicio y fin.

- **Complejidad**: O(n log n)
- **Archivo**: `src/tp_algos/algorithms/greedy/interval_scheduling.py`
- **Tests**: `tests/test_interval_scheduling.py`

**Estrategia Greedy:**
Ordenar por tiempo de fin y seleccionar siempre la actividad que termine primero.

**Justificación:**
La elección greedy maximiza el tiempo disponible para futuras actividades, garantizando optimalidad.

### 3. Mochila 0/1 (Programación Dinámica)

Maximiza el valor total en una mochila con capacidad limitada, pudiendo incluir o excluir completamente cada objeto.

- **Complejidad**: O(n × W) donde n = objetos, W = capacidad
- **Archivo**: `src/tp_algos/algorithms/dp/knapsack_01.py`
- **Tests**: `tests/test_knapsack.py`

**Características:**
- Solución con tabla DP completa
- Reconstrucción de items seleccionados
- Versión optimizada en espacio O(W)
- Información detallada del proceso

### 4. Floyd-Warshall (Grafos)

Encuentra los caminos más cortos entre todos los pares de nodos en un grafo ponderado.

- **Complejidad**: O(n³)
- **Archivo**: `src/tp_algos/algorithms/graphs/floyd_warshall.py`
- **Tests**: `tests/test_floyd_warshall.py`

**Problema Real:**
Red de distribución de paquetes de una empresa de logística con centros en diferentes ciudades.

**Características:**
- Matriz de distancias mínimas
- Reconstrucción de caminos
- Visualización paso a paso
- Aplicación práctica documentada

## 📊 Análisis de Complejidad

Ver documento completo en: [`docs/analisis-complejidad.md`](docs/analisis-complejidad.md)

| Algoritmo | Paradigma | Complejidad Temporal | Complejidad Espacial |
|-----------|-----------|---------------------|---------------------|
| Par de puntos más cercanos | Divide & Conquer | O(n log n) | O(n) |
| Selección de actividades | Greedy | O(n log n) | O(n) |
| Mochila 0/1 | Programación Dinámica | O(n × W) | O(n × W) o O(W) |
| Floyd-Warshall | Grafos | O(n³) | O(n²) |

## 🧪 Cobertura de Tests

Todos los algoritmos cuentan con tests exhaustivos:

- Tests unitarios para cada función
- Tests de casos límite (edge cases)
- Tests de rendimiento
- Tests de correctitud vs soluciones alternativas
- Tests con casos reales

## 📖 Documentación Adicional

- **Análisis de Complejidad**: [`docs/analisis-complejidad.md`](docs/analisis-complejidad.md)
- **Decisiones de Diseño**: [`docs/decisiones-de-diseno.md`](docs/decisiones-de-diseno.md)
- **Enunciado**: [`docs/enunciado.pdf`](docs/enunciado.pdf)

## 👥 Autores

Programación 3 - UADE

## 📝 Licencia

Este proyecto es parte de un trabajo práctico académico.
