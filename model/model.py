from typing import List, Tuple
from enum import Enum


class State(Enum):
    VOLTORB = 0
    ONE = 1
    TWO = 2
    THREE = 3
    UNKNOWN = 4

    @staticmethod
    def list_of_states():
        return [State.VOLTORB, State.ONE, State.TWO, State.THREE, State.UNKNOWN]

    @staticmethod
    def list_of_known_states():
        return [State.VOLTORB, State.ONE, State.TWO, State.THREE]


class FiveGrid(object):
    def __init__(self, grid_lists: List[List]):
        self.__grid = grid_lists

        # Pre-calculate columns for performance
        self.__columns = [[inner[coln] for inner in self.__grid] for coln in range(5)]
        l = list()
        for inner in self.__grid:
            l.extend(inner)
        self.list_of_all = l

    def __getitem__(self, item: Tuple[int, int]):
        """
        :param item: Tuple of two integers
        :return:
        """
        return self.__grid[item[0]][item[1]]

    def __setitem__(self, key, value):
        self.__grid[key[0]][key[1]] = value

    def column(self, j: int):
        return self.__columns[j]

    def row(self, i: int):
        return self.__grid[i]


class Card(object):
    def __init__(self, state: State):
        """
        Initializes Card class. Has a state
        :param state:
        """
        self.state = state


class Possibility(object):
    """
    Class remembering possibilities for a card
    """
    def __init__(self, voltorb: int = 0, one: int = 0, two: int = 0, three: int = 0):
        self.values = {State.VOLTORB: voltorb,
                       State.ONE: one,
                       State.TWO: two,
                       State.THREE: three}

    def probabilities(self):
        """
        :return: Dictionary of probabilities for each card type
        """
        all_summed = sum(self.values.values())
        return dict([(key, self.values[key] / all_summed) for key in self.values])

    def useful(self):
        """
        :return: Boolean telling if the card is worth flipping at all
        """
        return self.values[State.TWO] > 0 or self.values[State.THREE] > 0

    def safe(self):
        return self.values[State.VOLTORB] == 0

    def add(self, which: State):
        self.values[which] += 1


class Hint(object):
    def __init__(self, numbers: int, voltorbs: int):
        self.numbers = numbers
        self.voltorbs = voltorbs


class InputGrid(FiveGrid):
    """
    Class which takes the inputs for both hints and the cards from the user
    """
    def __init__(self, bottom: List[Hint], right: List[Hint], cards: List[List[Card]] = None):
        """
        :param cards: List of lists of Cards
        :param bottom: List of Hints
        :param right: List of Hints
        """
        if cards is None:
            cards = [[Card(State.UNKNOWN) for _ in range(5)] for _ in range(5)]
        super().__init__(cards)
        self.bottom = bottom
        self.right = right
        self.unknowns = []

    def first_unknown(self):
        indx = self.unknowns[-1] if len(self.unknowns) > 0 else 0
        for card in self.list_of_all[indx:]:
            if card.state == State.UNKNOWN:
                self.unknowns.append(indx)
                return card, indx // 5, indx % 5
            indx += 1
        return None, -1, -1

    @staticmethod
    def numbers_from_list(cardlist: List[Card]) -> Tuple[int, int, int]:
        voltorbs = 0
        numbersum = 0
        unknowns = 0
        for card in cardlist:
            if card.state == State.VOLTORB:
                voltorbs += 1
            elif card.state == State.UNKNOWN:
                unknowns += 1
            else:
                numbersum += 1 if card.state == State.ONE else 2 if card.state == State.TWO else 3
        return voltorbs, numbersum, unknowns

    @staticmethod
    def check(voltorbs: int, numbersum: int, unknowns: int, hint: Hint):
        """
        Check the possibility of the row or column against the hint
        :param voltorbs:
        :param numbersum:
        :param unknowns:
        :param hint:
        :return:
        """
        # Values over 1s exceed the possible values over 1
        # 5 - hint.voltorbs = number cards in row
        # hint.numbers - number cards in row = sum of values exceeding one
        # 5 - unknowns = flipped cards
        # numbersum - flipped cards = sum of values exceeding one
        if hint.numbers + hint.voltorbs < numbersum + unknowns:
            return False

        # More voltorbs than allowed, or more numbers than allowed
        if voltorbs > hint.voltorbs or numbersum > hint.numbers:
            return False

        # Less voltorbs possible than stated
        if unknowns + voltorbs < hint.voltorbs:
            return False

        # Less numbers possible than stated
        if numbersum + 3 * unknowns < hint.numbers:
            return False

        # If everything is flipped, does everything match
        if unknowns == 0 and (voltorbs != hint.voltorbs or numbersum != hint.numbers):
            return False

        return True

    def is_possible(self, row: int = None, col: int = None):
        """
        :return: Is the grid with the current card values possible
        """
        if row and col:
            rownindex = [row]
            colnindex = [col]
        else:
            rownindex = range(5)
            colnindex = range(5)

        for rown in rownindex:
            row = self.row(rown)
            hint = self.right[rown]
            voltorbs, numbersum, unknowns = self.numbers_from_list(row)
            if not self.check(voltorbs, numbersum, unknowns, hint):
                return False

        for coln in colnindex:
            col = self.column(coln)
            hint = self.bottom[coln]
            voltorbs, numbersum, unknowns = self.numbers_from_list(col)
            if not self.check(voltorbs, numbersum, unknowns, hint):
                return False

        return True


class PossibilityGrid(FiveGrid):
    """
    Class which remembers the possibilities for each card
    """
    def __init__(self, possibilities: List[List[Possibility]] = None):
        """
        :param possibilities:
        """
        if not possibilities:
            possibilities = [[Possibility() for _ in range(5)] for _ in range(5)]
        super().__init__(possibilities)
        self.possibilities = possibilities

    def add_possibility(self, grid: InputGrid):
        for i in range(5):
            for j in range(5):
                self[i, j].add(grid[i, j].state)
