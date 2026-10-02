import math
import numpy as np
from typing import Callable, List, Tuple

def simple_iteration_system(
    phi: Callable[[List[float]], List[float]],
    x0: List[float],
    epsilon: float = 0.001,
    max_iter: int = 1000
) -> Tuple[List[float], int]:
    """
    Реалізує метод простої ітерації для розв'язання систем нелінійних рівнянь
    
    Математична основа:
    Початкова система рівнянь F(x, y) = 0 перетворюється до еквівалентного 
    ітераційного вигляду x = Phi_1(x, y) та y = Phi_2(x, y)
    Починаючи з початкового наближення x0, кожне наступне наближення 
    обчислюється як x_{k+1} = Phi(x_k)
    Процес зупиняється, коли максимальна різниця між змінними 
    на сусідніх ітераціях стає меншою за задану точність epsilon.
    
    :param phi: Функція, що реалізує ітераційне відображення Phi(x)
    :param x0: Початкове наближення (список)
    :param epsilon: Задана точність
    :param max_iter: Максимальна кількість ітерацій
    :return: Кортеж (список знайдених коренів, кількість витрачених ітерацій)
    """
    
    # Валідація вхідних параметрів
    if epsilon <= 0:
        raise ValueError("Точність epsilon має бути строго більшою за нуль.")
    if max_iter <= 0:
        raise ValueError("Максимальна кількість ітерацій має бути додатнім цілим числом.")
    if not isinstance(x0, list) or len(x0) == 0:
        raise ValueError("Початкове наближення x0 має бути непорожнім списком.")
        
    x_prev = np.array(x0, dtype=float)
    
    for iteration in range(1, max_iter + 1):
        try:
            x_new = np.array(phi(x_prev.tolist()), dtype=float)
        except Exception as e:
            raise RuntimeError(f"Помилка обчислення функції Phi на ітерації {iteration}: {e}")
        
        # Перевірка умови зупинки
        max_diff = np.linalg.norm(x_new - x_prev, ord=np.inf)
        
        if max_diff < epsilon:
            return x_new.tolist(), iteration
            
        x_prev = x_new.copy()
        
    raise RuntimeError(f"Метод не зійшовся за {max_iter} ітерацій.")

def variant8_phi(vars: List[float]) -> List[float]:
    x, y = vars
    # Перетворення рівнянь
    # 1) x - cos(y) = 2          =>  x = 2 + cos(y)
    # 2) cos(2x - 1) + y = 0.8   =>  y = 0.8 - cos(2x - 1)
    
    new_x = 2.0 + math.cos(y)
    new_y = 0.8 - math.cos(2.0 * x - 1.0)
    
    return [new_x, new_y]

if __name__ == "__main__":
    # Початкове наближення
    # x = 2 + cos(y) -> cos() дає від -1 до 1, тому x в районі 2.
    # y = 0.8 - cos(...) -> y в районі 1.
    initial_guess = [2.0, 1.0] 
    
    try:
        solution, iters = simple_iteration_system(variant8_phi, initial_guess, epsilon=0.001)
        print(f"Знайдені корені: x = {solution[0]:.5f}, y = {solution[1]:.5f}")
        print(f"Кількість ітерацій: {iters}")
    except Exception as e:
        print("Помилка:", e)