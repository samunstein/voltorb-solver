from typing import List


VOLTORB = 0
ONE = 1
TWO = 2
THREE = 3
UNKNOWN = 4
STATES = [VOLTORB, ONE, TWO, THREE, UNKNOWN]


class FiveGrid(object):
    def __init__(self, grid_lists: List[List[object]]):
        assert len(grid_lists) == 5
        for inner_list in grid_lists:
            assert len(inner_list) == 5
        self.__grid = grid_lists

    def __getitem__(self, item):
        """
        :param item: Tuple of two integers
        :return:
        """
        assert type(item) is tuple
        assert len(item) == 2
        assert type(item[1]) is int
        assert type(item[0]) is int
        assert 0 <= item[1] < 5
        assert 0 <= item[0] < 5
        return self.__grid[item[0]][item[1]]


class Card(object):
    def __init__(self, state: int):
        """
        Initializes Card class. Has a state
        :param state:
        """
        assert state in STATES
        self.state = state


class Possibility(object):
    """
    Class remembering possibilities for a card
    """
    def __init__(self, voltorb: int = 0, one: int = 0, two: int = 0, three: int = 0):
        self.voltorb = voltorb
        self.one = one
        self.two = two
        self.three = three

    def probabilities(self):
        """
        :return: Dictionary of probabilities for each card type
        """
        all_summed = self.voltorb + self.one + self.two + self.three
        return {VOLTORB: self.voltorb / all_summed,
                ONE: self.one / all_summed,
                TWO: self.two / all_summed,
                THREE: self.three / all_summed}

    def useful(self):
        """
        :return: Boolean telling if the card is worth flipping at all
        """
        return self.two > 0 or self.three > 0


class PossibilityGrid(FiveGrid):
    """
    Class which remembers the possibilities for each card
    """
    def __init__(self, possibilities: List[List[Possibility]]):
        """
        :param possibilities:
        """
        super().__init__(possibilities)
        self.possibilities = possibilities


class Hint(object):
    def __init__(self, numbers: int, voltorbs: int):
        self.numbers = numbers
        self.voltorbs = voltorbs


class InputGrid(FiveGrid):
    """
    Class which takes the inputs for both hints and the cards from the user
    """
    def __init__(self, cards: List[List[Card]], bottom: List[Hint], right: List[Hint]):
        """
        :param cards: List of lists of Cards
        :param bottom: List of Hints
        :param right: List of Hints
        """
        super().__init__(cards)
        self.bottom = bottom
        self.right = right
