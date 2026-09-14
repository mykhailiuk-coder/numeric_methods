import numpy as np
import matplotlib.pyplot as plt

def f1(x: float) -> float:
    return 8*x**4 - 8*x**2 + 32*x + 1

def f2(x: float) -> float:
    if x <= 0:
        print("x must be greater than 0")
        return None
    return 2 - np.log10(x) - x

def tabulate_function(f: callable, a: float = -10, b: float = 10, h: float = 1) -> dict:
    """
    Алгоритм:
    Починаючи з точки a, обчислюємо значення функції f(x) через крок h до точки b.
    Результати зберігаються у словнику, де ключами є значення x, 
    а значеннями - відповідні значення функції f(x).
    """
    tabulated_function = {}
    x = a

    while x <= b:
        tabulated_function[x] = f(x)
        x += h

    return tabulated_function

def table_method(f: callable, a: float = -10, b: float = 10, h1: float = 1.0) -> list:
    """
    Табулюємо функцію з великим кроком h1.
    Знаходимо всі інтервали зміни знака (ширші діапазони). Для кожного
    знайденого інтервалу запускаємо табуляцію з меншим кроком h2 = h1 / 2 і
    повертаємо лише вужчі інтервали.
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
    print("Ширші діапазони:", intervals)

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
    print("Вужчі діапазони:", smaller_intervals)

    return smaller_intervals

# coefs = коефіцієнти многочлена починаючи з старшого степеня до вільного члена
def analytical_method(coefs: list) -> dict:
    """
    Основна теорема алгебри: у нас є n коренів де n - найвищий степінь многочлена 
    Наслідок від неї: рівняння непарного степеня має хоча б один корінь
    Теорема Декарта: n додатних коренів = число змін знаків
    Теорема Гюа 
    Теорема про кільце коренів.
    """
    #основна теорема алгебри
    n = len(coefs) - 1

    a_n = coefs[0]
    a0 = coefs[-1]

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

def graphic_method(
    g1: callable, g2: callable, a: float, b: float, h: float = 0.01
) -> list[float]:
    """
    Знаходить наближені абсциси точок перетину графіків g1(x) та g2(x).
    """
    x_vals = np.arange(a, b + h / 2, h)
    diff = g1(x_vals) - g2(x_vals)

    roots = []
    for i in range(len(diff) - 1):
        if diff[i] * diff[i + 1] <= 0:
            x_approx = round((x_vals[i] + x_vals[i + 1]) / 2, 2)
            roots.append(x_approx)
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
    g1=lambda x: 8 * x**4 - 8 * x**2,
    g2=lambda x: -32 * x - 1,
    a=-2.2,
    b=1.2,
    title=r"Рівняння 1: $8x^4 - 8x^2 = -32x - 1$",
    g1_label=r"$y = 8x^4 - 8x^2$",
    g2_label=r"$y = -32x - 1$",
)
print("Знайдені корені для f1 графічно:", roots_f1)

roots_f2 = plot_graphical_separation(
    g1=lambda x: 2 - x,
    g2=lambda x: np.log10(x),
    a=0.2,
    b=3.5,
    title=r"Рівняння 2: $2 - x = \lg(x)$",
    g1_label=r"$y = 2 - x$",
    g2_label=r"$y = \lg(x)$",
)

print("Інтервали f2(x):", table_method(f2, a=0.5, b=4.0, h1=1.0))
print("Знайдені корені для f2 графічно:", roots_f2)

print("Інтервали f1(x):", table_method(f1))
print(analytical_method([8, 0, -8, 32, 1]))
print("Знайдені корені для f1 графічно:", roots_f1)