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

        self.particles_number = Scale(self.factor_frame, from_=1, to_=200, label='particles number', orient=HORIZONTAL, length=150)
        self.particles_number.pack()

        self.iterations = Scale(self.factor_frame, from_=0, to_=2000, label='iterations', orient=HORIZONTAL, length=150)
        self.iterations.pack()

        self.mutation = Scale(self.factor_frame, label='mutation', orient=HORIZONTAL, length=150)
        self.mutation.pack()

        self.inertia = Scale(self.factor_frame, label='inertia', orient=HORIZONTAL, length=150)
        self.inertia.pack()

        self.global_factor = Scale(self.factor_frame, label='global', orient=HORIZONTAL, length=150)
        self.global_factor.pack()

        self.local_factor = Scale(self.factor_frame, label='local', orient=HORIZONTAL, length=150)
        self.local_factor.pack()

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
        if self.particles_number.get() == 0:
            pass
        elif self.inertia.get() + self.global_factor.get() + self.local_factor.get() != 100:
            # check if w + f_1 + f_2 == 100
            messagebox.showinfo('Error', 'Factors (inertia, global, local) must sum to 100')
        else:
            sudoku = [[self.sudoku_entries[i][j].get() for j in range(9)] for i in range(9)]
            self.swarm = Swarm(sudoku, self.particles_number.get(), self.iterations.get(), self.mutation.get(), self.inertia.get(), self.global_factor.get(), self.local_factor.get())

            if not self.swarm.check_correctness():
                # check if user gave only numbers 1-9
                messagebox.showinfo('Error', 'Only numbers 1-9 possible')
            else:
                self.swarm.start()

        self.unblock_gui()

    def on_exit(self):
        print('exiting...')
        exit()

    def block_gui(self):
        self.start_button['state'] = DISABLED
        self.exit_button['state'] = DISABLED
        self.particles_number['state'] = DISABLED
        self.iterations['state'] = DISABLED
        self.mutation['state'] = DISABLED
        self.inertia['state'] = DISABLED
        self.global_factor['state'] = DISABLED
        self.local_factor['state'] = DISABLED
        for i in range(9):
            for j in range(9):
                self.sudoku_entries[i][j]['state'] = DISABLED

    def unblock_gui(self):
        self.start_button['state'] = NORMAL
        self.exit_button['state'] = NORMAL
        self.mutation['state'] = NORMAL
        self.particles_number['state'] = NORMAL
        self.iterations['state'] = NORMAL
        self.inertia['state'] = NORMAL
        self.global_factor['state'] = NORMAL
        self.local_factor['state'] = NORMAL
        for i in range(9):
            for j in range(9):
                self.sudoku_entries[i][j]['state'] = NORMAL


if __name__ == "__main__":
    sth = View()
