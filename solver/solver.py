from model.model import InputGrid, PossibilityGrid, Hint, KNOWN_STATES, UNKNOWN, ONE, TWO, THREE, VOLTORB
from ui.ui import VoltorbUI

# Gathermode decides whether input mode is via camera or via keyboard
GATHERMODE = True



if GATHERMODE:
    import time
    import pygame.camera
    from reader.reader import imgprocess, hints as get_hints, save_hints
    import reader.reader
    reader.reader.READERFOLDER = "../reader/"


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


def solve(hints="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0", knowns=None):
    try:
        numhints = [int(a) for a in hints.split()]
        right = [Hint(numhints[i], numhints[i+1]) for i in range(0, 10, 2)]
        bottom = [Hint(numhints[i], numhints[i+1]) for i in range(10, 20, 2)]
    except:
        return False

    example = InputGrid(bottom, right)

    if knowns is None:
        knowns = [[0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0]]

    for i in range(5):
        for j in range(5):
            if knowns[i][j] != VOLTORB:
                example[i, j].state = 1 if knowns[i][j] == ONE else 2 if knowns[i][j] == TWO else 3
    return Solver().solve(example)

def parse_hints(hint):
    if len(hint) == 20:
        return " ".join(list(hint))
    elif len(hint) >= 39:
        return hint
    else:
        hintlist = hint.split(" ")
        if len(hintlist) == 2:
            if len(hintlist[0]) < len(hintlist[1]):
                return " ".join([hintlist[0]] + list(hintlist[1]))
            else:
                return " ".join(list(hintlist[0]) + [hintlist[1]])
        else:
            hint = []
            for part in hintlist:
                if len(part) == 2:
                    hint.append(part)
                else:
                    hint += list(part)
            return " ".join(hint)

def main():
    knowns = [[0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0]]
    hints = "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
    result = solve()

    def button_press(ui, x, y, i):
        knowns[y][x] = i
        result = solve(hints, knowns)
        if not result:
            return
        ui.update(result)

    def new_game(ui, new_hints):
        for i in range(5):
            for j in range(5):
                knowns[i][j] = 0
        nonlocal hints
        hints = parse_hints(new_hints)
        result = solve(hints)
        if not result:
            return
        ui.update(result)

        # If gathering images, save them
        if GATHERMODE:
            t = time.perf_counter()
            img = pygame.surfarray.array3d(webcam.get_image())
            while time.perf_counter() < t + 0.5:
                img = pygame.surfarray.array3d(webcam.get_image())
            imgs = imgprocess(img)
            hint = get_hints(imgs)
            save_hints(hint, hints.split())


    if GATHERMODE:
        pygame.camera.init()

        cameras = pygame.camera.list_cameras()
        # Change the right camera here. No way to know without trying.
        webcam = pygame.camera.Camera(cameras[1])
        webcam.start()

    VoltorbUI(result, button_press, new_game)

main()
