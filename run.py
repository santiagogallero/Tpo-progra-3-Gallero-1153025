#!/usr/bin/env python3
"""
Script de ejecución del TP Algoritmos.
Configura el PYTHONPATH y ejecuta el programa principal.
"""
import sys
import os

# Agregar src al path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

# Importar y ejecutar main
from tp_algos.main import main

if __name__ == "__main__":
    main()
