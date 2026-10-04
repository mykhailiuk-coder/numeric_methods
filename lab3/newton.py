import numpy as np
from typing import Callable, Tuple

def newton_system(
        func: Callable[[np.ndarray], np.ndarray],
        jacobian: Callable[[np.ndarray], np.ndarray],
        x0: np.ndarray,
        tol: float = 1e-6,
        max_iter: int = 100
) -> Tuple[np.ndarray, int]:
    """
    Метод Ньютона для розв'язання системи нелінійних рівнянь.

    Алгоритм ітеративно знаходить вектор x, для якого F(x) = 0, використовуючи
    формулу x_{k+1} = x_k - J(x_k)^{-1} * F(x_k). Для обчислювальної стабільності
    замість обернення матриці розв'язується СЛАР: J(x_k) * dx = -F(x_k),
    після чого вектор наближень оновлюється: x_{k+1} = x_k + dx.
    """
    x = np.array(x0, dtype=float)

    for i in range(max_iter):
        f_val = func(x)

        # Перевірка умови збіжності за нев'язкою
        if np.linalg.norm(f_val, ord=np.inf) < tol:
            return x, i

        # Обчислення матриці Якобі та приросту dx
        J = jacobian(x)
        dx = np.linalg.solve(J, -f_val)
        x = x + dx

        # Перевірка умови збіжності за приростом аргументу
        if np.linalg.norm(dx, ord=np.inf) < tol:
            return x, i + 1

    raise ValueError("Метод Ньютона не зійшовся за задану кількість ітерацій")