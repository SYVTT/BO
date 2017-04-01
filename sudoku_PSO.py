class Swarm:
    sudoku = None
    mask = None
    array = None
    dim = 9

    def __init__(self, array):
        self.array = array

    def check_correctness(self):
        if self.array is None:
            return None

        if not self.check_if_numbers():
            return False

        self.convert_to_numbers()

        for i in range(9):
            row = self.get_row(self.sudoku, i)
            column = self.get_column(self.sudoku, i)
            box = self.get_box(self.sudoku, i)
            if self.contains_duplicates(row) or self.contains_duplicates(column) or self.contains_duplicates(box):
                return False
        return True

    def get_row(self, array, number):
        if not self.check_array_dim(array) or number >= self.dim or number < 0:
            return None
        return array[number]

    def get_column(self, array, number):
        if not self.check_array_dim(array) or number >= self.dim or number < 0:
            return None
        return [array[i][number] for i in range(9)]

    def get_box(self, array, number):
        # get one of the box as list
        #  1 2 3
        #  4 5 6
        #  7 8 9
        if not self.check_array_dim(array) or number >= self.dim or number < 0:
            return None

        row = (number - 1) // 3
        column = (number - 1) % 3
        return [array[3 * row][3 * column + i] for i in range(3)] + \
               [array[3 * row + 1][3 * column + i] for i in range(3)] + \
               [array[3 * row + 2][3 * column + i] for i in range(3)]

    def check_array_dim(self, array):
        if len(array) != self.dim:
            return False
        for row in array:
            if len(row) != self.dim:
                return False
        return True

    def check_if_numbers(self):
        if not self.check_array_dim(self.array):
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
            return True if 1 <= number <= 9 else False
        except ValueError:
            return False

    def convert_to_numbers(self):
        if self.array is None:
            return None
        self.sudoku = [[0 for j in range(9)] for i in range(9)]
        self.mask = [[False for j in range(9)] for i in range(9)]
        try:
            for i in range(9):
                for j in range(9):
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
    def __init__(self):
        pass
