from SolverA import *
import random
import math


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
        print("{i}: {len} шагов".format(i=i, len=len(steps)))
        print("{i}: {eff} досок рассмотрено".format(i=i, eff=solver.GetEfficiency()))
        if show_steps:
            print("Шаги:")
            solver.PrintSteps(steps)
        print()
        total_steps.append(len(steps))
        efficiency.append(solver.GetEfficiency())
    total_steps.sort()
    efficiency.sort()
    print("Average steps:", sum(total_steps) / len(total_steps))
    print("Min steps:", min(total_steps))
    print("Max steps:", max(total_steps))
    print("Число шагов в выборке:", total_steps)
    print("Число рассмотренных досок в выборке:", efficiency)
    print()


# тестирует одну доску task - массив из SIZE * SIZE чисел - строки головоломки; SIZE * SIZE - 1 - пустая клетка
# show_steps - показывать шаги найденных решений
# show_first_res - во время работы алгоритма показывать текущую найденную ближайшую доску к ответу
def test_board(task, show_steps=False, show_first_res=False):
    solver = Solver(round(math.sqrt(len(task))))
    steps = solver.Solve(task, show_first_res=show_first_res)
    print("{len} шагов".format(len=len(steps)))
    print("{eff} досок рассмотрено".format(eff=solver.GetEfficiency()))
    if show_steps:
        print("Шаги:")
        solver.PrintSteps(steps)
    print()


def test_random_board(size, show_steps=False, show_first_res=False):
    random.seed(1)
    solver = Solver(size)
    print("SIZE:", solver.SIZE)
    task = solver.GetRandomBoard()
    steps = solver.Solve(task, show_first_res=show_first_res)
    print("{len} шагов".format(len=len(steps)))
    print("{eff} досок рассмотрено".format(eff=solver.GetEfficiency()))
    if show_steps:
        print("Шаги:")
        solver.PrintSteps(steps)
    print()


input("Чтобы протестировать 10 досок 3x3, введите 1:\n")
test_size(3, 10)

input("Чтобы протестировать 10 досок 4x4, введите 1:\n")
test_size(4, 10)

input("Чтобы протестировать 10 досок 5x5, введите 1:\n")
test_size(5, 10)

input("Чтобы протестировать доску 4x4 и вывести шаги, введите 1:\n")

board = [4, 5, 3, 9, 0, 1, 2, 12, 15, 13, 14, 6, 8, 7, 10, 11]
test_board(board, show_steps=True)

input("Чтобы протестировать доски 5x5 и 6x6, введите 1:\n")

# тестирует доску 5 на 5
test_random_board(5)
# тестирует доску 6 на 6
test_random_board(6)
# тестирует доску 8 на 8 (не останавливается, но печатает лучшие найденные доски)
# остается поменять пару клеток местами
input("Чтобы протестировать доску 7x7 и напечатать первые найденные результаты, введите 1:\n")
test_random_board(7, show_first_res=True)
