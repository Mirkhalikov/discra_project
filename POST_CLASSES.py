import numpy as np
import re


def compare_arrs(arr1, arr2):  # для праоверки монотонности
    '''
    Eсли второй массив >= первого, возвращает 2,
    Eсли  первый >= второго, возвращает 1,
    Eсли они не сравнимы, возвращает 0.
    Случай равенства не рассмаривается
    '''
    arr1 = np.array(arr1)
    arr2 = np.array(arr2)
    print(arr2-arr1)
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


def f(func):
    func = re.sub(r"(!\w+)", r"( \1 )", func)
    func = func.replace('!', ' not ')
    func = func.replace('->', ' <= ').replace('~', ' == ')
    func = func.replace('*', ' and ').replace('+', ' ^ ')
    func = func.replace('V', ' or ')  # заменил все для eval'a
    operations = ['not', '<=', '==', 'and', '^', '(', ')', 'or', '1', '0']
    func = re.sub(r"[ ]+", ' ', func)
    variables = []
    for i in func.split():
        if (not i in operations) and (not i in variables):
            variables += [i]
    n = len(variables)
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
        func1 = func
        for j in range(len(values)):
            table[i, j] = values[j]
            func1 = func1.replace(variables[j], values[j])
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

    print("Таблица истинности: ")
    print('', ' '.join(variables), 'f')
    for i in range(2 ** n):
        print(*[x for x in table[i:i + 1, :]])


    anf = ''
    for i in range(1, len(triangle)):
        if triangle[i][0]:
            anf += '*'.join(
                [variables[j] for j in range(len(*table[i:i + 1, :-1])) if table[i:i + 1, :-1].tolist()[0][j] == 1]) + ' + '
    if triangle[0][0]:
        anf += '1'
    else:
        anf += '0'
    print(f'АНФ ф-ии: {anf}')

    print(f"Классы функции {func}:")
    s = "|  P0  |  P1  |   L   |   S   |   M   |"
    print(len(s) * '-')
    print(s)
    print(len(s) * '-')
    ans = ["+" if x else '-' for x in [P0, P1, L, S, M]]
    print(f'|  {ans[0]}   |   {ans[1]}  |   {ans[2]}   |   {ans[3]}   |   {ans[4]}   |')
    print(len(s) * '-')


print('Введите формулу: ')
print('Используйте следующие обозначения логических операций:\n'
      '* - конъюнкця\n'
      'V - дизъюнкция\n'
      '! - отрицание\n'
      '-> - импликация\n'
      '~ - эквиваленция\n'
      '+ - XOR')
f(input("Введите функцию: "))

