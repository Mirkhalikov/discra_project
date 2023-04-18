if __name__ == "__main__":

    # Q = int(input("Введите кол-во состояний: "))
    m = int(input("Введите кол-во строк с описанием машины: "))
    print(f"Введите {m} cтрок с описанием машины. Пожалуйста, организуйте ввод в следующем порядке:\n"
          f"Текущее состояние, входной символ, новое состояние, выходной символ, смещение - через пробел, без запятых")

    states = dict()  # name: dict(in_symb -> new state out_symb, shift)
    A = set() # Алфавит
    for _ in range(m):
        # Считываем строку до тех пор, пока не введут правильно
        while True:
            try:
                first_state, in_symb, new_state, out_symb, shift = input().split()
                A.add(in_symb)
                A.add(out_symb)
                if shift not in ["+1", "-1"]:
                    print("Неверно введенная строка, попробуйте еще раз: ")
                    raise ValueError
                if not first_state in states:
                    states[first_state] = {in_symb: (new_state, out_symb, shift)}
                else:
                    if not in_symb in states[first_state].keys():
                        states[first_state][in_symb] = (new_state, out_symb, shift)
                    else:
                        print(
                            "В описании данного состояния уже существует алгоритм на данный входной символ. Попробуйте еще раз.")
                        raise ValueError
                break
            except ValueError:
                pass


    tape = input("Введите входные данные на ленте (в качестве пустого символа используйте ^): ")
    n = int(input("Введите длину ленты: "))
    if len(tape) > n:
        print("Длина ленты не может быть меньше длины входных данных")
        raise SystemExit
    tape += (n - len(tape)) * '^'
    tape = [x for x in tape] #преобразовал в массив для удобства
    firstStateOfTape = tape
    pos = 0
    cur_state = input("Введите название начального состояния: ")
    end_state = input("Введите название состояния, которое отвечает за окончание работы")
    maximum_iters = n * len(states) * len(A) ** n
    iteration = 0
    while True:
        iteration += 1
        if cur_state == end_state:
            print("OK")
            print(''.join(tape))
            break
        if iteration > maximum_iters:
            print("Not OK")
            break
        try:
            tape[pos], pos, cur_state = states[cur_state][tape[pos]][1], (pos + int(states[cur_state][tape[pos]][2])) % n, states[cur_state][tape[pos]][0]
        except KeyError:
            print("Состояние машины, в котором она сейчас находится, не умеет обрабатывать данный символ")
            break
