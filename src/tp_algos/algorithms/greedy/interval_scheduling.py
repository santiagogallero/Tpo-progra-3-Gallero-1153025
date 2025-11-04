"""
Problema: Selección de actividades (Interval Scheduling)
Algoritmo Greedy para maximizar el número de actividades no superpuestas.
"""
from typing import List, Tuple

Actividad = Tuple[int, int, int]  # (inicio, fin, id)


def seleccion_actividades(actividades: List[Tuple[int, int]]) -> List[int]:
    """
    Algoritmo Greedy: selecciona la máxima cantidad de actividades no superpuestas.
    
    Estrategia: Ordenar por tiempo de fin y seleccionar siempre la que termine primero.
    
    Args:
        actividades: Lista de tuplas (inicio, fin)
    
    Returns:
        Lista de índices de las actividades seleccionadas
    
    Complejidad: O(n log n) por el ordenamiento
    
    Justificación de corrección:
    - La elección greedy es seleccionar siempre la actividad que termine primero.
    - Esto maximiza el tiempo disponible para futuras actividades.
    - Demostración por intercambio: cualquier solución óptima puede transformarse
      en nuestra solución greedy sin perder optimalidad.
    """
    if not actividades:
        return []
    
    # Crear lista con índices
    actividades_indexadas = [(inicio, fin, i) for i, (inicio, fin) in enumerate(actividades)]
    
    # Ordenar por tiempo de fin (estrategia greedy)
    actividades_indexadas.sort(key=lambda x: x[1])
    
    seleccionadas = []
    ultimo_fin = -1
    
    for inicio, fin, idx in actividades_indexadas:
        # Si la actividad no se superpone con la última seleccionada
        if inicio >= ultimo_fin:
            seleccionadas.append(idx)
            ultimo_fin = fin
    
    return seleccionadas


def seleccion_actividades_con_detalles(actividades: List[Tuple[int, int]]) -> dict:
    """
    Versión extendida que retorna información detallada del proceso.
    
    Returns:
        Diccionario con:
        - 'indices': lista de índices seleccionados
        - 'actividades': lista de actividades seleccionadas
        - 'cantidad': número de actividades seleccionadas
        - 'pasos': información del proceso paso a paso
    """
    if not actividades:
        return {
            'indices': [],
            'actividades': [],
            'cantidad': 0,
            'pasos': []
        }
    
    actividades_indexadas = [(inicio, fin, i) for i, (inicio, fin) in enumerate(actividades)]
    actividades_indexadas.sort(key=lambda x: x[1])
    
    seleccionadas = []
    seleccionadas_detalles = []
    pasos = []
    ultimo_fin = -1
    
    pasos.append(f"Actividades ordenadas por tiempo de fin: {[(a[0], a[1], a[2]) for a in actividades_indexadas]}")
    
    for inicio, fin, idx in actividades_indexadas:
        if inicio >= ultimo_fin:
            seleccionadas.append(idx)
            seleccionadas_detalles.append((inicio, fin))
            pasos.append(f"✓ Seleccionar actividad {idx}: [{inicio}, {fin}] (no se superpone)")
            ultimo_fin = fin
        else:
            pasos.append(f"✗ Rechazar actividad {idx}: [{inicio}, {fin}] (se superpone, inicia antes de {ultimo_fin})")
    
    return {
        'indices': seleccionadas,
        'actividades': seleccionadas_detalles,
        'cantidad': len(seleccionadas),
        'pasos': pasos
    }
