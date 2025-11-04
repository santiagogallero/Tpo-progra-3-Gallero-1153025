# Decisiones de Diseño - TP Algoritmos

## Índice
1. [Arquitectura General](#1-arquitectura-general)
2. [Decisiones por Algoritmo](#2-decisiones-por-algoritmo)
3. [Estructura de Código](#3-estructura-de-código)
4. [Testing](#4-testing)
5. [Documentación](#5-documentación)

---

## 1. Arquitectura General

### Estructura de Paquetes

```
src/tp_algos/
├── algorithms/          # Algoritmos organizados por paradigma
│   ├── divide_conquer/ # Divide & Conquer
│   ├── greedy/         # Algoritmos Greedy
│   ├── dp/             # Programación Dinámica
│   ├── graphs/         # Algoritmos de Grafos
│   ├── backtracking/   # Backtracking
│   └── branch_and_bound/
├── structures/         # Estructuras de datos auxiliares
├── main.py            # Punto de entrada
└── io_utils.py        # Utilidades de I/O
```

**Justificación:**
- **Separación por paradigma**: Facilita la comprensión y el mantenimiento
- **Modularidad**: Cada algoritmo es independiente y reutilizable
- **Extensibilidad**: Fácil agregar nuevos algoritmos
- **Testabilidad**: Cada módulo se puede probar por separado

### Lenguaje: Python

**Razones de elección:**
1. **Claridad**: Código legible, cercano al pseudocódigo
2. **Productividad**: Desarrollo rápido
3. **Bibliotecas**: Excelente ecosistema (pytest, typing)
4. **Educativo**: Ideal para aprendizaje de algoritmos

**Trade-offs:**
- ❌ Menos rendimiento que C++/Java
- ✅ Más rápido de desarrollar y depurar
- ✅ Mejor para prototipado y demostraciones

---

## 2. Decisiones por Algoritmo

### 2.1 Par de Puntos Más Cercanos

#### Representación de Puntos

```python
Point = Tuple[float, float]  # (x, y)
```

**Decisión**: Usar tuplas en lugar de clases

**Razones:**
- ✅ Inmutabilidad: Previene modificaciones accidentales
- ✅ Eficiencia: Menor overhead de memoria
- ✅ Simplicidad: Fácil de usar y entender
- ✅ Hashable: Se pueden usar en sets y diccionarios

**Alternativa rechazada**: Clase `Point` con atributos x, y
- ❌ Más verboso
- ❌ Overhead innecesario para este problema

#### Umbral para Fuerza Bruta

```python
if n <= 3:
    return fuerza_bruta(puntos)
```

**Decisión**: Usar n ≤ 3 como caso base

**Justificación:**
- Con 3 o menos puntos, fuerza bruta es O(1)
- Evita overhead de recursión innecesario
- Balance entre simplicidad y eficiencia

**Experimentos**:
- Probado con umbrales de 2, 3, 5, 10
- n=3 mostró mejor balance

#### Optimización de la Franja

```python
for j in range(i + 1, min(i + 8, n)):
```

**Decisión**: Limitar búsqueda a 7 puntos siguientes

**Fundamento teórico:**
- En una franja de ancho 2d, máximo 6 puntos pueden estar dentro de un rectángulo de 2d × d
- Limitar a 7 asegura correctitud y optimiza rendimiento

### 2.2 Selección de Actividades

#### Criterio Greedy

```python
actividades_indexadas.sort(key=lambda x: x[1])  # Ordenar por fin
```

**Decisión**: Ordenar por tiempo de fin (no por inicio, duración o valor)

**Justificación:**
- ✅ Demostrado matemáticamente óptimo
- ✅ Maximiza tiempo disponible para futuras actividades
- ❌ Ordenar por inicio: NO es óptimo
- ❌ Ordenar por duración: NO es óptimo

**Ejemplo de por qué otras estrategias fallan:**

```
Ordenar por inicio:
[(0,10), (1,2), (3,4)] → Selecciona (0,10) → 1 actividad
Óptimo: (1,2), (3,4) → 2 actividades ✗

Ordenar por duración:
[(0,3), (2,5), (4,7)] todas duración 3
Puede seleccionar (2,5) primero → 1 actividad
Óptimo: (0,3), (4,7) → 2 actividades ✗

Ordenar por fin:
Siempre da solución óptima ✓
```

#### Mantenimiento de Índices

```python
actividades_indexadas = [(inicio, fin, i) for i, (inicio, fin) in enumerate(actividades)]
```

**Decisión**: Mantener índices originales durante ordenamiento

**Razones:**
- ✅ Permite rastrear actividades seleccionadas
- ✅ Útil para debugging y análisis
- ✅ Overhead mínimo

### 2.3 Mochila 0/1

#### Tabla DP vs Recursión con Memoización

**Decisión**: Implementar solución iterativa (bottom-up)

**Comparación:**

| Aspecto | Bottom-up (elegida) | Top-down (memoización) |
|---------|---------------------|------------------------|
| Control | Explícito, predecible | Recursión implícita |
| Espacio | O(n×W) tabla | O(n×W) + O(n) pila |
| Debugging | Más fácil ver tabla | Más difícil |
| Optimización | Fácil optimizar a O(W) | Difícil |
| Claridad | Muy clara | Requiere entender recursión |

**Implementación adicional**: Versión optimizada O(W)

```python
def knapsack_01_optimizado(pesos, valores, capacidad):
    dp = [0] * (capacidad + 1)
    for i in range(len(pesos)):
        for w in range(capacidad, pesos[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - pesos[i]] + valores[i])
    return dp[capacidad]
```

**Trade-off:**
- ✅ Ahorra memoria
- ❌ No se pueden reconstruir items

#### Reconstrucción de Items

```python
if dp[i][w] != dp[i-1][w]:
    items_seleccionados.append(i-1)
```

**Decisión**: Reconstruir examinando cambios en tabla DP

**Alternativas consideradas:**
1. **Mantener tabla de decisiones** (elegir/no elegir)
   - ❌ Duplica memoria
   
2. **Recalcular desde cero**
   - ❌ O(n×W) adicional
   
3. **Examinar cambios en DP** ✓
   - ✅ O(n) tiempo
   - ✅ No requiere memoria adicional

### 2.4 Floyd-Warshall

#### Inicialización del Grafo

```python
def crear_grafo_vacio(n):
    grafo = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        grafo[i][i] = 0
    return grafo
```

**Decisión**: Usar `float('inf')` para aristas inexistentes

**Razones:**
- ✅ Semántica clara: infinito = no hay camino
- ✅ Aritmética correcta: inf + x = inf
- ✅ Comparaciones funcionan: x < inf siempre verdadero
- ❌ Alternativa rechazada: usar -1 o None
  - Requiere checks especiales
  - No funciona con aritmética

#### Matriz de Reconstrucción (next)

```python
next_node = [[None] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        if i != j and dist[i][j] != float('inf'):
            next_node[i][j] = j
```

**Decisión**: Mantener matriz separada para reconstruir caminos

**Justificación:**
- ✅ Permite reconstruir cualquier camino en O(n)
- ✅ No modifica la matriz de distancias
- ✅ Costo de memoria: O(n²) adicional (aceptable)

**Alternativa rechazada**: Recalcular caminos cuando se necesiten
- ❌ O(n³) por cada camino
- ❌ Ineficiente si se consultan múltiples caminos

#### Orden de los Ciclos

```python
for k in range(n):      # Intermedio (DEBE ser el externo)
    for i in range(n):  # Origen
        for j in range(n):  # Destino
```

**Decisión crítica**: k (nodo intermedio) DEBE ser el ciclo externo

**Justificación:**
- El algoritmo construye soluciones usando nodos {0,...,k} como intermedios
- Si k no es el externo, el invariante se rompe
- **Orden correcto es esencial para correctitud**

---

## 3. Estructura de Código

### Type Hints

```python
def knapsack_01(pesos: List[int], valores: List[int], capacidad: int) -> int:
    ...
```

**Decisión**: Usar type hints en todas las funciones públicas

**Beneficios:**
- ✅ Autodocumentación
- ✅ Mejor IDE support (autocomplete, warnings)
- ✅ Detección temprana de errores
- ✅ Facilita mantenimiento

### Docstrings

**Decisión**: Usar docstrings estilo Google

```python
"""
Brief description.

Args:
    param1: Description
    param2: Description

Returns:
    Description

Complejidad: O(...)
"""
```

**Razones:**
- ✅ Estándar de la industria
- ✅ Legible tanto en código como generado
- ✅ Soportado por herramientas (Sphinx, VS Code)

### Funciones Múltiples por Algoritmo

Cada algoritmo tiene varias versiones:

```python
knapsack_01()              # Versión básica (valor máximo)
knapsack_01_con_items()    # Con reconstrucción
knapsack_01_detallado()    # Con información completa
knapsack_01_optimizado()   # Optimizado en espacio
```

**Justificación:**
- ✅ Diferentes casos de uso
- ✅ Trade-offs explícitos (memoria vs funcionalidad)
- ✅ Educativo: muestra variaciones
- ❌ Trade-off: más código que mantener

---

## 4. Testing

### Estructura de Tests

```
tests/
├── test_closest_pair.py
├── test_interval_scheduling.py
├── test_knapsack.py
└── test_floyd_warshall.py
```

**Decisión**: Un archivo de test por algoritmo

**Organización:**
```python
class TestAlgoritmo:
    """Tests del algoritmo principal"""
    
class TestCasosEspeciales:
    """Edge cases"""
    
class TestComparacion:
    """Comparaciones con otras soluciones"""
```

### Estrategia de Testing

**Tipos de tests implementados:**

1. **Tests básicos**: Casos simples conocidos
2. **Tests de correctitud**: Comparar con soluciones alternativas
3. **Tests de edge cases**: Vacío, un elemento, máximo
4. **Tests de propiedades**: Invariantes que deben cumplirse
5. **Tests de regresión**: Casos que fallaron anteriormente

**Ejemplo de test de propiedad:**
```python
def test_no_se_superponen(self):
    """Verificar que las actividades seleccionadas no se superpongan"""
    resultado = seleccion_actividades(actividades)
    actividades_selec = [actividades[i] for i in resultado]
    for i in range(len(actividades_selec) - 1):
        assert actividades_selec[i][1] <= actividades_selec[i+1][0]
```

### Fixtures y Parametrización

**Decisión**: Usar pytest sin fixtures complejas

**Razones:**
- ✅ Tests más explícitos y autocontenidos
- ✅ Más fácil de entender para propósitos educativos
- ✅ Menos "magia" de pytest

---

## 5. Documentación

### README.md

**Decisión**: README completo con:
- Instalación paso a paso
- Ejemplos de uso
- Estructura del proyecto
- Tabla resumen de algoritmos

**Target**: Estudiantes y evaluadores

### Análisis de Complejidad

**Decisión**: Documento separado con análisis detallado

**Contenido:**
- Pseudocódigo
- Análisis formal (mejor/promedio/peor caso)
- Comparaciones
- Ejemplos de tiempos reales

### Decisiones de Diseño

**Decisión**: Este documento

**Propósito:**
- Justificar decisiones técnicas
- Documentar alternativas consideradas
- Explicar trade-offs

---

## 6. Decisiones Rechazadas

### POO Excesiva

**Rechazado**: Crear clases para todo (Point, Activity, Item, etc.)

**Razones:**
- ❌ Overhead innecesario para problemas simples
- ❌ Más código sin beneficio real
- ✅ Preferir estructuras simples (tuplas, listas)

### Optimizaciones Prematuras

**Rechazado**: Implementar versiones en Cython/C

**Razones:**
- ❌ Complejidad innecesaria
- ❌ Dificulta comprensión
- ✅ Python puro es suficientemente rápido para casos de uso académicos

### GUI

**Rechazado**: Interfaz gráfica

**Razones:**
- ❌ Fuera del scope del TP
- ❌ CLI es suficiente
- ✅ Visualizaciones en terminal son más simples

### Múltiples Lenguajes

**Rechazado**: Implementar en Python + Java/C++

**Razones:**
- ❌ Duplicación de esfuerzo
- ❌ Más difícil de mantener
- ✅ Un lenguaje bien hecho es mejor

---

## 7. Lecciones Aprendidas

### Lo que funcionó bien

1. **Modularidad**: Separar por paradigmas fue excelente
2. **Tests exhaustivos**: Detectaron muchos bugs tempranos
3. **Type hints**: Mejoraron calidad del código
4. **Múltiples versiones**: Útil para diferentes casos de uso

### Lo que se podría mejorar

1. **Benchmarks**: Agregar módulo de benchmarking automatizado
2. **Visualización**: Agregar gráficos de complejidad
3. **Más ejemplos**: Más casos de uso reales
4. **Performance profiling**: Analizar cuellos de botella

### Trade-offs Aceptados

1. **Claridad > Performance**: Código legible sobre optimizaciones micro
2. **Completitud > Simplicidad**: Múltiples versiones vs una versión simple
3. **Educación > Producción**: Código didáctico sobre código productivo

---

## 8. Conclusión

Este diseño prioriza:

1. **Claridad y legibilidad** para propósitos educativos
2. **Modularidad** para facilitar comprensión y testing
3. **Completitud** con múltiples versiones de cada algoritmo
4. **Documentación exhaustiva** para facilitar evaluación

Las decisiones tomadas reflejan un balance entre teoría (correctitud, complejidad) y práctica (implementación, usabilidad), con énfasis en el aspecto educativo del trabajo práctico.
