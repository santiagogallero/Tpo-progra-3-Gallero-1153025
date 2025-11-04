"""
Problema: Mochila 0/1 (Knapsack Problem)
Programación Dinámica para maximizar el valor en una mochila con capacidad limitada.
"""
from typing import List, Tuple


def knapsack_01(pesos: List[int], valores: List[int], capacidad: int) -> int:
    """
    Mochila 0/1 usando Programación Dinámica.
    
    Args:
        pesos: Lista de pesos de los objetos
        valores: Lista de valores de los objetos
        capacidad: Capacidad máxima de la mochila
    
    Returns:
        Valor máximo alcanzable
    
    Complejidad: O(n * W) donde n = número de objetos, W = capacidad
    Espacio: O(n * W)
    """
    n = len(pesos)
    
    # Tabla DP: dp[i][w] = valor máximo usando los primeros i objetos con capacidad w
    dp = [[0] * (capacidad + 1) for _ in range(n + 1)]
    
    # Llenar la tabla
    for i in range(1, n + 1):
        for w in range(capacidad + 1):
            # No incluir el objeto i-1
            dp[i][w] = dp[i-1][w]
            
            # Incluir el objeto i-1 si cabe
            if pesos[i-1] <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w - pesos[i-1]] + valores[i-1])
    
    return dp[n][capacidad]


def knapsack_01_con_items(pesos: List[int], valores: List[int], capacidad: int) -> Tuple[int, List[int]]:
    """
    Mochila 0/1 que también retorna los objetos seleccionados.
    
    Returns:
        Tupla con (valor_maximo, lista_de_indices_seleccionados)
    """
    n = len(pesos)
    dp = [[0] * (capacidad + 1) for _ in range(n + 1)]
    
    # Llenar la tabla DP
    for i in range(1, n + 1):
        for w in range(capacidad + 1):
            dp[i][w] = dp[i-1][w]
            if pesos[i-1] <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w - pesos[i-1]] + valores[i-1])
    
    # Reconstruir la solución
    items_seleccionados = []
    w = capacidad
    for i in range(n, 0, -1):
        # Si el valor cambió, el objeto i-1 fue incluido
        if dp[i][w] != dp[i-1][w]:
            items_seleccionados.append(i-1)
            w -= pesos[i-1]
    
    items_seleccionados.reverse()
    return dp[n][capacidad], items_seleccionados


def knapsack_01_detallado(pesos: List[int], valores: List[int], capacidad: int) -> dict:
    """
    Versión detallada que muestra el proceso completo.
    
    Returns:
        Diccionario con:
        - 'valor_maximo': el valor máximo alcanzable
        - 'items_seleccionados': índices de los objetos seleccionados
        - 'peso_total': peso total de los objetos seleccionados
        - 'tabla_dp': tabla de programación dinámica
        - 'solucion_detallada': información de cada objeto seleccionado
    """
    n = len(pesos)
    dp = [[0] * (capacidad + 1) for _ in range(n + 1)]
    
    # Llenar la tabla DP
    for i in range(1, n + 1):
        for w in range(capacidad + 1):
            dp[i][w] = dp[i-1][w]
            if pesos[i-1] <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w - pesos[i-1]] + valores[i-1])
    
    # Reconstruir la solución
    items_seleccionados = []
    solucion_detallada = []
    w = capacidad
    
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            idx = i - 1
            items_seleccionados.append(idx)
            solucion_detallada.append({
                'indice': idx,
                'peso': pesos[idx],
                'valor': valores[idx],
                'relacion': valores[idx] / pesos[idx] if pesos[idx] > 0 else 0
            })
            w -= pesos[idx]
    
    items_seleccionados.reverse()
    solucion_detallada.reverse()
    
    peso_total = sum(pesos[i] for i in items_seleccionados)
    
    return {
        'valor_maximo': dp[n][capacidad],
        'items_seleccionados': items_seleccionados,
        'peso_total': peso_total,
        'capacidad_usada': f"{peso_total}/{capacidad}",
        'tabla_dp': dp,
        'solucion_detallada': solucion_detallada,
        'n_items_seleccionados': len(items_seleccionados)
    }


def knapsack_01_optimizado(pesos: List[int], valores: List[int], capacidad: int) -> int:
    """
    Versión optimizada en espacio: O(W) en lugar de O(n*W).
    Solo calcula el valor máximo, no los items.
    
    Complejidad temporal: O(n * W)
    Complejidad espacial: O(W)
    """
    dp = [0] * (capacidad + 1)
    
    for i in range(len(pesos)):
        # Recorrer de derecha a izquierda para no usar valores ya actualizados
        for w in range(capacidad, pesos[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - pesos[i]] + valores[i])
    
    return dp[capacidad]
