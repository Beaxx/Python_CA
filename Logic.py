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

    def initial_apend_cells(self, prop_vector):
        for row in range(0, self.grid_height):
            self.cells.append([])
            for col in range(0, self.grid_width):
                self.cells[row].append(self.generate_cell(prop_vector))

    def run_rules(self):
        temp_grid = []
        for row in range(0, self.grid_height):
            temp_grid.append([])
            for col in range(0, self.grid_width):
                environment = self.add_up_environment(row, col)

                # Game of Life Rule Set
                if self.cells[row][col].state_person == 0 and environment[0] == 3:
                    temp_grid[row].append(Cell([1, 0]))

                elif self.cells[row][col].state_person == 1 and (environment[0] == 3 or environment[0] == 2):
                    temp_grid[row].append(Cell([1, 0]))
                else:
                    temp_grid[row].append(Cell([0, 0]))

        self.cells = temp_grid

    # Moore Environment - Sphere
    def select_cells(self, row, col):

        # Normal
        if (0 < row < self.grid_height-1) and (0 < col < self.grid_width-1):
            return[[row - 1, col], [row - 1, col - 1], [row, col - 1], [row + 1, col - 1], [row + 1, col],
                   [row + 1, col + 1], [row, col + 1], [row - 1, col + 1]]

        # Top Left Corner
        elif 0 == row and col == 0:
            return [[self.grid_height-1, col], [self.grid_height-1, self.grid_width-1], [row, self.grid_width-1],
                    [row + 1, self.grid_width-1], [row + 1, col], [row + 1, col + 1], [row, col + 1],
                    [self.grid_height-1, col + 1]]

        # Top Border
        elif 0 == row and (0 < col < self.grid_width-1):
            return [[self.grid_height-1, col], [self.grid_height-1, col-1], [row, col - 1], [row + 1, col - 1],
                    [row + 1, col], [row + 1, col + 1], [row, col + 1], [self.grid_height-1, col + 1]]

        # Top Right Corner
        elif 0 == row and col == self.grid_width-1:
            return [[self.grid_height-1, col], [self.grid_height-1, col - 1], [row, col - 1], [row + 1, col - 1],
                    [row + 1, col], [row + 1, 0], [row, 0], [self.grid_height-1, 0]]

        # Left Border
        elif (0 < row < self.grid_height-1) and 0 == col:
            return [[row - 1, col], [row - 1, self.grid_width-1], [row, self.grid_width-1], [row + 1, self.grid_width-1],
                    [row + 1, col], [row + 1, col + 1], [row, col + 1], [row - 1, col + 1]]

        # Right Border
        elif (0 < row < self.grid_height-1) and col == self.grid_width-1:
            return [[row - 1, col], [row - 1, col - 1], [row, col - 1], [row + 1, col - 1], [row + 1, col],
                    [row + 1, 0], [row, 0], [row - 1, 0]]

        # Bottom Left Corner
        elif self.grid_height-1 == row and 0 == col:
            return [[row - 1, col], [row - 1, self.grid_width-1], [row, self.grid_width-1], [0, self.grid_width-1],
                    [0, col], [0, col + 1], [row, col + 1], [row - 1, col + 1]]

        # Bottom Border
        elif (self.grid_height-1 == row) and (0 < col < self.grid_width-1):
            return [[row - 1, col], [row - 1, col - 1], [row, col - 1], [0, col - 1], [0, col], [0, col + 1],
                    [row, col + 1], [row - 1, col + 1]]

        # Bottom Right Corner
        elif (self.grid_height-1 == row) and (self.grid_width-1 == col):
            return [[row - 1, col], [row - 1, col - 1], [row, col - 1], [0, col - 1], [0, col], [0, 0],
                    [row, 0], [row - 1, 0]]

    def add_up_environment(self, row, col):
        person = 0
        wealth = 0
        environment = self.select_cells(row, col)

        for i, element in enumerate(environment):
            person += self.cells[environment[i][0]][environment[i][1]].state_person
            if self.cells[environment[i][0]][environment[i][1]].state_person == 1:
                wealth += self.cells[environment[i][0]][environment[i][1]].state_wealth

        if person == 0:
            wealth_pp = 0
        else:
            wealth_pp = int(wealth / person)

        return [person, wealth, wealth_pp]
