from Cell import *
import random as rnd

class CellAutomata:
    def __init__(self, window_width, window_height, cell_size, initial_prop_vector):
        self.grid_width = int(window_width / cell_size)
        self.grid_height = int(window_height / cell_size)
        self.cell_size = cell_size
        self.cells = []
        self.initial_apend_cells(initial_prop_vector)

    @staticmethod
    def generate_cell(prop_vector):
        creation_vector = [0] * len(prop_vector)
        for i in prop_vector:
            if prop_vector[0] > rnd.uniform(0.0, 1.0):  # Person
                creation_vector[0] = 1
            else:
                creation_vector[0] = 0

            local_rnd = rnd.uniform(0.0, 1.0)           # Wealth
            if local_rnd < prop_vector[1][2]:
                creation_vector[1] = 3
            elif local_rnd < prop_vector[1][1]:
                creation_vector[1] = 2
            elif local_rnd < prop_vector[1][0]:
                creation_vector[1] = 1
            else:
                creation_vector[1] = 0
        return Cell(creation_vector)

    # Initial grid fill
    def initial_apend_cells(self, prop_vector):
        for row in range(0, self.grid_height):
            self.cells.append([])
            for col in range(0, self.grid_width):
                self.cells[row].append(self.generate_cell(prop_vector))

    # TODO Weitere draw optionen für weitere cell-attribute
    # With cell_cize == 10
                    # (0, 0) (0, 10) (10, 0) (10, 10)
                    # square_coords = (row * self.cell_size,                  col * self.cell_size,
                    #                  row * self.cell_size,                  col * self.cell_size + self.cell_size,
                    #                  row * self.cell_size + self.cell_size, col * self.cell_size,
                    #                  row * self.cell_size + self.cell_size, col * self.cell_size + self.cell_size)


    # Game of Life rules in Moore-Environment
    # TODO Regeln auslagern
    def run_rules(self):
        temp_grid = []
        for row in range(0, self.grid_height):
            temp_grid.append([])
            for col in range(0, self.grid_width):
                cell_sum = sum([self.get_cell_person(row - 1, col),
                                self.get_cell_person(row - 1, col - 1),
                                self.get_cell_person(row, col - 1),
                                self.get_cell_person(row + 1, col - 1),
                                self.get_cell_person(row + 1, col),
                                self.get_cell_person(row + 1, col + 1),
                                self.get_cell_person(row, col + 1),
                                self.get_cell_person(row - 1, col + 1)])

                # Game of Life Rule Set
                if self.cells[row][col].state[0] == 0 and cell_sum == 3:
                    temp_grid[row].append(Cell(1, 0))
                elif self.cells[row][col].state[0] == 1 and (cell_sum == 3 or cell_sum == 2):
                    temp_grid[row].append(Cell(1, 0))
                else:
                    temp_grid[row].append(Cell(0, 0))

        self.cells = temp_grid

    def get_cell_person(self, row, col):  # TODO Statt das Array seitlich zu begrenzen kreisrund gestalten
        if (0 <= row < self.grid_height) and (0 <= col < self.grid_width):
            return self.cells[row][col].state[0]
        return 0
