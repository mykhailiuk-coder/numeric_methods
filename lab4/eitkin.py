def eitkin(x_s, y_s, x, verbose=True):
    n = len(x_s)
    if n != len(y_s):
        raise ValueError("Кількість координат X та Y повинна бути однаковою!")

    table = [[0.0] * n for _ in range(n)]
    for i in range(n):
        table[i][0] = y_s[i]

    for j in range(1, n):
        for i in range(j, n):
            numerator = (
                table[i][j - 1] * (x_s[j - 1] - x)
                - table[j - 1][j - 1] * (x_s[i] - x)
            )
            denominator = x_s[j - 1] - x_s[i]
            table[i][j] = numerator / denominator

    if verbose:
        print(f"Таблиця схеми Ейткіна для x = {x}:")
        header = f"{'x_i':>8} | {'y_i':>10}" + "".join([f" | {'P_j=' + str(j):>10}" for j in range(1, n)])
        print("-" * len(header))
        print(header)
        print("-" * len(header))
        for i in range(n):
            row = f"{x_s[i]:>8.4f} | {table[i][0]:>10.4f}"
            for j in range(1, i + 1):
                row += f" | {table[i][j]:>10.4f}"
            print(row)
        print("-" * len(header))

    return table[n - 1][n - 1]

if __name__ == "__main__":
    x = [1.0, 2.0, 3.0, 4.0]
    y = [2.0, 5.0, 10.0, 17.0] 

    x_val = 2.5

    result = eitkin(x, y, x_val)
    print(f"\nЗначення інтерполяційного полінома у точці x = {x_val}: {result:.4f}")