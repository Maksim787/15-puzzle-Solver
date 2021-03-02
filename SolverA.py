from heapq import *
import random


class Solver:
    def __init__(self, SIZE=3):
        self.SIZE = SIZE
        # нумерация чисел с 0, пустое место обозначается SIZE * SIZE - 1
        # доска головоломки - массив из SIZE * SIZE - 1 элементов - строки головоломки, записанные в одну строку
        self.EMPTY = SIZE * SIZE - 1
        self.INF = 100000000
        # число перебранных в процессе решения комбинаций
        self.USED_SIZE = 0

        # штраф за манхеттенское расстояние до правильного места (расстояния от 0 до 8)
        self.penalty_dist = [0, 2, 4, 6, 8, 10, 12]
        # дополнительный коэффициент штрафа для каждой плитки
        self.scores = [1, 1, 1, 1,
                       1, 1, 1, 1,
                       1, 1, 1, 1,
                       1, 1, 1, 0]
        if SIZE > 4:
            self.scores = [1] * (SIZE * SIZE)
            self.scores[-1] = 0
            self.penalty_dist = [i * 10 for i in range(2 * SIZE - 1)]
        if SIZE <= 3:
            self.scores = [1] * (SIZE * SIZE)
            self.scores[-1] = 0
            self.penalty_dist = list(range(2 * SIZE - 1))

    # установка размера головоломки
    def SetSize(self, new_size):
        self.SIZE = new_size
        self.EMPTY = new_size * new_size - 1

    # Случайная головоломка
    def GetRandomBoard(self):
        # доска головоломки - массив из SIZE * SIZE - 1 элементов
        res = random.sample(range(self.SIZE * self.SIZE), self.SIZE * self.SIZE)
        # мешаем, пока не можем решить
        # т. к. корректных перестановок - половина, то мы быстро найдем решаемую
        while not self.CanSolve(res):
            random.shuffle(res)
        return res

    # проверка на то, что головоломку можно решить
    def CanSolve(self, board):
        empty_pos = board.index(self.EMPTY)
        # манхеттенское расстояние от пустой клетки до левого верхнего угла
        real_power = empty_pos // self.SIZE + empty_pos % self.SIZE
        # число транспозиций в перестановке
        power = 0
        for i in range(self.SIZE * self.SIZE):
            for j in range(i):
                power += (board[j] > board[i])
        # число транспозиций должно давать такой же остаток при делении на 2,
        # как и манхеттенское расстояние от пустой позиции до левого верхнего угла
        return power % 2 == real_power % 2

    # возможные ходы из текущего состояния доски
    # ход - пара чисел: (место пустой клетки; куда она идёт)
    def PossibleTurns(self, board):
        empty_pos = board.index(self.EMPTY)
        turns = []
        # перемещение пустой клетки влево
        if empty_pos % self.SIZE != 0:
            turns.append((empty_pos, empty_pos - 1))
        # перемещение пустой клетки вправо
        if empty_pos % self.SIZE != self.SIZE - 1:
            turns.append((empty_pos, empty_pos + 1))
        # перемещение пустой клетки вверх
        if empty_pos // self.SIZE != 0:
            turns.append((empty_pos, empty_pos - self.SIZE))
        # перемещение пустой клетки вниз
        if empty_pos // self.SIZE != self.SIZE - 1:
            turns.append((empty_pos, empty_pos + self.SIZE))
        return turns

    # делаем ход
    def MakeTurn(self, board, turn):
        from_pos, to_pos = turn
        board_list = list(board)
        board_list[from_pos], board_list[to_pos] = board_list[to_pos], board_list[from_pos]
        return tuple(board_list)

    # Получение эвристики
    def GetHeuristic(self, board):
        # попробовать свой счёт
        # return self.CustomHeuristic(board)

        # для каждой клетки считается её манхеттенское расстояние до правильной позиции, пусть оно равно man_dist
        # к счёту прибавляется penalty_dist[man_dist] * scores[number]
        dist = 0
        for ind in range(self.SIZE * self.SIZE):
            number = board[ind]
            true_pos = number // self.SIZE, number % self.SIZE
            pos = ind // self.SIZE, ind % self.SIZE
            man_dist = abs(true_pos[0] - pos[0]) + abs(true_pos[1] - pos[1])
            dist += self.penalty_dist[man_dist] * self.scores[number]
        return dist

    # переопределение своего расстояния
    def CustomHeuristic(self, board):
        dist = 0
        for ind in range(self.SIZE * self.SIZE):
            if board[ind] == self.EMPTY:
                continue
            true_pos = board[ind] // self.SIZE, board[ind] % self.SIZE
            pos = ind // self.SIZE, ind % self.SIZE
            man_dist = abs(true_pos[0] - pos[0]) + abs(true_pos[1] - pos[1])
            dist += man_dist * man_dist
        return dist

    # восстановление ответа по пути из словаря
    def GetOptimalPath(self, prev_board_dict, last_board):
        board_path = []
        while last_board is not None:
            board_path.append(last_board)
            last_board = prev_board_dict[last_board]
        board_path.reverse()
        return board_path

    # число рассмотренных комбинаций / общее число возможных комбинаций
    def GetEfficiency(self):
        return self.USED_SIZE

    # печать доски вместе со счётом
    def PrintBoard(self, board):
        print("-" * 10)
        print("Score:", self.GetHeuristic(board))
        for col_ind in range(self.SIZE):
            for row_ind in range(self.SIZE):
                num = board[col_ind * self.SIZE + row_ind]
                if num != self.EMPTY:
                    print(num + 1, end='\t')
                else:
                    print(0, end='\t')
            print()
        print("-" * 10)

    # печать шагов
    def PrintSteps(self, steps):
        for step in steps:
            self.PrintBoard(step)

    # основная функция
    # решает головоломку и возвращает промежуточные шаги
    # show_first_res - во время решения печатает доску с текущей наименьшей эвристикой
    def Solve(self, board, show_first_res=False):
        board = tuple(board)
        # уже решена
        if self.GetHeuristic(board) == 0:
            return [board]
        # не может быть решена
        if not self.CanSolve(board):
            return []
        # куча с (f = g + h, task), где g - число сделанных ходов, h - значение эвристики, task - массив доски
        heap = []  # (f, task)
        # min_g у использованных досок
        g_score = {}
        # словарь для восстановления пути
        prev_board = {}

        heappush(heap,
                 (self.GetHeuristic(board),
                  board))
        g_score[board] = 0
        prev_board[board] = None

        # текущий минимум эвристики
        h_min = self.INF

        while True:
            # берём доску с наименьшей f = g + h
            f, board = heappop(heap)
            # перебираем возможные ходы
            for turn in self.PossibleTurns(board):
                next_board = self.MakeTurn(board, turn)
                g = g_score[board] + 1
                # если он не был в рассмотрении или мы нашли более близкое расстояние
                if next_board not in g_score or g < g_score[next_board]:
                    g_score[next_board] = g
                    prev_board[next_board] = board
                    h = self.GetHeuristic(next_board)
                    heappush(heap,
                             (g + h, next_board))
                    # печать промежуточных результатов
                    if show_first_res and h < h_min:
                        h_min = h
                        self.USED_SIZE = len(g_score)
                        # число рассмотренных досок
                        print("Рассмотрено: {eff} расстановок".format(eff=self.GetEfficiency()))
                        print("Длина пути к этой расстановке:", g_score[next_board])
                        self.PrintBoard(next_board)
                    if h == 0:
                        self.USED_SIZE = len(g_score)
                        return self.GetOptimalPath(prev_board, next_board)
