from Cell import *

"""
CellAutomata hosts the rules and therefore the logic of the CA-Algorithm.
"""

class CellAutomata:
    def __init__(self, window_width, window_height, cell_size):
        self.grid_width = int(window_width / cell_size)
        self.grid_height = int(window_height / cell_size)
        self.cell_size = cell_size
        self.cells = []
        self.initial_apend_cells()

    @staticmethod
    def generate_cell():
        return Cell()

    def initial_apend_cells(self):
        for row in range(0, self.grid_height):
            self.cells.append([])
            for col in range(0, self.grid_width):
                self.cells[row].append(self.generate_cell())

    def run_rules(self):
        temp_grid = []
        for row in range(0, self.grid_height):
            temp_grid.append([])
            for col in range(0, self.grid_width):
                environment = self.add_up_environment(row, col)

                indication = 0
                indication = self.wealth_rule(row, col, environment, indication)
                if indication is Cell:
                    temp_grid[row].append(indication)
                    return

                # indication = self.culture_rule(self, indication)
                # TODO Funktionierenden Loop erzeugen
                if indication is int and indication < 0:
                    temp_grid[row].append(Cell(person=0, wealth=self.cells[row][col].state_wealth))
                elif indication is int and indication >= 0:
                    temp_grid[row].append(Cell(person=1, wealth=self.cells[row][col].state_wealth))

                else:
                    temp_grid[row].append(self.cells[row][col])

                # TODO Vergünstigung des Wohnraumes

                # # Game of Life Rule Set
                # if self.cells[row][col].state_person == 0 and environment[0] == 3:
                #     temp_grid[row].append(Cell(person=1, wealth=self.cells[row][col].state_wealth))
                # elif self.cells[row][col].state_person == 1 and (environment[0] == 3 or environment[0] == 2):
                #     temp_grid[row].append(Cell(person=1, wealth=self.cells[row][col].state_wealth))
                # else:
                #     temp_grid[row].append(Cell(person=0, wealth=self.cells[row][col].state_wealth))
        self.cells = temp_grid

    def wealth_rule(self, row, col, environment, indication):
        """
        - PRIO 1 -
        Wenn der durchschnittliche Wealth um eine Person über 50% über dem eigenen Wealth liegt sucht die Person in
        ihrer Moore Umgebung eine Freie Fläche, deren Kosten gleich oder unter ihrem wealth sind.
        Ist keine solche Fläche verfügbar, stirbt die zelle und hinterlässt wohngrund mit Ihrem Wealth als Kosten
        """
        surrounding_coords = self.select_cells(row, col)

        # Person is 1.5x poorer then surrounding Persons --> Person is forced to move
        if self.cells[row][col].state_person == 1 and (self.cells[row][col].state_wealth * 1.5 <= environment[3]):
            for i, cell_coord in enumerate(surrounding_coords):
                if self.cells[cell_coord[0]][cell_coord[1]].state_person == 0 and \
                   self.cells[cell_coord[0]][cell_coord[1]].state_wealth <= self.cells[row][col].state_wealth:
                    indication -= 1
                else:
                    indication += 1
            return indication

        # Free space 1.5x cheaper then environment (freee + inhabited) --> price increases
        elif self.cells[row][col].state_person == 0 and (self.cells[row][col].state_wealth * 1.5 <= environment[2] / 8):
            return Cell(person=0, wealth=self.cells[row][col].state_wealth+1)

    def culture_rule(self):
        """
        - Prio 2 -
        > Religion und Kultur zu nah beieinander<
        Zellen vermeiden den direkten Kontakt zu anderen Kulturen
            (Westlich, Slawisch, Islamisch, Sinisch, Afrikanisch, Hinduistisch)
        :return:
        """

    def age_rule(self):
        """
        - Prio 3 -
        Rentnerviertel
        :return:
        """

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
        wealth_p = 0
        wealth_t = 0
        environment = self.select_cells(row, col)

        for i, element in enumerate(environment):
            person += self.cells[environment[i][0]][environment[i][1]].state_person
            wealth_t += self.cells[environment[i][0]][environment[i][1]].state_wealth
            if self.cells[environment[i][0]][environment[i][1]].state_person == 1:
                wealth_p += self.cells[environment[i][0]][environment[i][1]].state_wealth

        if person == 0:
            wealth_pp = 0
        else:
            wealth_pp = wealth_p / person

        return [person, wealth_p, wealth_t, wealth_pp]
