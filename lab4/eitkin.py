def aitken(x_s, y_s, x, eps=0.01, verbose=True):
    n = len(x_s)
    P = [[0.0] * n for _ in range(n)]

    if len(x_s) != len(y_s):
        raise ValueError("Помилка: неправильно задана таблична функція")

    if x > max(x_s) or x < min(x_s):
        raise ValueError("Помилка: інтерполяція не проводиться поза межами табличної функції")

    for i in range(n):
        P[i][0] = y_s[i]

    last_j = n - 1

    for j in range(1, n):
        for i in range(j, n):
            P[i][j] = (
                P[j - 1][j - 1] * (x_s[i] - x) - P[i][j - 1] * (x_s[j - 1] - x)
            ) / (x_s[i] - x_s[j - 1])
        if abs(P[j][j] - P[j - 1][j - 1]) < eps:
            last_j = j
            break

    res = P[last_j][last_j]

    if verbose:
        print(f"Таблиця схеми Ейткіна для x = {x}:")
        header = f"{'x_i':>8} | {'y_i':>10}" + "".join([f" | {'P_j=' + str(col):>10}" for col in range(1, last_j + 1)])
        print("-" * len(header))
        print(header)
        print("-" * len(header))
        for i in range(n):
            row = f"{x_s[i]:>8.2f} | {P[i][0]:>10.2f}"
            for col in range(1, min(i + 1, last_j + 1)):
                row += f" | {P[i][col]:>10.2f}"
            print(row)
        print("-" * len(header))

    return round(res, 2)


# Початкові вузли
x_s = [0.0, 1.0, 2.0, 3.0]
y_s = [1.0, 3.0, 9.0, 19.0]

try:
    result = aitken(x_s, y_s, x=1.5, eps=0.01, verbose=True)
    print(f"Результат: {result:.2f}")
except ValueError as e:
    print(e)