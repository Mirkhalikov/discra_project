import numpy as np


def compare_arrs(arr1, arr2):  # для праоверки монотонности
    '''
    Eсли второй массив >= первого, возвращает 2,
    Eсли  первый >= второго, возвращает 1,
    Eсли они не сравнимы, возвращает 0.
    Случай равенства не рассмаривается
    '''
    arr1 = np.array(arr1)
    arr2 = np.array(arr2)
    if np.all((arr2 - arr1) >= 0):
        return 2
    elif np.all((arr2 - arr1) <= 0):
        return 1
    return 0


def is_monotonic(table):
    '''Проверяет монотонность ф-ии по таблице истинности'''
    M, N = table.shape
    for i in range(M):
        for j in range(i + 1, M):
            if compare_arrs(table[i:i + 1, :N - 1].tolist(), table[j:j + 1, :N - 1].tolist()) == 2:
                if table[i:i + 1, N - 1] > table[j:j + 1, N - 1]: return False
    return True


def f(function):
    func = function
    func = func.replace('!', 'not ').replace('->', ' <= ').replace('~', ' == ').replace('*', ' and ').replace('+',
                                                                                                              ' ^ ').replace(
        'V', ' or ')  # заменил все для eval'a
    n = 0
    for i in range(1, 11):
        if f'x{i}' in func:
            n = i  # определил кол-во переменных
    if n == 0:
        print("Неправильный ввод перемнных")
        return None  # assert, что названия ф-ий введены правильно
    table = np.zeros((2 ** n, n + 1), int)
    # составляем таблицу истинности
    eval_ = []  # тут будут храниться все зн-я ф-ии.
    for i in range(2 ** n):
        values = ''
        x = i
        for j in range(n):
            values = str(x % 2) + values
            x //= 2
        # cоставили значения переменных
        # table.append([0] * (n + 1)) # n ячеек для значений переменных, n + 1-я - для значения ф-ии
        func1 = func

        for j in range(len(values)):
            table[i, j] = values[j]
            func1 = func1.replace(f'x{j + 1}', values[j])
        table[i, n] = eval(func1)
        eval_.append(eval(func1))

    P0 = eval_[0] == 0
    P1 = eval_[-1] == 1
    M = is_monotonic(table)

    S = True
    len_eval = len(eval_)
    for i in range(len_eval // 2):
        if eval_[i] == eval_[len_eval - i - 1]:
            S = False

    # эта штука поможет определить, линейная ф-я или нет.
    triangle = [eval_.copy()]
    for i in range(1, len(eval_)):
        triangle.append([0] * (len(eval_) - i))
        for j in range(len(eval_) - i):
            triangle[i][j] = (triangle[i - 1][j] + triangle[i - 1][j + 1]) % 2
    L = True
    for i in range(len(triangle)):
        if bin(i).count('1') > 1 and triangle[i][0] == 1:
            L = False

    print(f"Классы функции {function}:")
    print(len("|  P0  |  P1  |   L   |   S   |   M   |") * '-')
    print("|  P0  |  P1  |   L   |   S   |   M   |")
    print(len("|  P0   |  P1 |   L   |   S    |   M  |") * '-')
    ans = ["+" if x else '-' for x in [P0, P1, L, S, M]]
    print(f'|  {ans[0]}   |   {ans[1]}  |   {ans[2]}   |   {ans[3]}   |   {ans[4]}   |')
    print(len("|  P0  |  P1  |   L   |   S   |   M   |") * '-')


print('Введите формулу с использоваием до 10 переменных вида x1, x2, ..., x10\n (пожалуйста, не используйте переменную xi, если не использовали переменную x(i-1)')
print('Используйте следующие обозначения логических операций:\n'
      '* - конъюнкця\n'
      'V - дизъюнкция\n'
      '! - отрицание\n'
      '-> - импликация\n'
      '~ - эквиваленция\n'
      '+ - XOR')
f(input("Введите функцию: "))
