import numpy as np

"""
A - матриця коефіцієнтів
В - вектор вільних членів
"""
def kramer_method(A: list[list[float | int]], B: list[float | int]) -> list[float]:
    # Валідація вхідних даних
    if len(A) != len(B): 
        raise ValueError("Кількість рядків не дорівнює кількості вільних членів")
    A = np.array(A)
    rows, cols = A.shape
    if rows != cols:
        raise ValueError("Матриця не є квадратною")
    if np.linalg.det(A) == 0:
        raise ValueError("Початковий визначник дорівнює нулю")

    # Алгоритм
    B = np.array(B)
    det = np.linalg.det(A)
    det_x = []
    for i in range(len(A)):
        A_temp = A.copy()
        A_temp[:, i] = B
        det_xi = np.linalg.det(A_temp)
        det_x.append(det_xi)

    res = np.array(det_x) / det
    return np.round(res.tolist(), 16)

"""
A - матриця коефіцієнтів
В - вектор вільних членів
"""
def matrix_method(A: list[list[float | int]], B: list[float | int]) -> list[float]:
    # Валідація вхідних даних
    if len(A) != len(B): 
        raise ValueError("Кількість рядків не дорівнює кількості вільних членів")
    A = np.array(A)
    rows, cols = A.shape
    if rows != cols:
        raise ValueError("Матриця не є квадратною")
    if np.linalg.det(A) == 0:
        raise ValueError("Початковий визначник дорівнює нулю")  

    # Алгоритм
    B = np.array(B)
    A_inverse = np.linalg.inv(A)
    x = A_inverse @ B
    return np.round(x.tolist(), 16)

A = [
    [4,2,3,1],
    [5,1,2,2],
    [6,2,4,1],
    [3,-1,2,2]
]
B = [1,3,0,1]
try: 
    kramer_solution = kramer_method(A, B)
    print("Розв'язок методом Крамера: ", kramer_solution)
    matrix_solution = matrix_method(A, B)
    print("Розв'язок матричним методом: ", matrix_solution)
    numpy_solution = np.linalg.solve(np.array(A), np.array(B))
    print("Розв'язок з допомогою numpy solver:", numpy_solution)
except ValueError as e: 
    print(f"Помилка вхідних даних: {e}")