from tkinter import *
from tkinter import messagebox

from sudoku_PSO import Swarm


class View:
    def __init__(self):
        self.swarm = None
        self.root = Tk()
        self.root.title('Sudoku - PSO')

        self.upper_frame = Frame(self.root)
        self.upper_frame.pack()

        self.factor_frame = Frame(self.root)
        self.factor_frame.pack()

        self.start_button = Button(self.upper_frame, text="Start", command=self.on_start)
        self.start_button.pack(side=LEFT)

        self.exit_button = Button(self.upper_frame, text="Exit", command=self.on_exit)
        self.exit_button.pack(side=LEFT)

        self.first_factor = Scale(self.factor_frame, label='w', orient=HORIZONTAL, length=150)
        self.first_factor.pack()

        self.second_factor = Scale(self.factor_frame, label='f_1', orient=HORIZONTAL, length=150)
        self.second_factor.pack()

        self.third_factor = Scale(self.factor_frame, label='f_2', orient=HORIZONTAL, length=150)
        self.third_factor.pack()

        self.row_frames = [Frame(self.root) for i in range(9)]
        for frame in self.row_frames:
            frame.pack()

        self.sudoku_entries = [[[] for j in range(9)] for i in range(9)]

        for i in range(9):
            for j in range(9):
                self.sudoku_entries[i][j] = Entry(self.row_frames[i], width=2, justify=CENTER)
                self.sudoku_entries[i][j].pack(side=LEFT)

        self.root.mainloop()

    def on_start(self):
        self.block_gui()
        if self.first_factor.get() + self.second_factor.get() + self.third_factor.get() != 100:
            # check if w + f_1 + f_2 == 100
            messagebox.showinfo('Error', 'Factors must sum to 100')
        else:
            sudoku = [[self.sudoku_entries[i][j].get() for j in range(9)] for i in range(9)]
            self.swarm = Swarm(sudoku)

            if not self.swarm.check_correctness():
                # check if user gave only numbers 1-9
                messagebox.showinfo('Error', 'Only numbers 1-9 possible')
            else:
                # do the rest
                self.swarm.start()
                # print('Actually do algo')

        self.unblock_gui()

    def on_exit(self):
        print('exiting...')
        exit()

    def block_gui(self):
        self.start_button['state'] = DISABLED
        self.exit_button['state'] = DISABLED
        self.first_factor['state'] = DISABLED
        self.second_factor['state'] = DISABLED
        self.third_factor['state'] = DISABLED
        for i in range(9):
            for j in range(9):
                self.sudoku_entries[i][j]['state'] = DISABLED

    def unblock_gui(self):
        self.start_button['state'] = NORMAL
        self.exit_button['state'] = NORMAL
        self.first_factor['state'] = NORMAL
        self.second_factor['state'] = NORMAL
        self.third_factor['state'] = NORMAL
        for i in range(9):
            for j in range(9):
                self.sudoku_entries[i][j]['state'] = NORMAL


if __name__ == "__main__":
    sth = View()
