from collections import defaultdict
from copy import deepcopy
import time

class Solver:
    def __init__(self, path):
        try:
            file = open(path, 'r')
            self.text = file.read()
        except(FileNotFoundError):
            print("File not found.")

        self.puzzle_dict = defaultdict(list)
        self.empty_spaces = []

    def parse(self):
        index = 0

        for char in self.text:
            if (not char.isdigit()):
                continue

            row = index // 9
            col = index % 9
            box = self.getBox(row, col)

            position = (str(row), str(col), str(box))

            if (int(char) == 0):
                self.empty_spaces.append([position, set([])])

            self.initDict(int(char), position)

            index += 1

    def initDict(self, num, position):
        row, col, box = position

        self.puzzle_dict['r' + row].append(num)
        self.puzzle_dict['c' + col].append(num)

        if (num != 0):
            self.puzzle_dict['b' + box].append(num)

    def getBox(self, row, col):
        if (row < 3):
            if (col < 3):
                return 0
            elif (col < 6):
                return 1
            else:
                return 2
        elif (row < 6):
            if (col < 3):
                return 3
            elif (col < 6):
                return 4
            else:
                return 5
        else:
            if (col < 3):
                return 6
            elif (col < 6):
                return 7
            else:
                return 8

    def solve(self):
        solution = None

        t1 = time.perf_counter()
        self.parse()
        t2 = time.perf_counter()
        print("Parsed puzzle in %f seconds." % (t2 - t1))

        t1 = time.perf_counter()
        self.updatePossibleMoves()
        self.elimCand()

        if (len(self.empty_spaces) > 0):
            solution = self.dfs()

        t2 = time.perf_counter()
        print("Solved puzzle in %f seconds." % (t2 - t1))

        if (solution):
            solution.printPuzzle()
        else:
            self.printPuzzle()

    def dfs(self):
        if (len(self.empty_spaces) == 0):
            return self

        space = self.empty_spaces.pop(0)
        possibleMoves = space[1]
        state = deepcopy(self)

        for move in possibleMoves:
            # Check if next board state is valid if current move played
            nextValid = state.updateDict(move, space[0])
            
            if (nextValid):
                state.updatePossibleMoves()
                solution = state.dfs()

                if (solution):
                    return solution
                else:
                    # Reset state if dfs could not find a solution
                    state = deepcopy(self)

        return None

    def elimCand(self):
        sFound = self.elimSingletons()

        while (sFound):
            self.updatePossibleMoves()
            self.elimSingletons()

    def updatePossibleMoves(self):
        allMoves = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
        possibleMoves = set()

        for space in self.empty_spaces:
            position = space[0]
            row, col, box = position

            notPossible = set(self.puzzle_dict['r' + row]).union(set(self.puzzle_dict['c' + col])).union(set(self.puzzle_dict['b' + box]))
            possibleMoves = allMoves - notPossible

            space[1] = possibleMoves

    def elimSingletons(self):
        solved = False

        for space in self.empty_spaces.copy():
            if (not len(space[1]) == 1):
                continue
            
            solved = True
            self.updateDict(list(space[1]).pop(), space[0])
            self.empty_spaces.remove(space)

        return solved

    def updateDict(self, num, position):
        row, col, box = position

        if (num in self.puzzle_dict['r' + row] or num in self.puzzle_dict['c' + col]\
            or num in self.puzzle_dict['b' + box]):
            return False

        self.puzzle_dict['r' + row][int(col)] = num
        self.puzzle_dict['c' + col][int(row)] = num

        if (num != 0):
            self.puzzle_dict['b' + box].append(num)

        return True

    def printPuzzle(self):
        for k, v in self.puzzle_dict.items():
            if ('r' not in k):
                continue

            print(v)

path = 'hard_puzzle1.txt'
puzzle = Solver(path)
puzzle.solve()