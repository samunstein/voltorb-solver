from tkinter import *

SHOWTABLE_X_SHIFT = 15


class VoltorbUI:
    def __init__(self, result, button_press, new_game):
        self.__mainwindow = Tk()
        self.__result = result
        self.__button_press = button_press
        self.__new_game = new_game

        self.__images = [PhotoImage("voltorb", file="0.png"),
                         PhotoImage("one", file="1.png"),
                         PhotoImage("two", file="2.png"),
                         PhotoImage("three", file="3.png"),
                         PhotoImage("empty", file="e.png")
                        ]
        self.__new_game_entry = Entry(self.__mainwindow)
        self.__new_game_entry.grid(row=15, column=0, columnspan=9, sticky=W + E)
        Button(self.__mainwindow, command=self.new_game, text="New Game").grid(row=12, column=SHOWTABLE_X_SHIFT + 3, columnspan=2)
        Button(self.__mainwindow, command=self.__mainwindow.destroy, text="Quit").grid(row=13, column=SHOWTABLE_X_SHIFT + 4)
        buttons = []
        for i in range(5):
            for j in range(5):
                for y in range(3):
                    for x in range(3):
                        if x < 2 and y < 2:
                            newButton = Button(self.__mainwindow, image=self.__images[2  * y + x], command=lambda n=j, m=i, o=2*y+x: self.update_square(n, m, o))
                            buttons.append(newButton)
                            newButton.grid(row=3 * i + y, column=3 * j + x)
                        else:
                            Label(self.__mainwindow).grid(row = 3 * i + y, column=3 * j + x)

        self.__showlabels = []
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

                newLabel = Label(self.__mainwindow, text=r)
                newLabel.grid(row = i, column = SHOWTABLE_X_SHIFT + j)
                self.__showlabels.append(newLabel)
        self.__mainwindow.mainloop()

    def update_square(self, x, y, i):
        self.__button_press(self, x, y, i)

    def update(self, result):
        self.__result = result
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

                self.__showlabels[5 * i + j]["text"] = r

    def new_game(self):
        self.__new_game(self, self.__new_game_entry.get())