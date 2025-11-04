"""
Tests para el algoritmo de par de puntos más cercanos.
"""
import pytest
import math
from tp_algos.algorithms.divide_conquer.closest_pair import (
    closest_pair, fuerza_bruta, distancia
)


class TestClosestPair:
    """Tests para closest_pair."""
    
    def test_dos_puntos(self):
        """Test con solo dos puntos."""
        puntos = [(0, 0), (3, 4)]
        dist, p1, p2 = closest_pair(puntos)
        assert dist == 5.0
        assert {p1, p2} == {(0, 0), (3, 4)}
    
    def test_puntos_colineales(self):
        """Test con puntos en una línea."""
        puntos = [(0, 0), (1, 0), (2, 0), (5, 0)]
        dist, p1, p2 = closest_pair(puntos)
        assert dist == 1.0
        assert {p1, p2} == {(0, 0), (1, 0)} or {p1, p2} == {(1, 0), (2, 0)}
    
    def test_puntos_identicos(self):
        """Test con puntos muy cercanos (casi idénticos)."""
        puntos = [(1.0, 1.0), (1.001, 1.001), (5, 5), (10, 10)]
        dist, p1, p2 = closest_pair(puntos)
        assert dist < 0.002
    
    def test_ejemplo_complejo(self):
        """Test con ejemplo más complejo."""
        puntos = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
        dist, p1, p2 = closest_pair(puntos)
        # El par más cercano es (2,3) y (3,4) con distancia sqrt(2)
        expected_dist = math.sqrt(2)
        assert abs(dist - expected_dist) < 0.001
    
    def test_muchos_puntos(self):
        """Test con muchos puntos."""
        puntos = [(i, i * 2) for i in range(20)]
        dist, p1, p2 = closest_pair(puntos)
        expected_dist = math.sqrt(5)  # distancia entre puntos consecutivos
        assert abs(dist - expected_dist) < 0.001
    
    def test_comparacion_fuerza_bruta(self):
        """Test que compara con solución de fuerza bruta."""
        puntos = [(1, 2), (3, 4), (5, 6), (2, 1), (8, 9), (4, 2)]
        
        dist_fb, _, _ = fuerza_bruta(puntos)
        dist_dc, _, _ = closest_pair(puntos)
        
        assert abs(dist_fb - dist_dc) < 0.001
    
    def test_puntos_en_cuadricula(self):
        """Test con puntos en cuadrícula."""
        puntos = [(i, j) for i in range(5) for j in range(5)]
        dist, p1, p2 = closest_pair(puntos)
        # En una cuadrícula unitaria, la distancia mínima es 1
        assert dist == 1.0
    
    def test_caso_borde_lista_vacia(self):
        """Test con lista vacía."""
        puntos = []
        dist, p1, p2 = closest_pair(puntos)
        assert dist == float('inf')
        assert p1 is None
        assert p2 is None
    
    def test_un_punto(self):
        """Test con un solo punto."""
        puntos = [(1, 1)]
        dist, p1, p2 = closest_pair(puntos)
        assert dist == float('inf')
        assert p1 is None
        assert p2 is None


class TestDistancia:
    """Tests para la función de distancia."""
    
    def test_distancia_basica(self):
        """Test de distancia básica."""
        assert distancia((0, 0), (3, 4)) == 5.0
    
    def test_distancia_cero(self):
        """Test de distancia entre el mismo punto."""
        assert distancia((1, 1), (1, 1)) == 0.0
    
    def test_distancia_horizontal(self):
        """Test de distancia horizontal."""
        assert distancia((0, 0), (5, 0)) == 5.0
    
    def test_distancia_vertical(self):
        """Test de distancia vertical."""
        assert distancia((0, 0), (0, 5)) == 5.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
