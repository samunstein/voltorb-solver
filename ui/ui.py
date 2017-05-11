from tkinter import *

# Constants for colors
LOWEST = "red"
CLICKED = "green"
USELESS = "teal"

class VoltorbUI:
    def __init__(self, result, button_press, new_game):
        self.__mainwindow = Tk()
        self.__mainwindow.title("Voltorb Flip Solver")
        # PossibilityGrid
        self.__result = result
        # Two callback functions
        self.__button_press = button_press
        self.__new_game = new_game

        # Bind key presses to Return and Tab
        self.__mainwindow.bind("<Return>", lambda x: self.new_game())
        self.__mainwindow.bind("<Tab>", lambda x: self.__new_game_entry.focus_set())

        self.__images = [PhotoImage("voltorb", file="0.png"),
                         PhotoImage("one", file="1.png"),
                         PhotoImage("two", file="2.png"),
                         PhotoImage("three", file="3.png")
                        ]
        # Create entries and buttons
        self.__new_game_entry = Entry(self.__mainwindow)
        self.__new_game_entry.grid(row=15, column=0, columnspan=10, sticky=W + E)
        Button(self.__mainwindow, command=self.new_game, text="New Game").grid(row=15, column=9, columnspan=5)
        Button(self.__mainwindow, command=self.__mainwindow.destroy, text="Quit").grid(row=15, column=13, columnspan=5)

        # Create Voltorb buttons and a few entries to help with the grid
        self.__buttons = []
        for i in range(5):
            for j in range(5):
                for y in range(3):
                    for x in range(3):
                        if x < 2 and y < 2:
                            newButton = Button(self.__mainwindow, image=self.__images[2  * y + x],
                                               compound=CENTER, command=lambda n=j, m=i, o=2*y+x: self.update_square(n, m, o))
                            self.__buttons.append(newButton)
                            newButton.grid(row=3 * i + y, column=3 * j + x)
                        else:
                            Label(self.__mainwindow).grid(row = 3 * i + y, column=3 * j + x)

        # Just a list to show which buttons have already been clicked
        self.__clicked = [0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0]
        # Store the original background color
        self.__orig_bg = Label(self.__mainwindow).cget("background")
        # Set the focus to entry for ease of use
        self.__new_game_entry.focus_set()
        self.__mainwindow.mainloop()

    def update_square(self, x, y, i):
        """
        Updates the clicked matrix and calls the solver with newest clues
        :param x: coordinate
        :param y: coordinate
        :param i: Tells which button was clicked (int 0-3)
        :return: None
        """
        self.__clicked[5 * y + x] = i
        self.__button_press(self, x, y, i)

    def update(self, result):
        """
        Updates the UI with newly solved grid.
        :param result: New PossibilityGrid with latest changes
        :return: None
        """
        # Update the result in memory
        self.__result = result
        # Here we store all the values with the lowest probability of a Voltorb
        lowest = []
        min_p = 1

        # Loop through all the possibilities
        for i in range(5):
            for j in range(5):
                poss = result[i, j]
                # Everything back to gray
                self.color_buttons(i, j, self.__orig_bg)
                r = "0"
                if not poss.useful() or self.__clicked[5 * i + j]:
                    r = "NN"
                    # This is to prevent clicked squares from becoming colored
                    if not self.__clicked[5 * i + j]:
                        # Mark all the useless squares
                        self.color_buttons(i, j, USELESS)
                else:
                    # If possibility of voltorb
                    if poss.values[0] > 0:
                        p = poss.probabilities()[0]
                        r = "{:.0f}".format(100 * p)
                    else:
                        p = 0
                    # Check if new optimal
                    if p < min_p:
                        lowest = [(i, j)]
                        min_p = p
                    elif p == min_p:
                        lowest.append((i, j))
                # Mark the clicked square
                if self.__clicked[5 * i + j]:
                    self.color_buttons(i, j, CLICKED, self.__clicked[5 * i + j])
                # Show the probability in empty square
                self.__buttons[4 * (5 * i + j)]["text"] = r

        # Color all the lowest probability squares
        for pos in lowest:
            self.color_buttons(pos[0], pos[1], LOWEST)

    def new_game(self):
        """
        Resets the game and starts a new one with fresh hints
        :return: None
        """
        self.__clicked = [0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0]
        self.__new_game(self, self.__new_game_entry.get())
        self.__new_game_entry.delete(0, END)


    def color_buttons(self, x, y, color, square=None):
        """
        Function changes the background color of given buttons
        :param x: coordinate
        :param y: coordinate
        :param color: new color
        :param square: if None, color all four buttons,
                       if number, only color the one
        :return: None
        """
        if square == None:
            for i in range(2):
                for j in range(2):
                    self.__buttons[4 * y + 20 * x + 2 * i + j]["background"] = color
        else:
            self.__buttons[4 * y + 20 * x + square]["background"] = color

