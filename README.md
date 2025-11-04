# TP Algoritmos – Entrega

Este repositorio contiene el código fuente del TP. Todo lo no-código (análisis, pseudocódigo, explicaciones, modelado, discusión y casos de prueba) está unificado en:

- Informe: `docs/informe-tp.md` (exportable a PDF)

## Requisitos

- Python 3.10+
- pip

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

```bash
# incluir src en el PYTHONPATH
PYTHONPATH=$(pwd)/src python3 -m tp_algos.main
```

## Tests

```bash
pytest -q
```

## Exportar informe a PDF (opcional)

```bash
pandoc docs/informe-tp.md -o docs/informe-tp.pdf \
    --from gfm --toc --number-sections \
    -V geometry:margin=1in -V mainfont="Helvetica"
```

## Estructura mínima

```
src/
    tp_algos/
        main.py
        algorithms/
            divide_conquer/closest_pair.py
            greedy/interval_scheduling.py
            dp/knapsack_01.py
            graphs/floyd_warshall.py
tests/
    test_closest_pair.py
    test_interval_scheduling.py
    test_knapsack.py
    test_floyd_warshall.py
docs/
    informe-tp.md
```
