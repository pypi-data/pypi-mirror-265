# calculator-papartynas

Basic Python calculator for Turing College Data Science program's module #1, sprint #1. Supports floating point number
addition, subtraction, multiplication, division and taking nth root. Keeps track of the current calculation result.

## Installation

```shell
python3 -m pip install calculator_papartynas
```

## Examples

Import calculator module:

```python
from calculator-papartynas.calculator import Calculator
```

Perform basic mathematical operations:

```python
print(Calculator().add(2).subtract(1).multiply_by(8).divide_by(2).take_nth_root(2))
# outputs: ((0 + 2 - 1) × 8 / 2) ^ 0.5 = 2.0
```

Get calculation result:

```python
print(Calculator().add(42).result)  # outputs: 42
```

Reset memory:

```python
print(Calculator().add(1).reset_memory().add(1))  # outputs: 0 + 1 = 1
```