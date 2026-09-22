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

    B = np.array(B)
    det = np.linalg.det(A)
    det_x = []

    for i in range(len(A)):
        A_temp = A.copy()
        A_temp[:, i] = B
        det_xi = np.linalg.det(A_temp)
        det_x.append(det_xi)

    res = np.array(det_x) / det

    return res.tolist()

A = [
    [4,2,3,1],
    [5,1,2,2],
    [6,2,4,1],
    [3,-1,2,2]
]
B = [1,2,3,4]

try: 
    kramer_method(A, B)
except ValueError as e: 
    print(f"Помилка вхідних даних: {e}")