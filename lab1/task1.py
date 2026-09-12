import numpy as np

def f1(x: float) -> float:
    return 8*x**4 - 8*x**2 + 32*x + 1

def f2(x: float) -> float:
    return 2 - np.log10(x) - x

def tabulate_function(f: callable, a: int = -32, b: int = 32, h: int = 8) -> dict:
    # Табулювання функції f на проміжку [a, b] з кроком h
    length = (b - a) 
    tabulated_function = {}
    for x in range(a, b + 1, h):
        tabulated_function[x] = f(x)
    return tabulated_function

def table_method(f: callable) -> list:
    # Метод таблиць для знаходження інтервалів, де функція f змінює знак
    result = []
    a = -32
    b = 32
    h = 8
    tabulated_function = tabulate_function(f, a, b, h)
    items = list(tabulated_function.items())

    for i in range(len(items) - 1):
        x1, y1 = items[i]
        x2, y2 = items[i + 1]

        if y1 * y2 < 0:
            result.append((x1, x2))

    return result