"""
Tests para el algoritmo de Mochila 0/1 (Knapsack).
"""
import pytest
from tp_algos.algorithms.dp.knapsack_01 import (
    knapsack_01, knapsack_01_con_items, knapsack_01_detallado, knapsack_01_optimizado
)


class TestKnapsack01:
    """Tests para el algoritmo de mochila 0/1."""
    
    def test_ejemplo_enunciado(self):
        """Test con el ejemplo del enunciado."""
        pesos = [6, 3, 4]
        valores = [30, 14, 16]
        capacidad = 10
        
        resultado = knapsack_01(pesos, valores, capacidad)
        # La solución óptima es O2 + O3 = 14 + 16 = 30
        assert resultado == 30
    
    def test_ejemplo_simple(self):
        """Test con ejemplo simple."""
        pesos = [2, 3, 4, 5]
        valores = [3, 4, 5, 6]
        capacidad = 8
        
        resultado = knapsack_01(pesos, valores, capacidad)
        # Mejor combinación: objetos 1 y 3 (peso=3+5=8, valor=4+6=10)
        assert resultado == 10
    
    def test_capacidad_cero(self):
        """Test con capacidad cero."""
        pesos = [1, 2, 3]
        valores = [10, 20, 30]
        capacidad = 0
        
        resultado = knapsack_01(pesos, valores, capacidad)
        assert resultado == 0
    
    def test_sin_objetos(self):
        """Test sin objetos."""
        pesos = []
        valores = []
        capacidad = 10
        
        resultado = knapsack_01(pesos, valores, capacidad)
        assert resultado == 0
    
    def test_un_objeto_cabe(self):
        """Test con un objeto que cabe."""
        pesos = [5]
        valores = [100]
        capacidad = 10
        
        resultado = knapsack_01(pesos, valores, capacidad)
        assert resultado == 100
    
    def test_un_objeto_no_cabe(self):
        """Test con un objeto que no cabe."""
        pesos = [15]
        valores = [100]
        capacidad = 10
        
        resultado = knapsack_01(pesos, valores, capacidad)
        assert resultado == 0
    
    def test_todos_objetos_caben(self):
        """Test donde todos los objetos caben."""
        pesos = [1, 2, 3]
        valores = [10, 20, 30]
        capacidad = 10
        
        resultado = knapsack_01(pesos, valores, capacidad)
        # Debe tomar todos: valor = 60
        assert resultado == 60
    
    def test_objetos_identicos(self):
        """Test con objetos idénticos."""
        pesos = [5, 5, 5]
        valores = [10, 10, 10]
        capacidad = 12
        
        resultado = knapsack_01(pesos, valores, capacidad)
        # Puede tomar 2 objetos: valor = 20
        assert resultado == 20


class TestKnapsackConItems:
    """Tests para knapsack con reconstrucción de items."""
    
    def test_reconstruccion_items_ejemplo_enunciado(self):
        """Test de reconstrucción con ejemplo del enunciado."""
        pesos = [6, 3, 4]
        valores = [30, 14, 16]
        capacidad = 10
        
        valor, items = knapsack_01_con_items(pesos, valores, capacidad)
        
        assert valor == 30
        assert set(items) == {1, 2}  # Objetos O2 y O3
        
        # Verificar que no excede la capacidad
        peso_total = sum(pesos[i] for i in items)
        assert peso_total <= capacidad
    
    def test_reconstruccion_items_simple(self):
        """Test de reconstrucción simple."""
        pesos = [2, 3, 4, 5]
        valores = [3, 4, 5, 6]
        capacidad = 8
        
        valor, items = knapsack_01_con_items(pesos, valores, capacidad)
        
        # Verificar valor
        assert valor == 10
        
        # Verificar que los items suman el valor correcto
        valor_calculado = sum(valores[i] for i in items)
        assert valor_calculado == valor
        
        # Verificar capacidad
        peso_total = sum(pesos[i] for i in items)
        assert peso_total <= capacidad
    
    def test_un_item_optimo(self):
        """Test donde la solución óptima es un solo item."""
        pesos = [5, 10, 3]
        valores = [100, 10, 20]
        capacidad = 6
        
        valor, items = knapsack_01_con_items(pesos, valores, capacidad)
        
        assert valor == 100
        assert items == [0]


class TestKnapsackDetallado:
    """Tests para la versión detallada."""
    
    def test_informacion_completa(self):
        """Test que verifica toda la información retornada."""
        pesos = [2, 3, 4]
        valores = [3, 4, 5]
        capacidad = 5
        
        resultado = knapsack_01_detallado(pesos, valores, capacidad)
        
        # Verificar que contiene todas las claves esperadas
        assert 'valor_maximo' in resultado
        assert 'items_seleccionados' in resultado
        assert 'peso_total' in resultado
        assert 'tabla_dp' in resultado
        assert 'solucion_detallada' in resultado
        
        # Verificar consistencia
        peso_calculado = sum(pesos[i] for i in resultado['items_seleccionados'])
        assert peso_calculado == resultado['peso_total']
        assert peso_calculado <= capacidad


class TestKnapsackOptimizado:
    """Tests para la versión optimizada en espacio."""
    
    def test_mismo_resultado_que_version_normal(self):
        """Verificar que da el mismo resultado que la versión normal."""
        pesos = [6, 3, 4, 2, 5]
        valores = [30, 14, 16, 10, 25]
        capacidad = 10
        
        resultado_normal = knapsack_01(pesos, valores, capacidad)
        resultado_optimizado = knapsack_01_optimizado(pesos, valores, capacidad)
        
        assert resultado_normal == resultado_optimizado
    
    def test_varios_casos(self):
        """Test con varios casos."""
        casos = [
            ([1, 2, 3], [10, 15, 40], 6),
            ([5, 4, 6, 3], [10, 40, 30, 50], 10),
            ([2, 3, 4, 5], [3, 4, 5, 6], 8),
        ]
        
        for pesos, valores, capacidad in casos:
            resultado_normal = knapsack_01(pesos, valores, capacidad)
            resultado_optimizado = knapsack_01_optimizado(pesos, valores, capacidad)
            assert resultado_normal == resultado_optimizado


class TestCasosEspeciales:
    """Tests para casos especiales y edge cases."""
    
    def test_valor_cero(self):
        """Test con valores cero."""
        pesos = [1, 2, 3]
        valores = [0, 0, 0]
        capacidad = 5
        
        resultado = knapsack_01(pesos, valores, capacidad)
        assert resultado == 0
    
    def test_peso_uno_capacidad_grande(self):
        """Test con pesos unitarios y capacidad grande."""
        n = 10
        pesos = [1] * n
        valores = list(range(1, n + 1))
        capacidad = 5
        
        resultado = knapsack_01(pesos, valores, capacidad)
        # Debe tomar los 5 de mayor valor: 10+9+8+7+6 = 40
        assert resultado == sum(range(6, 11))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
