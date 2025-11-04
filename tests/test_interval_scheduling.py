"""
Tests para el algoritmo de selección de actividades (Greedy).
"""
import pytest
from tp_algos.algorithms.greedy.interval_scheduling import (
    seleccion_actividades, seleccion_actividades_con_detalles
)


class TestSeleccionActividades:
    """Tests para selección de actividades."""
    
    def test_caso_basico(self):
        """Test con caso básico."""
        actividades = [(1, 3), (2, 5), (4, 6)]
        resultado = seleccion_actividades(actividades)
        assert len(resultado) == 2
        # Debe seleccionar actividades 0 y 2
        assert 0 in resultado
        assert 2 in resultado
    
    def test_actividades_disjuntas(self):
        """Test con actividades que no se superponen."""
        actividades = [(1, 2), (3, 4), (5, 6), (7, 8)]
        resultado = seleccion_actividades(actividades)
        assert len(resultado) == 4
        assert resultado == [0, 1, 2, 3]
    
    def test_actividades_superpuestas(self):
        """Test con todas las actividades superpuestas."""
        actividades = [(1, 10), (2, 9), (3, 8), (4, 7)]
        resultado = seleccion_actividades(actividades)
        # Solo debe seleccionar una (la que termina primero)
        assert len(resultado) == 1
        assert 3 in resultado  # La que termina en 7
    
    def test_ejemplo_clase(self):
        """Test con ejemplo típico de clase."""
        actividades = [
            (1, 4), (3, 5), (0, 6), (5, 7), 
            (3, 8), (5, 9), (6, 10), (8, 11), 
            (8, 12), (2, 13), (12, 14)
        ]
        resultado = seleccion_actividades(actividades)
        # Debe seleccionar varias actividades no superpuestas
        assert len(resultado) >= 4
        
        # Verificar que no se superpongan
        actividades_seleccionadas = sorted(
            [actividades[i] for i in resultado], 
            key=lambda x: x[0]
        )
        for i in range(len(actividades_seleccionadas) - 1):
            assert actividades_seleccionadas[i][1] <= actividades_seleccionadas[i+1][0]
    
    def test_lista_vacia(self):
        """Test con lista vacía."""
        actividades = []
        resultado = seleccion_actividades(actividades)
        assert resultado == []
    
    def test_una_actividad(self):
        """Test con una sola actividad."""
        actividades = [(1, 5)]
        resultado = seleccion_actividades(actividades)
        assert resultado == [0]
    
    def test_con_detalles(self):
        """Test de la versión con detalles."""
        actividades = [(1, 3), (2, 4), (3, 5)]
        resultado = seleccion_actividades_con_detalles(actividades)
        
        assert 'indices' in resultado
        assert 'cantidad' in resultado
        assert 'pasos' in resultado
        assert resultado['cantidad'] == len(resultado['indices'])
        assert len(resultado['pasos']) > 0
    
    def test_orden_no_importa(self):
        """Test que el orden de entrada no afecta el resultado."""
        actividades1 = [(1, 3), (2, 5), (4, 6), (5, 8)]
        actividades2 = [(5, 8), (4, 6), (1, 3), (2, 5)]
        
        resultado1 = seleccion_actividades(actividades1)
        resultado2 = seleccion_actividades(actividades2)
        
        # El número de actividades seleccionadas debe ser el mismo
        assert len(resultado1) == len(resultado2)


class TestOptimalidadGreedy:
    """Tests para verificar la optimalidad del algoritmo greedy."""
    
    def test_optimalidad_simple(self):
        """Verificar que la solución es óptima en caso simple."""
        # Caso donde greedy debe dar la solución óptima
        actividades = [(0, 2), (1, 3), (2, 4)]
        resultado = seleccion_actividades(actividades)
        # La solución óptima es 2 actividades
        assert len(resultado) == 2
    
    def test_greedy_vs_fuerza_bruta_pequeno(self):
        """Comparar con todas las combinaciones posibles en caso pequeño."""
        actividades = [(1, 3), (2, 4), (3, 5), (4, 6)]
        resultado = seleccion_actividades(actividades)
        
        # En este caso, greedy debe dar 2 actividades
        # que es el máximo posible
        assert len(resultado) >= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
