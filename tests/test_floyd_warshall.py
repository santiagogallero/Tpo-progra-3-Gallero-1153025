"""
Tests para el algoritmo Floyd-Warshall.
"""
import pytest
from tp_algos.algorithms.graphs.floyd_warshall import (
    floyd_warshall, reconstruir_camino, floyd_warshall_detallado,
    crear_grafo_vacio
)


class TestFloydWarshall:
    """Tests para el algoritmo Floyd-Warshall."""
    
    def test_grafo_simple(self):
        """Test con grafo simple de 3 nodos."""
        # Grafo: 0 -> 1 (peso 4), 1 -> 2 (peso 3), 0 -> 2 (peso 10)
        grafo = crear_grafo_vacio(3)
        grafo[0][1] = 4
        grafo[1][2] = 3
        grafo[0][2] = 10
        
        dist, _ = floyd_warshall(grafo)
        
        # Verificar distancias
        assert dist[0][1] == 4
        assert dist[1][2] == 3
        assert dist[0][2] == 7  # 0->1->2 es mejor que 0->2
    
    def test_grafo_completo_pequeno(self):
        """Test con grafo completo de 4 nodos."""
        n = 4
        grafo = crear_grafo_vacio(n)
        
        # Crear grafo completo con pesos
        grafo[0][1] = 5
        grafo[0][2] = 10
        grafo[0][3] = 15
        grafo[1][2] = 3
        grafo[1][3] = 20
        grafo[2][3] = 2
        
        dist, _ = floyd_warshall(grafo)
        
        # Verificar algunas distancias
        assert dist[0][1] == 5
        assert dist[0][2] == 8  # 0->1->2
        assert dist[0][3] == 10  # 0->1->2->3
    
    def test_grafo_sin_aristas(self):
        """Test con grafo sin aristas."""
        n = 3
        grafo = crear_grafo_vacio(n)
        
        dist, _ = floyd_warshall(grafo)
        
        # Solo debe haber caminos de cada nodo a sí mismo
        for i in range(n):
            assert dist[i][i] == 0
            for j in range(n):
                if i != j:
                    assert dist[i][j] == float('inf')
    
    def test_grafo_con_un_nodo(self):
        """Test con grafo de un solo nodo."""
        grafo = [[0]]
        
        dist, _ = floyd_warshall(grafo)
        
        assert dist[0][0] == 0
    
    def test_camino_indirecto_mas_corto(self):
        """Test donde el camino indirecto es más corto."""
        grafo = crear_grafo_vacio(3)
        grafo[0][1] = 100
        grafo[1][2] = 100
        grafo[0][2] = 1
        grafo[2][1] = 1
        
        dist, _ = floyd_warshall(grafo)
        
        # 0->1 directo es 100, pero 0->2->1 es 2
        assert dist[0][1] == 2
    
    def test_grafo_direccionado(self):
        """Test con grafo direccionado."""
        grafo = crear_grafo_vacio(3)
        grafo[0][1] = 5
        grafo[1][2] = 3
        # No hay arista de vuelta
        
        dist, _ = floyd_warshall(grafo)
        
        assert dist[0][1] == 5
        assert dist[1][0] == float('inf')  # No hay camino de vuelta


class TestReconstruirCamino:
    """Tests para la reconstrucción de caminos."""
    
    def test_reconstruir_camino_directo(self):
        """Test de reconstrucción con camino directo."""
        grafo = crear_grafo_vacio(3)
        grafo[0][1] = 5
        grafo[1][2] = 3
        
        _, next_node = floyd_warshall(grafo)
        camino = reconstruir_camino(next_node, 0, 1)
        
        assert camino == [0, 1]
    
    def test_reconstruir_camino_indirecto(self):
        """Test de reconstrucción con camino indirecto."""
        grafo = crear_grafo_vacio(4)
        grafo[0][1] = 1
        grafo[1][2] = 1
        grafo[2][3] = 1
        
        _, next_node = floyd_warshall(grafo)
        camino = reconstruir_camino(next_node, 0, 3)
        
        assert camino == [0, 1, 2, 3]
    
    def test_reconstruir_sin_camino(self):
        """Test cuando no hay camino."""
        grafo = crear_grafo_vacio(3)
        grafo[0][1] = 5
        # No hay camino de 1 a 2
        
        _, next_node = floyd_warshall(grafo)
        camino = reconstruir_camino(next_node, 1, 2)
        
        assert camino == []
    
    def test_reconstruir_camino_mismo_nodo(self):
        """Test de camino de un nodo a sí mismo."""
        grafo = crear_grafo_vacio(2)
        grafo[0][1] = 5
        
        _, next_node = floyd_warshall(grafo)
        camino = reconstruir_camino(next_node, 0, 0)
        
        # El camino debe estar vacío o contener solo el nodo origen
        assert camino == [] or camino == [0]


class TestFloydWarshallDetallado:
    """Tests para la versión detallada."""
    
    def test_informacion_completa(self):
        """Test que verifica toda la información retornada."""
        grafo = crear_grafo_vacio(3)
        grafo[0][1] = 4
        grafo[1][2] = 3
        grafo[0][2] = 10
        
        nombres = ["A", "B", "C"]
        resultado = floyd_warshall_detallado(grafo, nombres)
        
        # Verificar que contiene todas las claves esperadas
        assert 'matriz_distancias' in resultado
        assert 'nombres_nodos' in resultado
        assert 'pasos' in resultado
        assert 'todos_caminos' in resultado
        assert 'next_node' in resultado
        
        # Verificar que los nombres son correctos
        assert resultado['nombres_nodos'] == nombres
        
        # Verificar que hay pasos registrados
        assert len(resultado['pasos']) > 0
    
    def test_todos_caminos(self):
        """Test que verifica que todos los caminos son generados."""
        grafo = crear_grafo_vacio(3)
        grafo[0][1] = 5
        grafo[1][2] = 3
        grafo[0][2] = 10
        
        nombres = ["X", "Y", "Z"]
        resultado = floyd_warshall_detallado(grafo, nombres)
        
        # Debe haber caminos para todos los pares (excepto a sí mismos)
        assert 'X_a_Y' in resultado['todos_caminos']
        assert 'X_a_Z' in resultado['todos_caminos']
        assert 'Y_a_Z' in resultado['todos_caminos']
        
        # Verificar que el camino X->Z es correcto
        camino_xz = resultado['todos_caminos']['X_a_Z']
        assert camino_xz['distancia'] == 8  # X->Y->Z
        assert camino_xz['camino'] == ['X', 'Y', 'Z']


class TestCrearGrafoVacio:
    """Tests para la función de crear grafo vacío."""
    
    def test_crear_grafo_dimension_correcta(self):
        """Test que crea un grafo de tamaño correcto."""
        n = 5
        grafo = crear_grafo_vacio(n)
        
        assert len(grafo) == n
        assert all(len(fila) == n for fila in grafo)
    
    def test_crear_grafo_diagonal_ceros(self):
        """Test que la diagonal son ceros."""
        n = 4
        grafo = crear_grafo_vacio(n)
        
        for i in range(n):
            assert grafo[i][i] == 0
    
    def test_crear_grafo_resto_infinito(self):
        """Test que el resto son infinitos."""
        n = 3
        grafo = crear_grafo_vacio(n)
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    assert grafo[i][j] == float('inf')


class TestCasosReales:
    """Tests con casos de uso reales."""
    
    def test_red_ciudades(self):
        """Test simulando una red de ciudades."""
        # 4 ciudades: A, B, C, D
        grafo = crear_grafo_vacio(4)
        
        # Conexiones (bidireccionales)
        conexiones = [
            (0, 1, 50),   # A-B: 50km
            (1, 2, 30),   # B-C: 30km
            (2, 3, 20),   # C-D: 20km
            (0, 3, 150),  # A-D: 150km (directo)
        ]
        
        for origen, destino, distancia in conexiones:
            grafo[origen][destino] = distancia
            grafo[destino][origen] = distancia  # Bidireccional
        
        dist, next_node = floyd_warshall(grafo)
        
        # A->D directo es 150, pero A->B->C->D es 100
        assert dist[0][3] == 100
        
        # Reconstruir el camino óptimo
        camino = reconstruir_camino(next_node, 0, 3)
        assert camino == [0, 1, 2, 3]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
