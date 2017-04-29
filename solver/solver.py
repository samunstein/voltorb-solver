from model.model import InputGrid, PossibilityGrid, Hint, KNOWN_STATES, UNKNOWN, ONE, TWO, THREE, VOLTORB


class Solver(object):
    def __init__(self):
        self.__grid = None
        self.__possibility_grid = None

    def solve(self, grid) -> PossibilityGrid:
        self.__grid = grid
        self.__possibility_grid = PossibilityGrid()
        self.__try()
        return self.__possibility_grid

    def __try(self):
        card, row, col = self.__grid.first_unknown()
        if card is None:
            self.__possibility_grid.add_possibility(self.__grid)
        else:
            for state in KNOWN_STATES:
                card.state = state
                if self.__grid.is_possible(row, col):
                    self.__try()
            card.state = UNKNOWN
            # This is done here even if it is very unintuitive
            self.__grid.unknowns.pop()

"""
xample  = [[1, 1, 1, 0, 1],
           [2, 1, 1, 1, 2],
           [0, 0, 1, 1, 3],
           [1, 1, 1, 0, 2],
           [1, 1, 1, 1, 0]]
bottom = []
for i in range(5):
    col = []
    for j in range(5):
        col.append(xample[j][i])
    bottom.append(Hint(sum(col), col.count(0)))

right = []
for i in range(5):
    row = []
    for j in range(5):
        row.append(xample[i][j])
    right.append(Hint(sum(row), row.count(0)))
"""

if __name__ == "__main__":
    # Up-down -> left-right
    hints = "3 2 7 2 5 2 6 2 5 2 7 1 2 4 6 2 7 1 4 2"
    numhints = [int(a) for a in hints.split()]
    right = [Hint(numhints[i], numhints[i+1]) for i in range(0, 10, 2)]
    bottom = [Hint(numhints[i], numhints[i+1]) for i in range(10, 20, 2)]

    example = InputGrid(bottom, right)

    zeross = [[0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0]]

    knowns = [[0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0]]

    for i in range(5):
        for j in range(5):
            if knowns[i][j] != VOLTORB:
                example[i, j].state = 1 if knowns[i][j] == ONE else 2 if knowns[i][j] == TWO else 3
    result = Solver().solve(example)

    for i in range(5):
        for j in range(5):
            poss = result[i, j]
            r = ""
            if not poss.useful():
                r += "MEH"
            else:
                if poss.values[1] > 0:
                    r += "1"
                if poss.values[2] > 0:
                    r += "2"
                if poss.values[3] > 0:
                    r += "3"
                if poss.values[0] > 0:
                    r += "V={:.0f}".format(100 * poss.probabilities()[0])
            print("{:10s}".format(r), end="")
        print()
        print()
