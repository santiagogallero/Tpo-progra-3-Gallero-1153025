# Informe – Trabajo Práctico Integrador (Algoritmos)

Programación 3 – UADE  
Autor: Santiago Gallero (1153025)

---

## Índice
- [Introducción](#introducción)
- [Parte 1 – Divide & Conquer: Par de puntos más cercanos](#parte-1--divide--conquer-par-de-puntos-más-cercanos)
  - [Enunciado](#enunciado)
  - [Pseudocódigo](#pseudocódigo)
  - [Explicación paso a paso](#explicación-paso-a-paso)
  - [Complejidad y comparación con O(n²)](#complejidad-y-comparación-con-on²)
  - [Implementación (referencia de código)](#implementación-referencia-de-código)
  - [Casos de prueba](#casos-de-prueba)
- [Parte 2 – Greedy: Selección de actividades](#parte-2--greedy-selección-de-actividades)
  - [Enunciado](#enunciado-1)
  - [Pseudocódigo Greedy](#pseudocódigo-greedy)
  - [Justificación de correctitud](#justificación-de-correctitud)
  - [Complejidad](#complejidad)
  - [Implementación (referencia de código)](#implementación-referencia-de-código-1)
  - [Casos de prueba](#casos-de-prueba-1)
- [Parte 3 – Programación Dinámica: Mochila 0/1](#parte-3--programación-dinámica-mochila-01)
  - [Enunciado y ejemplo](#enunciado-y-ejemplo)
  - [Pseudocódigo](#pseudocódigo-1)
  - [Complejidad](#complejidad-1)
  - [Implementación (referencia de código)](#implementación-referencia-de-código-2)
  - [Pruebas y variantes](#pruebas-y-variantes)
- [Parte 4 – Grafos: Floyd-Warshall](#parte-4--grafos-floyd-warshall)
  - [Modelado del problema real](#modelado-del-problema-real)
  - [Representación (matriz de adyacencia)](#representación-matriz-de-adyacencia)
  - [Pseudocódigo](#pseudocódigo-2)
  - [Ejecución paso a paso (resumen)](#ejecución-paso-a-paso-resumen)
  - [Complejidad](#complejidad-2)
  - [Implementación (referencia de código)](#implementación-referencia-de-código-3)
  - [Tabla final de distancias mínimas (ejemplo)](#tabla-final-de-distancias-mínimas-ejemplo)
  - [Comparación con Dijkstra (opcional)](#comparación-con-dijkstra-opcional)
- [Conclusiones y reflexión](#conclusiones-y-reflexión)
- [Cómo ejecutar](#cómo-ejecutar)
- [Cómo exportar este informe a PDF](#cómo-exportar-este-informe-a-pdf)

---

## Introducción
Este informe reúne todo lo no-código del TP: enunciados resumidos, pseudocódigo, explicaciones, análisis de complejidad, modelado, discusión y casos de prueba usados para validar las implementaciones. Las implementaciones en Python se encuentran en `src/` y los tests en `tests/`.

---

## Parte 1 – Divide & Conquer: Par de puntos más cercanos

### Enunciado
Dado un conjunto de n puntos en el plano 2D, encontrar el par de puntos con menor distancia euclidiana.

### Pseudocódigo
```
función CLOSEST_PAIR(puntos):
    px ← ORDENAR(puntos por x)
    py ← ORDENAR(puntos por y)
    retornar CLOSEST_PAIR_REC(px, py)

función CLOSEST_PAIR_REC(px, py):
    n ← |px|
    si n ≤ 3:
        retornar FUERZA_BRUTA(px)

    mid ← n // 2
    p_med ← px[mid]
    pyl ← {p ∈ py | p.x ≤ p_med.x}
    pyr ← {p ∈ py | p.x > p_med.x}

    dl, parL ← CLOSEST_PAIR_REC(px[0:mid], pyl)
    dr, parR ← CLOSEST_PAIR_REC(px[mid:n], pyr)

    d, par ← min{(dl, parL), (dr, parR)}

    franja ← {p ∈ py | |p.x − p_med.x| < d}
    ds, parS ← MIN_DISTANCIA_FRANJA(franja, d)

    si ds < d: retornar (ds, parS)
    en otro caso: retornar (d, par)

función MIN_DISTANCIA_FRANJA(franja, d):
    ordenar franja por y
    min_d ← d
    para i en [0..|franja|-1]:
        para j en [i+1 .. min(i+7, |franja|-1)]:
            si franja[j].y − franja[i].y ≥ min_d: romper
            min_d ← min(min_d, dist(franja[i], franja[j]))
    retornar min_d, (p_i, p_j)
```

### Explicación paso a paso
1. Ordenar por x e y (preprocesamiento).  
2. Dividir el conjunto en dos mitades por x.  
3. Resolver recursivamente izquierda y derecha.  
4. Combinar: tomar el mínimo y revisar la franja central (puntos a menos de d de la línea media), comparando a lo sumo 7 vecinos por punto.  
5. Devolver la menor distancia encontrada.

### Complejidad y comparación con O(n²)
- Fuerza bruta: O(n²) comparando todos los pares.  
- Divide & Conquer: T(n) = 2T(n/2) + O(n) ⇒ O(n log n).  
- A partir de n ≳ 1,000 el método D&C es sustancialmente más rápido.

### Implementación (referencia de código)
- `src/tp_algos/algorithms/divide_conquer/closest_pair.py`
- Tests: `tests/test_closest_pair.py`

### Casos de prueba
- Caso básico: `[(0,0),(1,1),(2,2),(3,3),(1,0)]` ⇒ par más cercano `(1,0)-(1,1)` o similar; distancia ≈ 1.0.  
- Puntos muy cercanos: `[(1.5,2.3),(1.51,2.31),(5,5),(10,10),(8,8)]` ⇒ distancia < 0.02.  
- Puntos dispersos: `[(0,0),(10,10),(20,20),(30,30),(5,15)]` ⇒ d > 1.0.  
- En línea: `[(i,0) para i en 0..9]` ⇒ d = 1.0.  
- Caso complejo: `[(2,3),(12,30),(40,50),(5,1),(12,10),(3,4)]` ⇒ d = √2 entre `(2,3)` y `(3,4)`.

---

## Parte 2 – Greedy: Selección de actividades

### Enunciado
Dadas actividades con inicio y fin, seleccionar la máxima cantidad de actividades no superpuestas.

### Pseudocódigo Greedy
```
función SELECCION_ACTIVIDADES(A):
    A_ords ← ordenar A por tiempo de fin
    seleccion ← []
    ultimo_fin ← −∞
    para (inicio, fin) en A_ords:
        si inicio ≥ ultimo_fin:
            agregar seleccion ← (inicio, fin)
            ultimo_fin ← fin
    retornar seleccion
```

### Justificación de correctitud
- Elección greedy: elegir siempre la que termina primero deja más “espacio” al futuro.  
- Demostración por intercambio: cualquier solución óptima puede transformarse en la greedy sin perder optimalidad.

### Complejidad
- O(n log n) por ordenar; el recorrido es O(n).

### Implementación (referencia de código)
- `src/tp_algos/algorithms/greedy/interval_scheduling.py`
- Tests: `tests/test_interval_scheduling.py`

### Casos de prueba
- Caso clásico (CLRS): `(1,4),(3,5),(0,6),(5,7),(3,8),(5,9),(6,10),(8,11),(8,12),(2,13),(12,14)`  
- Disjuntas: `(0,2),(3,5),(6,8),(9,11)` ⇒ selecciona todas.  
- Todas superpuestas: `(1,10),(2,9),(3,8),(4,7)` ⇒ elige una (la que termina antes).

---

## Parte 3 – Programación Dinámica: Mochila 0/1

### Enunciado y ejemplo
Capacidad W=10; Objetos: O1=(6,30), O2=(3,14), O3=(4,16).  
Solución óptima: {O2, O3} con valor 30.

### Pseudocódigo
```
función KNAPSACK_01(pesos, valores, W):
    n ← |pesos|
    dp ← matriz (n+1) × (W+1) con 0
    para i=1..n:
        para w=0..W:
            dp[i][w] ← dp[i-1][w]
            si pesos[i-1] ≤ w:
                dp[i][w] ← max(dp[i][w], dp[i-1][w-pesos[i-1]] + valores[i-1])
    retornar dp[n][W]
```

### Complejidad
- Tiempo: O(n × W).  
- Espacio: O(n × W) (u O(W) en la versión optimizada).

### Implementación (referencia de código)
- `src/tp_algos/algorithms/dp/knapsack_01.py` (incluye: valor, reconstrucción de items, versión O(W)).  
- Tests: `tests/test_knapsack.py`.

### Pruebas y variantes
- Caso del enunciado ⇒ valor 30, items {1,2}.  
- Capacidad 0 ⇒ valor 0.  
- Todos caben ⇒ suma de todos los valores.  
- Versión O(W) verifica mismo resultado que la tabla completa.

---

## Parte 4 – Grafos: Floyd-Warshall

### Modelado del problema real
Red de distribución de paquetes con centros: BA, COR, ROS, MDZ, TUC.  
Costo de transporte (en miles de pesos) como pesos de las aristas (dirigidas).

### Representación (matriz de adyacencia)
- `grafo[i][j] = costo(i→j)`; `∞` si no hay arista; `0` en la diagonal.

### Pseudocódigo
```
función FLOYD_WARSHALL(grafo):
    n ← |grafo|
    dist ← copia(grafo)
    next ← matriz n×n con None
    para i,j:
        si i≠j y dist[i][j]≠∞: next[i][j] ← j
    para k=0..n-1:
      para i=0..n-1:
        para j=0..n-1:
          si dist[i][k] + dist[k][j] < dist[i][j]:
              dist[i][j] ← dist[i][k] + dist[k][j]
              next[i][j] ← next[i][k]
    retornar dist, next
```

### Ejecución paso a paso (resumen)
- Para cada `k`, se permiten caminos con nodos intermedios en `{0..k}`.  
- Se actualiza `dist[i][j]` si pasar por `k` mejora el costo.  
- Se mantiene `next` para reconstruir caminos mínimos.

### Complejidad
- Tiempo: O(n³).  
- Espacio: O(n²).

### Implementación (referencia de código)
- `src/tp_algos/algorithms/graphs/floyd_warshall.py` (incluye reconstrucción y versión detallada).  
- Tests: `tests/test_floyd_warshall.py`.

### Tabla final de distancias mínimas (ejemplo)
Caso de 5 nodos (BA, COR, ROS, MDZ, TUC) con rutas definidas en `main.py`.  
La matriz de distancias y algunos caminos óptimos se muestran por consola en la demo.

### Comparación con Dijkstra (opcional)
- Floyd-Warshall devuelve distancias para **todos los pares** en O(n³).  
- Dijkstra (con heap) desde un nodo cuesta O((n+m) log n); para todos los nodos: ≈ O(n·(n+m) log n).  
- Grafos pequeños/densos o con pesos negativos (sin ciclos): Floyd-Warshall.  
- Grafos grandes/dispersos y consultas desde pocos orígenes: Dijkstra.

---

## Conclusiones y reflexión
- Greedy es el más simple; D&C y DP requieren mayor diseño, pero logran mejoras asintóticas o garantizan optimalidad.  
- Closest Pair y Greedy escalan muy bien.  
- Knapsack depende de W (pseudo-polinomial).  
- Floyd-Warshall es práctico para n moderado; para grafos grandes conviene Dijkstra repetido.

---

## Cómo ejecutar
1) Crear venv e instalar dependencias:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Ejecutar el menú de demostraciones:
```bash
# asegúrate de incluir src en PYTHONPATH
PYTHONPATH=$(pwd)/src python3 -m tp_algos.main
```

3) Ejecutar tests:
```bash
pytest -q
```

---

## Cómo exportar este informe a PDF
Si tenés `pandoc` instalado, podés exportar este archivo a PDF con:
```bash
# desde la carpeta del repositorio
pandoc docs/informe-tp.md -o docs/informe-tp.pdf \
  --from gfm --toc --number-sections \
  -V geometry:margin=1in -V mainfont="Helvetica"
```
Alternativas:
- VS Code: “Markdown PDF” extension o “Export as PDF”.
- Google Docs: copiar/pegar y exportar a PDF.
