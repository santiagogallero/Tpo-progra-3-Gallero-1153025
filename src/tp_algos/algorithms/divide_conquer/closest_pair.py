"""
Problema: Par de puntos más cercanos en el plano.
Algoritmo Divide & Conquer para encontrar los dos puntos más cercanos.
"""
import math
from typing import List, Tuple

Point = Tuple[float, float]


def distancia(p1: Point, p2: Point) -> float:
    """Calcula la distancia euclidiana entre dos puntos."""
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def fuerza_bruta(puntos: List[Point]) -> Tuple[float, Point, Point]:
    """
    Solución ingenua O(n²): compara todos los pares de puntos.
    
    Returns:
        Tupla con (distancia_minima, punto1, punto2)
    """
    n = len(puntos)
    if n < 2:
        return float('inf'), None, None
    
    min_dist = float('inf')
    p1, p2 = None, None
    
    for i in range(n):
        for j in range(i + 1, n):
            dist = distancia(puntos[i], puntos[j])
            if dist < min_dist:
                min_dist = dist
                p1, p2 = puntos[i], puntos[j]
    
    return min_dist, p1, p2


def min_distancia_franja(franja: List[Point], d: float) -> Tuple[float, Point, Point]:
    """
    Encuentra el par más cercano en la franja del medio.
    Optimización: solo compara con los siguientes 7 puntos.
    """
    min_dist = d
    p1, p2 = None, None
    franja.sort(key=lambda p: p[1])  # Ordenar por coordenada y
    
    n = len(franja)
    for i in range(n):
        # Solo necesitamos revisar hasta 7 puntos siguientes
        for j in range(i + 1, min(i + 8, n)):
            if (franja[j][1] - franja[i][1]) >= min_dist:
                break
            dist = distancia(franja[i], franja[j])
            if dist < min_dist:
                min_dist = dist
                p1, p2 = franja[i], franja[j]
    
    return min_dist, p1, p2


def closest_pair_recursivo(px: List[Point], py: List[Point]) -> Tuple[float, Point, Point]:
    """
    Algoritmo recursivo Divide & Conquer.
    
    px: puntos ordenados por x
    py: puntos ordenados por y
    
    Complejidad: O(n log n)
    """
    n = len(px)
    
    # Caso base: usar fuerza bruta para n pequeño
    if n <= 3:
        return fuerza_bruta(px)
    
    # Dividir en dos mitades
    mid = n // 2
    punto_medio = px[mid]
    
    # Dividir py en izquierda y derecha
    pyl = [p for p in py if p[0] <= punto_medio[0]]
    pyr = [p for p in py if p[0] > punto_medio[0]]
    
    # Recursión en ambas mitades
    dl, p1l, p2l = closest_pair_recursivo(px[:mid], pyl)
    dr, p1r, p2r = closest_pair_recursivo(px[mid:], pyr)
    
    # Tomar el mínimo de ambas mitades
    if dl < dr:
        d = dl
        p1, p2 = p1l, p2l
    else:
        d = dr
        p1, p2 = p1r, p2r
    
    # Construir franja de puntos cercanos a la línea divisoria
    franja = [p for p in py if abs(p[0] - punto_medio[0]) < d]
    
    # Buscar en la franja
    ds, p1s, p2s = min_distancia_franja(franja, d)
    
    if ds < d:
        return ds, p1s, p2s
    return d, p1, p2


def closest_pair(puntos: List[Point]) -> Tuple[float, Point, Point]:
    """
    Encuentra el par de puntos más cercanos usando Divide & Conquer.
    
    Args:
        puntos: Lista de tuplas (x, y)
    
    Returns:
        Tupla con (distancia_minima, punto1, punto2)
    
    Complejidad: O(n log n)
    """
    if len(puntos) < 2:
        return float('inf'), None, None
    
    # Pre-ordenar por x e y
    px = sorted(puntos, key=lambda p: p[0])
    py = sorted(puntos, key=lambda p: p[1])
    
    return closest_pair_recursivo(px, py)
