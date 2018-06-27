import random as rnd
import pyglet


class Program:
    def __init__(self, window_width, window_height, cell_size, percent_fill):
        self.grid_width = int(window_width / cell_size)
        self.grid_height = int(window_height / cell_size)
        self.cell_size = cell_size
        self.percent_fill = percent_fill
        self.cells = []
        self.generate_cells()

    def generate_cells(self):
        for row in range(0, self.grid_height):
            self.cells.append([])
            for col in range(0, self.grid_width):
                # Bedingung für Befüllung einer Zelle und mit welchen Werten --> Cell Objekte nutzen
                if rnd.random() < self.percent_fill:
                    self.cells[row].append(1)
                else:
                    self.cells[row].append(0)

    def draw(self):
        for row in range(0, self.grid_height):
            for col in range(0, self.grid_width):
                if self.cells[row][col] == 1:
                    # (0, 0) (0, 20) (20, 0) (20, 20)
                    square_coords = (row * self.cell_size,                  col * self.cell_size,
                                     row * self.cell_size,                  col * self.cell_size + self.cell_size,
                                     row * self.cell_size + self.cell_size, col * self.cell_size,
                                     row * self.cell_size + self.cell_size, col * self.cell_size + self.cell_size)
                    pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
                                                 [0, 1, 2, 1, 2, 3],
                                                 ("v2i", square_coords))

    #Game of Life rules in Moore-Environment
    def run_rules(self):
        temp_grid = []
        for row in range(0, self.grid_height):
            temp_grid.append([])
            for col in range(0, self.grid_width):
                cell_sum = sum([self.get_cell_value(row - 1,    col),
                                self.get_cell_value(row - 1,    col - 1),
                                self.get_cell_value(row,        col - 1),
                                self.get_cell_value(row + 1,    col - 1),
                                self.get_cell_value(row + 1,    col),
                                self.get_cell_value(row + 1,    col + 1),
                                self.get_cell_value(row,        col + 1),
                                self.get_cell_value(row - 1,    col + 1)])

                if self.cells[row][col] == 0 and cell_sum == 3:
                    temp_grid[row].append(1)
                elif self.cells[row][col] == 1 and (cell_sum == 3 or cell_sum == 2):
                    temp_grid[row].append(1)
                else:
                    temp_grid[row].append(0)

        self.cells = temp_grid

    def get_cell_value(self, row, col):
        if row >= 0 and row < self.grid_height and col >= 0 and col < self.grid_width:
            return self.cells[row][col]
        return 0