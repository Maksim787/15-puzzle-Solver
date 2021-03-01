from SolverA import *


# тестирует n_times случайных решаемых досок размера size
# show_steps - показывать шаги найденных решений
# show_first_res - во время работы алгоритма показывать текущую найденную ближайшую доску к ответу
def test_size(size, n_times, show_steps=False, show_first_res=False):
    random.seed(1)
    total_steps = []
    efficiency = []
    solver = Solver(size)
    print("SIZE:", solver.SIZE)
    for i in range(n_times):
        task = solver.GetRandomBoard()
        steps = solver.Solve(task, show_first_res=show_first_res)
        print("{i}: {len} steps".format(i=i, len=len(steps)))
        print("{i}: {eff:.8f}% efficiency".format(i=i, eff=solver.GetEfficiency() * 100))
        if show_steps:
            print("Steps:")
            solver.PrintSteps(steps)
        print()
        total_steps.append(len(steps))
        efficiency.append(solver.GetEfficiency() * 100)
    total_steps.sort()
    efficiency.sort()
    print("Average steps:", sum(total_steps) / len(total_steps))
    print("Min steps:", min(total_steps))
    print("Max steps:", max(total_steps))
    print("Sample steps:", total_steps)
    print("Sample efficiency:", *["{eff:.8f}%".format(eff=i) for i in efficiency])
    print()


# тестирует одну доску task - массив из SIZE * SIZE чисел - строки головоломки; SIZE * SIZE - 1 - пустая клетка
# show_steps - показывать шаги найденных решений
# show_first_res - во время работы алгоритма показывать текущую найденную ближайшую доску к ответу
def test_board(task, show_steps=False, show_first_res=False):
    solver = Solver(round(math.sqrt(len(board))))
    steps = solver.Solve(task, show_first_res=show_first_res)
    print("{len} steps".format(len=len(steps)))
    print("{eff:.8f}% efficiency".format(eff=solver.GetEfficiency() * 100))
    if show_steps:
        print("Steps:")
        solver.PrintSteps(steps)
    print()


input("Чтобы протестировать 10 досок 3x3, введите 1:\n")
test_size(3, 10)

input("Чтобы протестировать 10 досок 4x4, введите 1:\n")
test_size(4, 10)

input("Чтобы протестировать доску 4x4 и вывести шаги, введите 1:\n")

board = [4, 5, 3, 9, 0, 1, 2, 12, 15, 13, 14, 6, 8, 7, 10, 11]
test_board(board, show_steps=True)

input("Чтобы протестировать доску 5x5 и выводить лучшую доску, найденную алгоритмом, введите 1:\n")

# тестирует доску 5 на 5
test_size(5, 1, show_first_res=True)
