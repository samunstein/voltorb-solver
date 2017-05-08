from tkinter import *

SHOWTABLE_X_SHIFT = 15


class VoltorbUI:
    def __init__(self, result, button_press, new_game):
        self.__mainwindow = Tk()
        self.__mainwindow.title("Voltorb Flip Solver")
        self.__result = result
        self.__button_press = button_press
        self.__new_game = new_game
        self.__mainwindow.bind("<Return>", lambda x: self.new_game())
        self.__mainwindow.bind("<Tab>", lambda x: self.__new_game_entry.focus_set())

        self.__images = [PhotoImage("voltorb", file="0.png"),
                         PhotoImage("one", file="1.png"),
                         PhotoImage("two", file="2.png"),
                         PhotoImage("three", file="3.png")
                        ]
        self.__new_game_entry = Entry(self.__mainwindow)
        self.__new_game_entry.grid(row=15, column=0, columnspan=9, sticky=W + E)
        Button(self.__mainwindow, command=self.new_game, text="New Game").grid(row=12, column=SHOWTABLE_X_SHIFT + 3, columnspan=2)
        Button(self.__mainwindow, command=self.__mainwindow.destroy, text="Quit").grid(row=13, column=SHOWTABLE_X_SHIFT + 4, columnspan=2)
        self.__buttons = []
        for i in range(5):
            for j in range(5):
                for y in range(3):
                    for x in range(3):
                        if x < 2 and y < 2:
                            newButton = Button(self.__mainwindow, image=self.__images[2  * y + x], compound=CENTER, command=lambda n=j, m=i, o=2*y+x: self.update_square(n, m, o))
                            self.__buttons.append(newButton)
                            newButton.grid(row=3 * i + y, column=3 * j + x)
                        else:
                            Label(self.__mainwindow).grid(row = 3 * i + y, column=3 * j + x)


        self.__clicked = [0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0]
        newLabel = Label(self.__mainwindow)
        self.__orig_bg = newLabel.cget("background")
        self.__new_game_entry.focus_set()
        self.__mainwindow.mainloop()

    def update_square(self, x, y, i):
        if i == 0:
            self.__clicked[5 * y + x] = 0
        else:
            self.__clicked[5 * y + x] = 1
        self.__button_press(self, x, y, i)

    def update(self, result):
        self.__result = result
        lowest = []
        min_p = 1
        for i in range(5):
            for j in range(5):
                poss = result[i, j]
                self.color_buttons(i, j, self.__orig_bg)
                r = "0"
                if not poss.useful() or self.__clicked[5 * i + j]:
                    r = "NN"
                else:
                    p = 1
                    if poss.values[0] > 0:
                        p = poss.probabilities()[0]
                        r = "{:.0f}".format(100 * p)
                    else:
                        p = 0
                    if p < min_p:
                        lowest = [(i, j)]
                        min_p = p
                    elif p == min_p:
                        lowest.append((i, j))

                self.__buttons[4 * (5 * i + j)]["text"] = r

        for pos in lowest:
            self.color_buttons(pos[0], pos[1], "red")

    def new_game(self):
        self.__new_game(self, self.__new_game_entry.get())
        self.__new_game_entry.delete(0, END)
        self.__clicked = [0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0]


    def color_buttons(self, x, y, color):
        for i in range(2):
            for j in range(2):
                self.__buttons[4 * y + 20 * x + 2 * i + j]["background"] = color



