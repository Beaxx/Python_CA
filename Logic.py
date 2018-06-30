from Cell import *
import random as rnd

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
        self.rent = []

    @staticmethod
    def generate_cell():
        return Cell()

    def initial_apend_cells(self):
        for row in range(0, self.grid_height):
            self.cells.append([])
            for col in range(0, self.grid_width):
                self.cells[row].append(self.generate_cell())

    def run_rules(self, period, weights):
        """
        Nutzt verschiedene Rulesets, um ein neues
        :param period: Iterationsperiode
        """

        temp_grid = []
        temp_wealth_grid = [[[] for i in range(self.grid_height)] for j in range(self.grid_width)]
        temp_culture_grid = [[[] for i in range(self.grid_height)] for j in range(self.grid_width)]
        temp_age_grid = []

        # Wealth Grid
        self.wealth_rule_rent(period)
        for row in range(0, self.grid_height):
            for col in range(0, self.grid_width):
                environment = self.add_up_environment(row, col)
                return_value = self.wealth_rule(row, col, environment)

                if type(return_value) is Cell:
                    temp_wealth_grid[row][col] = return_value
                else:
                    temp_wealth_grid[return_value[0]][return_value[1]] = self.cells[row][col]
                    temp_wealth_grid[row][col] = Cell(person=0, wealth=rnd.choice([1, 2]))
        self.cells = temp_wealth_grid



    def wealth_rule_rent(self, period):
        """
        Wennn eine freie Fläche für 5 Iterationsperioden nicht besetzt wurde, wird die Miete / der Preis um 1 gesenkt.
        Die Miete ist mindestens 0.
        :param period: Iterationsperiode
        """
        if period == 0:
            for row in range(0, self.grid_height):
                self.rent.append([])
                for col in range(0, self.grid_width):
                    self.rent[row].append(self.cells[row][col].state_wealth)

        if period >= 5 and period % 5 == 0:
            temp_rent = []
            for row in range(0, self.grid_height):
                temp_rent.append([])
                for col in range(0, self.grid_width):
                    temp_rent[row].append(self.cells[row][col].state_wealth)
                    if self.cells[row][col].state_person == 0 and temp_rent[row][col] == self.rent[row][col]:
                        self.cells[row][col].state_wealth -= 1
            self.rent = temp_rent

    # Wealth Ruleset
    def wealth_rule(self, row, col, environment):
        """
        - PRIO 1 -
        R1: Wenn der durchschnittliche Wealth der Umgebung einer Person über 50% über dem eigenen Wealth liegt sucht
            die Person in ihrer Moore Umgebung eine Freie Fläche, deren Kosten gleich oder unter ihrem wealth sind.
            Ist keine solche Fläche verfügbar, verschwindet die Zelle und hinterlässt Wohnraum mit Kosten, die ihren
            Wohlstand um 1 übersteigen.
        R2: Wenn die Umgebung um eine Person im Durchschnitt 1.75 Stufen günstiger ist, wird die Person versuchen auf
            eine höherpreise Wohnfläche abzuwandern. Die Wahl, welche der möglichen Flächen ausgewählt wird ist zufällig
            Ist keine passende freie Fläche verfügbar, wander die Person ab.
        R3: Wenn der Preis für eine Wohnfläche auf 0 fällt,wird sie von einer zufälligen externen Person bezogen.
        R4: Wenn eine Wohnfläche 1.5x günstiger ist, als die Flächen in ihrer Umgebung, ändert sich ihr Preis:
            40% Preis fällt
            60% Preis steigt

        Ist eine Fläche 1.5x günstiger, als die umliegenden Flächen o. Personen, erhöht sich mit 70-Prozentiger
            ihre Preiskategorie um 1. Mit 30-Prozentiger wahrscheinlichkeit senken die umliegenden Flächen ihren Preis
            um 1.75 oder mehr Stufen niedriger ist, als
        :param row: Zeilenindex
        :param col: Spaltenindex
        :param environment:
        """

        surrounding_coords = self.select_cells(row, col)
        moving_options = []
        # R1 Environment persons are 1.5x richer then Cell Person--> Person is forced to move and rent increases
        if self.cells[row][col].state_person == 1 and (self.cells[row][col].state_wealth * 1.5 <= environment[3]):
            for i, cell_coord in enumerate(surrounding_coords):
                if self.cells[cell_coord[0]][cell_coord[1]].state_person == 0 and \
                   self.cells[cell_coord[0]][cell_coord[1]].state_wealth <= self.cells[row][col].state_wealth:
                    moving_options.append([cell_coord[0], cell_coord[1]])
            if len(moving_options) == 0:
                return Cell(person=0, wealth=self.cells[row][col].state_wealth+1)
            else:
                return rnd.choice(moving_options)

        # R2 Environment is 2 price levels cheaper/poorer then persons wealth -->
        #    Move to higher price Region if available (snop effect)
        elif self.cells[row][col].state_person == 1 and \
                (self.cells[row][col].state_wealth - 1.75 >= environment[2] / 8):
            for i, cell_coord in enumerate(surrounding_coords):
                if self.cells[cell_coord[0]][cell_coord[1]].state_person == 0 and \
                   self.cells[cell_coord[0]][cell_coord[1]].state_wealth <= self.cells[row][col].state_wealth:
                    moving_options.append([cell_coord[0], cell_coord[1]])
            if len(moving_options) == 0 and self.cells[row][col].state_wealth - 1 >= 0:  # Rich-Person leaves
                return Cell(person=0, wealth=self.cells[row][col].state_wealth - 1)
            elif len(moving_options) == 0 and self.cells[row][col].state_wealth - 1 < 0:  # Rich-Persoon leaves
                return Cell(person=0, wealth=0)
            else:
                return rnd.choice(moving_options)  # Person moves randomly in Moore-Environment

        # R3 Moving into cheap space from outside the metropolis
        elif self.cells[row][col].state_person == 0 and self.cells[row][col].state_wealth == 0:
            return Cell()

        # R4 Free space 1.5x cheaper then environment (freee + inhabited) --> Rent price changes
        elif self.cells[row][col].state_wealth * 1.5 <= environment[2] / 8:
            if rnd.uniform(0.0, 1.0) < 0.6:
                return Cell(person=0, wealth=self.cells[row][col].state_wealth+1)
            else:
                for i, cell_coord in enumerate(surrounding_coords):
                    if self.cells[cell_coord[0]][cell_coord[1]].state_person == 0 and \
                       self.cells[cell_coord[0]][cell_coord[1]].state_wealth - 1 >= 0:
                        self.cells[cell_coord[0]][cell_coord[1]].state_wealth -= 1

                    elif self.cells[cell_coord[0]][cell_coord[1]].state_person == 0 and \
                            self.cells[cell_coord[0]][cell_coord[1]].state_wealth - 1 < 0:
                        self.cells[cell_coord[0]][cell_coord[1]].state_wealth = 0
                return self.cells[row][col]
        else:
            return self.cells[row][col]  # Catch-All, if no rule applys cell stais unchanged

    # Culture Ruleset
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
