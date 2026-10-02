import numpy as np
# я просив не підключати сторонні ліби для типізації
from typing import Callable, Tuple

# де базова валідація? 
def newton_system(
        func: Callable[[np.ndarray], np.ndarray],
        jacobian: Callable[[np.ndarray], np.ndarray],
        x0: np.ndarray,
        # точність 0.001 має бути
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
            return x, i + 1 # повертай також масив значень з кожною ітерацією, це потрібно для візуалізації, дякую)

    raise ValueError("Метод Ньютона не зійшовся за задану кількість ітерацій")


if __name__ == "__main__":
    # Тестова система:
    # 1) x1 + x2 - 3 = 0
    # 2) x1^2 + x2^2 - 5 = 0
    def system_equations(x: np.ndarray) -> np.ndarray:
        return np.array([
            x[0] + x[1] - 3.0,
            x[0] ** 2 + x[1] ** 2 - 5.0
        ])


    def system_jacobian(x: np.ndarray) -> np.ndarray:
        return np.array([
            [1.0, 1.0],
            [2.0 * x[0], 2.0 * x[1]]
        ])

    # Пошук першого розв'язку (1, 2)
    # не обробляються винятки
    # немає нашого прикладу
    initial_guess_1 = np.array([0.0, 5.0])
    solution_1, iterations_1 = newton_system(system_equations, system_jacobian, initial_guess_1)
    print(f"Корінь 1: {solution_1}")
    print(f"Кількість ітерацій: {iterations_1}\n")

    # Пошук другого розв'язку (2, 1)
    # не обробляються винятки
    # немає нашого прикладу
    initial_guess_2 = np.array([5.0, 0.0])
    solution_2, iterations_2 = newton_system(system_equations, system_jacobian, initial_guess_2)
    print(f"Корінь 2: {solution_2}")
    print(f"Кількість ітерацій: {iterations_2}")