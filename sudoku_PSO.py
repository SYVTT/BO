import sys

import numpy as np


def print_sudoku(array, dim):
    if array is None:
        return
    sys.stdout.write('\n')
    for i in range(dim):
        for j in range(dim):
            sys.stdout.write(str(array[i][j]))
            if j in [2, 5]:
                sys.stdout.write(' | ')
        if i in [2, 5]:
            sys.stdout.write('\n----+-----+----')

        sys.stdout.write('\n')
    sys.stdout.write('\n')


def get_row(array, number, dim):
    if not check_array_dim(array, dim) or number >= dim or number < 0:
        return None
    return array[number]


def get_column(array, number, dim):
    if not check_array_dim(array, dim) or number >= dim or number < 0:
        return None
    return [array[i][number] for i in range(dim)]


def get_box(array, number, dim):
    # get one of the box as list
    #  1 2 3
    #  4 5 6
    #  7 8 9
    if not check_array_dim(array, dim) or number >= dim or number < 0:
        return None

    row = (number - 1) // 3
    column = (number - 1) % 3
    return [array[3 * row][3 * column + i] for i in range(3)] + \
           [array[3 * row + 1][3 * column + i] for i in range(3)] + \
           [array[3 * row + 2][3 * column + i] for i in range(3)]


def check_array_dim(array, dim):
    if len(array) != dim:
        return False
    for row in array:
        if len(row) != dim:
            return False
    return True


class Swarm:
    sudoku = None
    mask = None
    array = None
    dim = 9
    number_of_particles = 1
    number_of_iterations = 10000
    particles = None
    best_fitness = 0
    best_position = None

    def __init__(self, array):
        self.array = array

    def start(self):
        print_sudoku(self.sudoku, self.dim)
        self.particles = [Particle(self.sudoku, self.mask, self.dim) for i in range(self.number_of_particles)]
        for particle in self.particles:
            if particle.get_fitness() > self.best_fitness:
                self.best_fitness = particle.get_fitness()
                self.best_position = particle.get_position()

        # iteration = 0
        # while self.best_fitness < 3*self.dim**2 and iteration < self.number_of_iterations:
        #     for particle in self.particles:
        #         particle.update_position(self.best_fitness, self.best_position)
        #
        #     for particle in self.particles:
        #         particle.next_position()
        #         if particle.get_fitness() > self.best_fitness:
        #             self.best_fitness = particle.get_fitness()
        #             self.best_position = particle.get_position()

        print(self.best_fitness)
        print_sudoku(self.best_position, self.dim)

    def check_correctness(self):
        if self.array is None:
            return None

        if not self.check_if_numbers():
            return False

        self.convert_to_numbers()

        for i in range(self.dim):
            row = get_row(self.sudoku, i, self.dim)
            column = get_column(self.sudoku, i, self.dim)
            box = get_box(self.sudoku, i, self.dim)
            if self.contains_duplicates(row) or self.contains_duplicates(column) or self.contains_duplicates(box):
                return False
        return True

    def check_if_numbers(self):
        if not check_array_dim(self.array, self.dim):
            return None

        for row in self.array:
            for entry in row:
                if not self.is_empty(entry) and not self.is_number(entry):
                    return False
        return True

    def is_empty(self, entry):
        return entry == ''

    def is_number(self, entry):
        try:
            number = int(entry)
            return True if 1 <= number <= self.dim else False
        except ValueError:
            return False

    def convert_to_numbers(self):
        if self.array is None:
            return None
        self.sudoku = [[0 for j in range(self.dim)] for i in range(self.dim)]
        self.mask = [[False for j in range(self.dim)] for i in range(self.dim)]
        try:
            for i in range(self.dim):
                for j in range(self.dim):
                    cell = self.array[i][j]
                    if not self.is_empty(cell):
                        self.sudoku[i][j] = int(cell)
                        self.mask[i][j] = True

        except ValueError:
            return None

    def contains_duplicates(self, flat_array):
        numbers = set()
        for number in flat_array:
            if number > 0:
                if number in numbers:
                    return True
                else:
                    numbers.add(number)
        return False


class Particle:
    def __init__(self, sudoku, mask, dim):
        self.mask = mask
        self.dim = dim
        self.sudoku = self.random_complete(sudoku, mask)

    def random_complete(self, sudoku, mask):
        array = [[0 for j in range(self.dim)] for i in range(self.dim)]
        for i in range(self.dim):
            numbers = [i for i in range(1, 10)]
            for j in range(self.dim):
                if mask[i][j]:
                    array[i][j] = sudoku[i][j]
                    numbers.remove(sudoku[i][j])
            numbers = np.random.permutation(numbers)
            idx = 0
            for j in range(self.dim):
                if not mask[i][j]:
                    array[i][j] = numbers[idx]
                    idx += 1
        return array

    def get_fitness(self):
        return 1

    def get_position(self):
        return self.copy_of(self.sudoku)

    def copy_of(self, sudoku):
        copy = [[0 for j in range(self.dim)] for i in range(self.dim)]
        for i in range(self.dim):
            for j in range(self.dim):
                copy[i][j] = sudoku[i][j]
        return copy
