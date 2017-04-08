import random
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


# OK
def get_row(array, number):
    return [i for i in array[number]]


# OK
def get_column(array, number, dim):
    return [array[i][number] for i in range(dim)]


# OK
def get_box(array, number):
    # get one of the box as list
    #  1 2 3
    #  4 5 6
    #  7 8 9

    row = (number - 1) // 3
    column = (number - 1) % 3
    return [array[3 * row][3 * column + i] for i in range(3)] + \
           [array[3 * row + 1][3 * column + i] for i in range(3)] + \
           [array[3 * row + 2][3 * column + i] for i in range(3)]


# OK
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
    number_of_particles = 100
    number_of_iterations = 1000
    particles = None
    best_fitness = 0
    best_position = None
    row_nums = None

    def __init__(self, array, w, f_1, f_2):
        self.array = array
        self.w = w
        self.f_1 = f_1
        self.f_2 = f_2

    def start(self):
        print_sudoku(self.sudoku, self.dim)
        self.particles = [Particle(self.sudoku, self.mask, self.dim, self.row_nums, self.w, self.f_1, self.f_2)
                          for i in range(self.number_of_particles)]
        for particle in self.particles:
            if particle.get_best_fitness() > self.best_fitness:
                self.best_fitness = particle.get_best_fitness()
                self.best_position = particle.get_best_position()

        iteration = 0
        while self.best_fitness < 3*self.dim**2 and iteration < self.number_of_iterations:
            print(iteration)

            for particle in self.particles:
                particle.update_global_position(self.best_fitness, self.best_position)

            for particle in self.particles:
                particle.next_position()
                if particle.get_fitness() > self.best_fitness:
                    self.best_fitness = particle.get_fitness()
                    self.best_position = particle.get_position()
            iteration += 1

        print(self.best_fitness)
        print_sudoku(self.best_position, self.dim)

    def check_correctness(self):
        if self.array is None:
            return None

        if not self.check_if_numbers():
            return False

        self.convert_to_numbers()

        for i in range(self.dim):
            row = get_row(self.sudoku, i)
            column = get_column(self.sudoku, i, self.dim)
            box = get_box(self.sudoku, i)
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
            self.count_row_nums()

        except ValueError:
            return None

    def count_row_nums(self):
        self.row_nums = {}
        for i in range(self.dim):
            nums = []
            for num in self.mask[i]:
                if not num:
                    nums.append(num)
            self.row_nums[i] = nums

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
    def __init__(self, sudoku, mask, dim, row_nums, w, f_1, f_2):
        self.mask = mask
        self.dim = dim
        self.sudoku = self.random_complete(sudoku, mask)
        self.best_position = self.copy_of(self.sudoku)
        self.best_fitness = self.get_fitness()
        self.best_global_fitness = self.best_fitness
        self.best_global_position = self.best_position
        self.row_nums = row_nums
        self.w = w / 100
        self.f_1 = f_1 / 100
        self.f_2 = f_2 / 100

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

    # OK
    def get_fitness(self):
        sum = 0
        for i in range(self.dim):
            row = get_row(self.sudoku, i)
            column = get_column(self.sudoku, i, self.dim)
            box = get_box(self.sudoku, i)
            sum += len(set(row)) + len(set(column)) + len(set(box))
        return sum

    # OK
    def get_position(self):
        return self.copy_of(self.sudoku)

    def get_best_position(self):
        return self.copy_of(self.best_position)

    # OK
    def get_best_fitness(self):
        return self.best_fitness

    # OK
    def copy_of(self, sudoku):
        copy = [[0 for j in range(self.dim)] for i in range(self.dim)]
        for i in range(self.dim):
            for j in range(self.dim):
                copy[i][j] = sudoku[i][j]
        return copy

    # OK
    def update_global_position(self, best_global_fitness, best_global_position):
        if best_global_fitness > self.best_global_fitness:
            self.best_global_position = best_global_position
            self.best_global_fitness = best_global_fitness

    def next_position(self):
        possible_rows = [i for i in range(self.dim) if len(self.row_nums[i]) >= 2]
        # row = random.choice(possible_rows)
        for row in possible_rows:
            self_row = get_row(self.sudoku, row)
            local_row = get_row(self.best_position, row)
            global_row = get_row(self.best_global_position, row)

            new_row = self.crossover(self_row, local_row, global_row)

            if random.uniform(0, 1) < 0.4:
                possible_indexes = [i for i in range(self.dim) if not self.mask[row][i]]
                a, b = random.sample(range(0, len(possible_indexes)), 2)
                # not sure
                a = possible_indexes[a]
                b = possible_indexes[b]
                tmp = new_row[a]
                new_row[a] = new_row[b]
                new_row[b] = tmp

            for i in range(self.dim):
                self.sudoku[row][i] = new_row[i]

        fitness = self.get_fitness()
        if fitness > self.best_fitness:
            self.best_fitness = fitness
            self.best_position = self.copy_of(self.sudoku)

    # OK
    def crossover(self, self_row, local_row, global_row):
        new_row = [0 for i in range(len(self_row))]
        for i in range(len(self_row)):
            # choice = random.randint(0, 2)
            choice = np.random.choice([0, 1, 2], p=[self.w, self.f_1, self.f_2])
            if choice == 0:
                new_row[i] = self_row[i]
                self.swap(i, new_row[i], local_row, global_row)
            elif choice == 2:
                new_row[i] = local_row[i]
                self.swap(i, new_row[i], self_row, global_row)
            else:
                new_row[i] = global_row[i]
                self.swap(i, new_row[i], self_row, local_row)

        for i in range(self.dim):
            if new_row[i] == 0:
                print("ERROR")

        return new_row

    # OK
    def swap(self, position, number, a, b):
        idx = position
        while idx < len(a):
            if a[idx] == number:
                a[idx] = a[position]
                a[position] = number
            if b[idx] == number:
                b[idx] = b[position]
                b[position] = number
            idx += 1
