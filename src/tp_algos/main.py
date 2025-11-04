"""
TP Algoritmos - Trabajo Práctico Integrador
Programación 3 - UADE

Implementación de algoritmos:
1. Divide & Conquer: Par de puntos más cercanos
2. Greedy: Selección de actividades
3. Programación Dinámica: Mochila 0/1
4. Grafos: Floyd-Warshall
"""
import sys
import time
from typing import Callable, Any

# Imports de los algoritmos implementados
from tp_algos.algorithms.divide_conquer.closest_pair import (
    closest_pair, fuerza_bruta
)
from tp_algos.algorithms.greedy.interval_scheduling import (
    seleccion_actividades_con_detalles
)
from tp_algos.algorithms.dp.knapsack_01 import (
    knapsack_01_detallado
)
from tp_algos.algorithms.graphs.floyd_warshall import (
    floyd_warshall_detallado, crear_grafo_vacio, imprimir_matriz
)


def separador(titulo: str = ""):
    """Imprime un separador visual."""
    print("\n" + "=" * 80)
    if titulo:
        print(f" {titulo} ".center(80, "="))
        print("=" * 80)
    print()


def medir_tiempo(func: Callable, *args, **kwargs) -> tuple[Any, float]:
    """Ejecuta una función y mide su tiempo de ejecución."""
    inicio = time.time()
    resultado = func(*args, **kwargs)
    fin = time.time()
    return resultado, (fin - inicio) * 1000  # en milisegundos


def demo_parte1_closest_pair():
    """Demostración: Par de puntos más cercanos."""
    separador("PARTE 1: PAR DE PUNTOS MÁS CERCANOS (Divide & Conquer)")
    
    ejemplos = [
        # Ejemplo 1: Caso simple
        {
            'nombre': 'Ejemplo 1 - Caso básico',
            'puntos': [(0, 0), (1, 1), (2, 2), (3, 3), (1, 0)]
        },
        # Ejemplo 2: Puntos muy cercanos
        {
            'nombre': 'Ejemplo 2 - Puntos muy cercanos',
            'puntos': [(1.5, 2.3), (1.51, 2.31), (5, 5), (10, 10), (8, 8)]
        },
        # Ejemplo 3: Puntos dispersos
        {
            'nombre': 'Ejemplo 3 - Puntos dispersos',
            'puntos': [(0, 0), (10, 10), (20, 20), (30, 30), (5, 15)]
        },
        # Ejemplo 4: Muchos puntos en línea
        {
            'nombre': 'Ejemplo 4 - Puntos en línea',
            'puntos': [(i, 0) for i in range(10)]
        },
        # Ejemplo 5: Caso más complejo
        {
            'nombre': 'Ejemplo 5 - Caso aleatorio complejo',
            'puntos': [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
        }
    ]
    
    for ejemplo in ejemplos:
        print(f"\n{'─' * 80}")
        print(f"{ejemplo['nombre']}")
        print(f"{'─' * 80}")
        print(f"Puntos: {ejemplo['puntos']}")
        print(f"Cantidad de puntos: {len(ejemplo['puntos'])}")
        
        # Método 1: Fuerza bruta O(n²)
        resultado_fb, tiempo_fb = medir_tiempo(fuerza_bruta, ejemplo['puntos'])
        dist_fb, p1_fb, p2_fb = resultado_fb
        
        # Método 2: Divide & Conquer O(n log n)
        resultado_dc, tiempo_dc = medir_tiempo(closest_pair, ejemplo['puntos'])
        dist_dc, p1_dc, p2_dc = resultado_dc
        
        print(f"\n✓ Resultado Fuerza Bruta (O(n²)):")
        print(f"  Distancia mínima: {dist_fb:.4f}")
        print(f"  Puntos: {p1_fb} y {p2_fb}")
        print(f"  Tiempo: {tiempo_fb:.6f} ms")
        
        print(f"\n✓ Resultado Divide & Conquer (O(n log n)):")
        print(f"  Distancia mínima: {dist_dc:.4f}")
        print(f"  Puntos: {p1_dc} y {p2_dc}")
        print(f"  Tiempo: {tiempo_dc:.6f} ms")
        
        print(f"\n📊 Comparación:")
        if tiempo_fb > 0:
            speedup = tiempo_fb / tiempo_dc if tiempo_dc > 0 else float('inf')
            print(f"  Speedup: {speedup:.2f}x más rápido con D&C")


def demo_parte2_greedy():
    """Demostración: Selección de actividades."""
    separador("PARTE 2: SELECCIÓN DE ACTIVIDADES (Greedy)")
    
    ejemplos = [
        {
            'nombre': 'Ejemplo 1 - Caso del enunciado',
            'actividades': [(1, 4), (3, 5), (0, 6), (5, 7), (3, 8), (5, 9), (6, 10), (8, 11), (8, 12), (2, 13), (12, 14)]
        },
        {
            'nombre': 'Ejemplo 2 - Actividades disjuntas',
            'actividades': [(0, 2), (3, 5), (6, 8), (9, 11)]
        },
        {
            'nombre': 'Ejemplo 3 - Todas superpuestas',
            'actividades': [(1, 10), (2, 9), (3, 8), (4, 7), (5, 6)]
        },
        {
            'nombre': 'Ejemplo 4 - Caso complejo',
            'actividades': [(1, 3), (2, 5), (4, 7), (1, 8), (5, 9), (8, 10), (9, 11), (11, 14), (13, 16)]
        }
    ]
    
    for ejemplo in ejemplos:
        print(f"\n{'─' * 80}")
        print(f"{ejemplo['nombre']}")
        print(f"{'─' * 80}")
        print(f"Actividades (inicio, fin):")
        for i, (inicio, fin) in enumerate(ejemplo['actividades']):
            print(f"  Actividad {i}: [{inicio:2d}, {fin:2d}]")
        
        resultado, tiempo_ejecucion = medir_tiempo(
            seleccion_actividades_con_detalles, 
            ejemplo['actividades']
        )
        
        print(f"\n✓ Resultado:")
        print(f"  Cantidad máxima de actividades: {resultado['cantidad']}")
        print(f"  Índices seleccionados: {resultado['indices']}")
        print(f"  Actividades seleccionadas:")
        for idx in resultado['indices']:
            inicio, fin = ejemplo['actividades'][idx]
            print(f"    Actividad {idx}: [{inicio}, {fin}]")
        
        print(f"\n📝 Proceso Greedy:")
        for paso in resultado['pasos']:
            print(f"  {paso}")
        
        print(f"\n⏱️  Tiempo de ejecución: {tiempo_ejecucion:.6f} ms")
        print(f"📊 Complejidad: O(n log n) - dominada por el ordenamiento")


def demo_parte3_knapsack():
    """Demostración: Mochila 0/1."""
    separador("PARTE 3: MOCHILA 0/1 (Programación Dinámica)")
    
    ejemplos = [
        {
            'nombre': 'Ejemplo 1 - Del enunciado',
            'pesos': [6, 3, 4],
            'valores': [30, 14, 16],
            'capacidad': 10,
            'nombres': ['O1', 'O2', 'O3']
        },
        {
            'nombre': 'Ejemplo 2 - Caso simple',
            'pesos': [2, 3, 4, 5],
            'valores': [3, 4, 5, 6],
            'capacidad': 8,
            'nombres': ['A', 'B', 'C', 'D']
        },
        {
            'nombre': 'Ejemplo 3 - Muchos objetos pequeños',
            'pesos': [1, 2, 3, 4, 5],
            'valores': [10, 15, 40, 25, 30],
            'capacidad': 10,
            'nombres': ['Item1', 'Item2', 'Item3', 'Item4', 'Item5']
        },
        {
            'nombre': 'Ejemplo 4 - Objetos de alto valor',
            'pesos': [5, 4, 6, 3],
            'valores': [10, 40, 30, 50],
            'capacidad': 10,
            'nombres': ['Oro', 'Plata', 'Bronce', 'Diamante']
        }
    ]
    
    for ejemplo in ejemplos:
        print(f"\n{'─' * 80}")
        print(f"{ejemplo['nombre']}")
        print(f"{'─' * 80}")
        print(f"Capacidad de la mochila: {ejemplo['capacidad']}")
        print(f"\nObjetos disponibles:")
        for i, (nombre, peso, valor) in enumerate(zip(ejemplo['nombres'], ejemplo['pesos'], ejemplo['valores'])):
            relacion = valor / peso if peso > 0 else 0
            print(f"  {nombre}: peso={peso}, valor={valor}, relación={relacion:.2f}")
        
        resultado, tiempo_ejecucion = medir_tiempo(
            knapsack_01_detallado,
            ejemplo['pesos'],
            ejemplo['valores'],
            ejemplo['capacidad']
        )
        
        print(f"\n✓ Resultado:")
        print(f"  Valor máximo: {resultado['valor_maximo']}")
        print(f"  Capacidad usada: {resultado['capacidad_usada']}")
        print(f"  Objetos seleccionados ({resultado['n_items_seleccionados']}):")
        
        for item in resultado['solucion_detallada']:
            nombre = ejemplo['nombres'][item['indice']]
            print(f"    {nombre}: peso={item['peso']}, valor={item['valor']}, relación={item['relacion']:.2f}")
        
        print(f"\n⏱️  Tiempo de ejecución: {tiempo_ejecucion:.6f} ms")
        print(f"📊 Complejidad: O(n × W) donde n={len(ejemplo['pesos'])}, W={ejemplo['capacidad']}")


def demo_parte4_floyd_warshall():
    """Demostración: Floyd-Warshall."""
    separador("PARTE 4: FLOYD-WARSHALL (Grafos)")
    
    print("Problema de la vida real: RED DE DISTRIBUCIÓN DE PAQUETES")
    print("\nUna empresa de logística tiene 5 centros de distribución:")
    print("- Buenos Aires (BA)")
    print("- Córdoba (COR)")
    print("- Rosario (ROS)")
    print("- Mendoza (MDZ)")
    print("- Tucumán (TUC)")
    print("\nLos costos (en miles de pesos) para transportar paquetes entre centros son:")
    
    # Crear el grafo del problema
    n = 5
    nombres = ["BA", "COR", "ROS", "MDZ", "TUC"]
    grafo = crear_grafo_vacio(n)
    
    # Definir las rutas directas (asimétricas para mayor realismo)
    rutas = [
        (0, 1, 500),   # BA -> COR: $500k
        (0, 2, 300),   # BA -> ROS: $300k
        (1, 0, 500),   # COR -> BA: $500k
        (1, 3, 600),   # COR -> MDZ: $600k
        (1, 4, 450),   # COR -> TUC: $450k
        (2, 0, 300),   # ROS -> BA: $300k
        (2, 1, 350),   # ROS -> COR: $350k
        (2, 4, 800),   # ROS -> TUC: $800k
        (3, 1, 600),   # MDZ -> COR: $600k
        (4, 1, 450),   # TUC -> COR: $450k
        (4, 2, 750),   # TUC -> ROS: $750k
    ]
    
    for origen, destino, costo in rutas:
        grafo[origen][destino] = costo
    
    print("\nMatriz de adyacencia (costos directos):")
    imprimir_matriz(grafo, nombres)
    
    # Ejecutar Floyd-Warshall
    print("\n🔄 Ejecutando algoritmo Floyd-Warshall...")
    resultado, tiempo_ejecucion = medir_tiempo(
        floyd_warshall_detallado,
        grafo,
        nombres
    )
    
    print(f"⏱️  Tiempo de ejecución: {tiempo_ejecucion:.6f} ms")
    print(f"📊 Complejidad: O(n³) donde n={n}")
    
    # Mostrar proceso paso a paso (solo algunos pasos importantes)
    print("\n📝 Proceso paso a paso (pasos con cambios):")
    for paso in resultado['pasos']:
        if paso['k'] >= 0 and paso.get('cambios'):
            print(f"\n  Paso {paso['k'] + 1}: Usando {paso['nodo_intermedio']} como intermedio")
            for cambio in paso['cambios'][:3]:  # Mostrar máximo 3 cambios
                print(f"    {cambio['de']} → {cambio['a']}: {cambio['dist_anterior']} → {cambio['dist_nueva']} (vía {cambio['via']})")
            if len(paso['cambios']) > 3:
                print(f"    ... y {len(paso['cambios']) - 3} cambios más")
    
    # Matriz final
    print("\n✓ Matriz de distancias mínimas (resultado final):")
    imprimir_matriz(resultado['matriz_distancias'], nombres)
    
    # Ejemplos de caminos específicos
    print("\n🛣️  Ejemplos de rutas óptimas:")
    ejemplos_rutas = [
        ("BA", "MDZ"),
        ("BA", "TUC"),
        ("ROS", "MDZ"),
        ("MDZ", "ROS"),
    ]
    
    for origen_nombre, destino_nombre in ejemplos_rutas:
        clave = f"{origen_nombre}_a_{destino_nombre}"
        if clave in resultado['todos_caminos']:
            info = resultado['todos_caminos'][clave]
            camino_str = " → ".join(info['camino'])
            print(f"  {origen_nombre} a {destino_nombre}:")
            print(f"    Camino: {camino_str}")
            print(f"    Costo total: ${info['distancia']:.0f}k")
    
    print("\n💡 Interpretación:")
    print("  - El algoritmo encontró las rutas más económicas entre todos los centros")
    print("  - Algunas rutas óptimas pasan por centros intermedios")
    print("  - La empresa puede usar esta información para optimizar costos de envío")


def menu_principal():
    """Menú interactivo principal."""
    while True:
        separador("TP ALGORITMOS - MENÚ PRINCIPAL")
        print("Seleccione una demostración:")
        print()
        print("  1. Parte 1: Par de puntos más cercanos (Divide & Conquer)")
        print("  2. Parte 2: Selección de actividades (Greedy)")
        print("  3. Parte 3: Mochila 0/1 (Programación Dinámica)")
        print("  4. Parte 4: Floyd-Warshall (Grafos)")
        print("  5. Ejecutar todas las demostraciones")
        print("  0. Salir")
        print()
        
        try:
            opcion = input("Ingrese su opción: ").strip()
            
            if opcion == "1":
                demo_parte1_closest_pair()
            elif opcion == "2":
                demo_parte2_greedy()
            elif opcion == "3":
                demo_parte3_knapsack()
            elif opcion == "4":
                demo_parte4_floyd_warshall()
            elif opcion == "5":
                demo_parte1_closest_pair()
                demo_parte2_greedy()
                demo_parte3_knapsack()
                demo_parte4_floyd_warshall()
                print("\n✓ Todas las demostraciones completadas!")
            elif opcion == "0":
                print("\n¡Hasta luego!")
                break
            else:
                print("\n❌ Opción inválida. Intente nuevamente.")
            
            input("\nPresione Enter para continuar...")
            
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\nPresione Enter para continuar...")


def main():
    """Punto de entrada principal."""
    try:
        menu_principal()
    except Exception as e:
        print(f"Error fatal: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

