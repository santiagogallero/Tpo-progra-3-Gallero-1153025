"""
Algoritmo Floyd-Warshall para encontrar caminos más cortos entre todos los pares de nodos.

Problema de la vida real: Red de distribución de paquetes
Una empresa de logística tiene centros de distribución en diferentes ciudades.
Los paquetes pueden pasar por múltiples centros antes de llegar a su destino.
Cada ruta entre centros tiene un costo (tiempo, distancia o dinero).
Floyd-Warshall nos ayuda a encontrar la ruta más económica entre cualquier par de centros.
"""
from typing import List, Tuple, Optional
import math


def floyd_warshall(grafo: List[List[float]]) -> Tuple[List[List[float]], List[List[Optional[int]]]]:
    """
    Algoritmo Floyd-Warshall para caminos más cortos entre todos los pares.
    
    Args:
        grafo: Matriz de adyacencia n×n donde grafo[i][j] es el peso de i->j
               Usar float('inf') para indicar que no hay arista
    
    Returns:
        Tupla con:
        - dist: Matriz de distancias mínimas
        - next: Matriz para reconstruir caminos (next[i][j] = próximo nodo en el camino i->j)
    
    Complejidad: O(n³)
    Espacio: O(n²)
    """
    n = len(grafo)
    
    # Inicializar matriz de distancias (copia del grafo)
    dist = [fila[:] for fila in grafo]
    
    # Inicializar matriz de siguiente nodo para reconstrucción de caminos
    next_node = [[None] * n for _ in range(n)]
    
    # Si hay una arista directa de i a j, el siguiente nodo es j
    for i in range(n):
        for j in range(n):
            if i != j and dist[i][j] != float('inf'):
                next_node[i][j] = j
    
    # Algoritmo Floyd-Warshall
    # Para cada nodo intermedio k
    for k in range(n):
        # Para cada par de nodos (i, j)
        for i in range(n):
            for j in range(n):
                # Si el camino i->k->j es mejor que el actual i->j
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]
    
    return dist, next_node


def reconstruir_camino(next_node: List[List[Optional[int]]], origen: int, destino: int) -> List[int]:
    """
    Reconstruye el camino más corto de origen a destino.
    
    Args:
        next_node: Matriz generada por floyd_warshall
        origen: Nodo inicial
        destino: Nodo final
    
    Returns:
        Lista de nodos en el camino (incluyendo origen y destino)
        Lista vacía si no hay camino
    """
    if next_node[origen][destino] is None:
        return []
    
    camino = [origen]
    actual = origen
    
    while actual != destino:
        actual = next_node[actual][destino]
        camino.append(actual)
    
    return camino


def floyd_warshall_detallado(grafo: List[List[float]], nombres_nodos: List[str] = None) -> dict:
    """
    Versión detallada que muestra el proceso paso a paso.
    
    Args:
        grafo: Matriz de adyacencia
        nombres_nodos: Nombres opcionales para los nodos
    
    Returns:
        Diccionario con información completa del algoritmo
    """
    n = len(grafo)
    
    if nombres_nodos is None:
        nombres_nodos = [f"Nodo_{i}" for i in range(n)]
    
    dist = [fila[:] for fila in grafo]
    next_node = [[None] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i != j and dist[i][j] != float('inf'):
                next_node[i][j] = j
    
    # Guardar pasos intermedios
    pasos = []
    pasos.append({
        'k': -1,
        'descripcion': 'Matriz inicial',
        'matriz': [fila[:] for fila in dist]
    })
    
    # Algoritmo con seguimiento de pasos
    for k in range(n):
        cambios = []
        for i in range(n):
            for j in range(n):
                nueva_dist = dist[i][k] + dist[k][j]
                if nueva_dist < dist[i][j]:
                    cambios.append({
                        'de': nombres_nodos[i],
                        'a': nombres_nodos[j],
                        'via': nombres_nodos[k],
                        'dist_anterior': dist[i][j] if dist[i][j] != float('inf') else '∞',
                        'dist_nueva': nueva_dist
                    })
                    dist[i][j] = nueva_dist
                    next_node[i][j] = next_node[i][k]
        
        pasos.append({
            'k': k,
            'nodo_intermedio': nombres_nodos[k],
            'descripcion': f'Considerando {nombres_nodos[k]} como nodo intermedio',
            'matriz': [fila[:] for fila in dist],
            'cambios': cambios
        })
    
    # Generar todos los caminos
    todos_caminos = {}
    for i in range(n):
        for j in range(n):
            if i != j and dist[i][j] != float('inf'):
                camino = reconstruir_camino(next_node, i, j)
                camino_nombres = [nombres_nodos[nodo] for nodo in camino]
                todos_caminos[f"{nombres_nodos[i]}_a_{nombres_nodos[j]}"] = {
                    'camino': camino_nombres,
                    'distancia': dist[i][j]
                }
    
    return {
        'matriz_distancias': dist,
        'nombres_nodos': nombres_nodos,
        'pasos': pasos,
        'todos_caminos': todos_caminos,
        'next_node': next_node
    }


def crear_grafo_vacio(n: int) -> List[List[float]]:
    """
    Crea una matriz de adyacencia vacía de tamaño n×n.
    Inicializa con 0 en la diagonal y infinito en el resto.
    """
    grafo = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        grafo[i][i] = 0
    return grafo


def imprimir_matriz(matriz: List[List[float]], nombres: List[str] = None):
    """
    Imprime una matriz de forma legible.
    """
    n = len(matriz)
    if nombres is None:
        nombres = [str(i) for i in range(n)]
    
    # Calcular ancho de columnas
    ancho = max(len(nombre) for nombre in nombres) + 2
    ancho = max(ancho, 8)
    
    # Encabezado
    print(" " * ancho, end="")
    for nombre in nombres:
        print(f"{nombre:>{ancho}}", end="")
    print()
    
    # Filas
    for i, fila in enumerate(matriz):
        print(f"{nombres[i]:>{ancho}}", end="")
        for valor in fila:
            if valor == float('inf'):
                print(f"{'∞':>{ancho}}", end="")
            else:
                print(f"{valor:>{ancho}.1f}", end="")
        print()
