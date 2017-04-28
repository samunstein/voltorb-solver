from model.model import InputGrid, PossibilityGrid, Possibility, Card, Hint, State


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
        card = self.__grid.first_unknown()
        if card is None:
            self.__possibility_grid.add_possibility(self.__grid)
        else:
            for state in State.list_of_known_states():
                card.state = state
                if self.__grid.is_possible():
                    self.__try()
            card.state = State.UNKNOWN

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
            if knowns[i][j] != 0:
                example[i, j].state = State.ONE if knowns[i][j] == 1 else State.TWO if knowns[i][j] == 2 else State.THREE
    result = Solver().solve(example)

    for i in range(5):
        for j in range(5):
            poss = result[i, j]
            r = ""
            if not poss.useful():
                r += "MEH"
            else:
                if poss.values[State.ONE] > 0:
                    r += "1"
                if poss.values[State.TWO] > 0:
                    r += "2"
                if poss.values[State.THREE] > 0:
                    r += "3"
                if poss.values[State.VOLTORB] > 0:
                    r += "V={:.0f}".format(100 * poss.probabilities()[State.VOLTORB])
            print("{:10s}".format(r), end="")
        print()
        print()
