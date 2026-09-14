import numpy as np
import matplotlib.pyplot as plt

def f1(x: float) -> float:
    return x**4 - 2*x**3 + x - 1.5

def f2(x: float) -> float:
    return np.sin(x) - x + 0.25

def tabulate_function(f: callable, a: float, b: float, h: float = 1) -> dict:
    """
    Починаючи з точки a, обчислюємо значення функції f(x) через крок h до точки b.
    Результати зберігаються у словнику, де ключами є значення x, 
    а значеннями - відповідні значення функції f(x).
    """
    tabulated_function = {}
    x = a

    num_steps = int(round((b - a) / h)) + 1

    for i in range(num_steps):
        x = round(a + i * h, 10)
        tabulated_function[x] = f(x)

    return tabulated_function

def table_method(f: callable, a: float, b: float, h1: float = 1.0) -> list:
    """
    Табулюємо функцію з великим кроком h1.
    Знаходимо всі інтервали зміни знака (ширші діапазони). Для кожного
    знайденого інтервалу запускаємо табуляцію з меншим кроком h2 = h1 / 2 і
    повертаємо вужчі інтервали.
    """
    intervals = []
    smaller_intervals = []

    tabulated_function = tabulate_function(f, a, b, h1)
    items = list(tabulated_function.items())

    for i in range(len(items) - 1):
        x1, y1 = items[i]
        x2, y2 = items[i + 1]
        if y1 * y2 < 0:
            intervals.append((x1, x2))
    # Прибери в коментарі, якщо не хочеш бачити ширші діапазони
    # print("Ширші діапазони:", intervals)

    h2 = h1 / 2
    for x, y in intervals:
        tabulated_function = tabulate_function(f, x, y, h2)
        items = list(tabulated_function.items())

        for i in range(len(items) - 1):
            x1, y1 = items[i]
            x2, y2 = items[i + 1]
            if y1 * y2 < 0:
                smaller_intervals.append((x1, x2))
    # Прибери в коментарі, якщо не хочеш бачити вужчі діапазони
    # print("Вужчі діапазони:", smaller_intervals)

    return smaller_intervals

# coefs = коефіцієнти многочлена починаючи з старшого степеня до вільного члена
def analytical_method(coefs: list) -> dict:
    """
    Основна теорема алгебри: у нас є n коренів де n - найвищий степінь многочлена 
    Наслідок від неї: рівняння непарного степеня має хоча б один корінь
    Теорема Декарта: n додатних коренів = число змін знаків коефіцієнтів
    Теорема Гюа: якщо всі корені дійсні, тоді квадрат будь-якого коефіцієнта(крім крайніх) більший за 
    Теорема про кільце коренів: корені многочлена містяться в кільці(рядок 110).
    """
    # Основна теорема алгебри
    n = len(coefs) - 1

    a_n = coefs[0]
    a0 = coefs[-1]

    # Наслідок з основної теореми алгебри
    has_real_guaranteed = n % 2 != 0

    # Теорема Декарта: додатні корені 
    non_zero_pos = [c for c in coefs if c != 0]
    pos_roots_changes = 0
    for i in range(len(non_zero_pos) - 1):
        if non_zero_pos[i] * non_zero_pos[i + 1] < 0:
            pos_roots_changes += 1

    # Теорема Декарта: від'ємні корені 
    neg_coefs = [(-c if (n - i) % 2 != 0 else c) for i, c in enumerate(coefs)]
    non_zero_neg = [c for c in neg_coefs if c != 0]
    neg_roots_changes = 0
    for i in range(len(non_zero_neg) - 1):
        if non_zero_neg[i] * non_zero_neg[i + 1] < 0:
            neg_roots_changes += 1

    # Теорема Гюа 
    all_roots_real = True
    for k in range(1, n):
        if coefs[k] ** 2 <= coefs[k - 1] * coefs[k + 1]:
            all_roots_real = False
            break

    # Кільце коренів
    a = max(abs(x) for x in coefs[1:])
    b = max(abs(x) for x in coefs[:-1])

    lower_bound = abs(a0) / (abs(a0) + b)
    upper_bound = 1 + a / abs(a_n)
    ring = (round(lower_bound, 4), round(upper_bound, 4))

    return {
        "total_roots": n,
        "has_real_guaranteed": has_real_guaranteed,
        "pos_roots_max": pos_roots_changes,
        "neg_roots_max": neg_roots_changes,
        "all_roots_real_necessary": all_roots_real,
        "ring": ring,
    }

def f1_left(x):
    return 8 * x**4 - 8 * x**2

def f1_right(x):
    return -32 * x - 1

def f2_left(x):
    return 2 - x

def f2_right(x):
    return np.log10(x)

"""
g1, g2 - елементарні функції які легше зобразити на графіку, 
такі щоб f(x) = g1(x) - g2(x)
"""
def graphic_method(
    g1: callable, g2: callable, a: float, b: float, h: float = 0.01
) -> list[float]:
    """
    Приблизний розв'язок - середина діапазону 
    де різниця значень двох функцій 
    на кінцях має різний знак, 
    для кращої точності задаємо малий крок h
    """
    x_vals = np.arange(a, b + h / 2, h)
    diff = g1(x_vals) - g2(x_vals)

    roots = []
    for i in range(len(diff) - 1):
        if diff[i] * diff[i + 1] <= 0:
            x_approx = round((x_vals[i] + x_vals[i + 1]) / 2, 2)
            roots.append(x_approx)

    for i in range(len(roots)):
        roots[i] = float(roots[i])
        
    return roots

def plot_graphical_separation(
    g1: callable,
    g2: callable,
    a: float,
    b: float,
    title: str = "",
    g1_label: str = "y1",
    g2_label: str = "y2",
):
    
    roots = graphic_method(g1, g2, a, b)

    x_vals = np.linspace(a, b, 500)
    plt.figure(figsize=(7, 4.5))
    plt.plot(x_vals, g1(x_vals), label=g1_label, color="tab:blue", lw=2)
    plt.plot(
        x_vals,
        g2(x_vals),
        label=g2_label,
        color="tab:red",
        linestyle="--",
        lw=2,
    )

    for r in roots:
        y_val = g1(r)
        plt.scatter([r], [y_val], color="green", s=50, zorder=5)
        plt.annotate(
            f"x ≈ {r}",
            (r, y_val),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontweight="bold",
        )

    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return roots

roots_f1 = plot_graphical_separation(
    g1=lambda x: x**4 - 2*x**3,
    g2=lambda x: -x + 1.5,
    a=-2.2,
    b=1.2,
    title=r"Рівняння 1: $x^4 - 2x^3 + x - 1.5$",
    g1_label=r"$y = x^4 - 2x^3$",
    g2_label=r"$y = -x + 1.5$",
)

roots_f2 = plot_graphical_separation(
    g1=lambda x: np.sin(x),
    g2=lambda x: x - 0.25,
    a=0.2,
    b=3.5,
    title=r"Рівняння 2: $sin(x) - x + 0.25$",
    g1_label=r"$y = sin(x)$",
    g2_label=r"$y = x - 0.25$",
)

print("Табличні інтервали f1(x):", table_method(f1, a=-10, b = 10))
print("Аналітичний висновок f1(x)", analytical_method([1, -2, 0, 1, -1.5]))
print("Знайдені корені для f1(x) графічно:", roots_f1)

print("Табличні інтервали f2(x):", table_method(f2, a=0.5, b=4.0, h1=1.0))
print("Знайдені корені для f2 графічно:", roots_f2)