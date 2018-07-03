from Cell import *
import random as rnd
from decimal import Decimal, ROUND_HALF_UP

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
        print()

    def run_rules(self, period, weights):
        """
        Ruft verschiedene Rulesets auf, die verschiedene temporäre Grids erzeugen. Diese werden mit dem weights Faktor
        gewichtet und dann in einem neuen Zellen-Raster zusammengefasst.
        :param period: Iterationsperiode
        :param weights: Gewichtung der einzelnen Regeln
        """

        temp_grid = []
        temp_wealth_grid = [[[] for i in range(self.grid_height)] for j in range(self.grid_width)]
        temp_culture_grid = [[[] for i in range(self.grid_height)] for j in range(self.grid_width)]
        temp_skin_grid = [[[] for i in range(self.grid_height)] for j in range(self.grid_width)]

        # Apply Rules
        self.wealth_rule_rent(period)
        for row in range(0, self.grid_height):
            for col in range(0, self.grid_width):
                surrounding_coords = self.select_cells(row, col)
                environment = self.add_up_environment(row, col)

                # Wealth Rule
                return_value_wealth = self.wealth_rule(row, col, environment, surrounding_coords)

                if type(return_value_wealth) is Cell:
                    temp_wealth_grid[row][col] = return_value_wealth
                else:
                    temp_wealth_grid[return_value_wealth[0]][return_value_wealth[1]] = self.cells[row][col]
                    temp_wealth_grid[row][col] = Cell(person=0, wealth=rnd.choice([1, 2]))

                # Culture Rule
                return_value_culture = self.culture_rule(row, col, surrounding_coords)
                if type(return_value_culture) is Cell:
                    temp_culture_grid[row][col] = return_value_culture
                else:
                    temp_culture_grid[return_value_culture[0]][return_value_culture[1]] = self.cells[row][col]
                    temp_culture_grid[row][col] = Cell(person=0)

                # Skin Rule
                return_value_skin = self.skin_rule(row, col, surrounding_coords)
                if type(return_value_skin) is Cell:
                    temp_skin_grid[row][col] = return_value_skin
                else:
                    temp_skin_grid[return_value_skin[0]][return_value_skin[1]] = self.cells[row][col]
                    temp_skin_grid[row][col] = Cell(person=0)

        # Compose temp_grid
        for row in range(0, self.grid_height):
            temp_grid.append([])
            for col in range(0, self.grid_width):

                person_indication = weights[0] * temp_wealth_grid[row][col].state_person
                person_indication += weights[1] * temp_culture_grid[row][col].state_person
                person_indication += weights[2] * temp_skin_grid[row][col].state_person

                wealth_indication = temp_wealth_grid[row][col].state_wealth
                culture_indication = temp_culture_grid[row][col].state_culture
                skin_indication = temp_culture_grid[row][col].state_skin

                person = int(Decimal(person_indication/sum(weights)).quantize(0, ROUND_HALF_UP))
                if person == 0:
                    temp_grid[row].append(Cell(person=0, wealth=wealth_indication))
                elif person == 1 and culture_indication == "":
                    temp_grid[row].append(Cell(person=1, wealth=wealth_indication))
                else:
                    temp_grid[row].append(Cell(person=1,
                                               wealth=wealth_indication,
                                               culture=culture_indication,
                                               skin=skin_indication))
        self.cells = temp_grid

    # Wealth Ruleset (Rent)
    def wealth_rule_rent(self, period):
        """
        R1: Wennn eine freie Fläche für 5 Iterationsperioden nicht besetzt wurde, wird die Miete / der Preis um 1 gesenkt.
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
    def wealth_rule(self, row, col, environment, surrounding_coords):
        """
        R2: Wenn der durchschnittliche Wealth der Umgebung einer Person über 50% über dem eigenen Wealth liegt sucht
            die Person in ihrer Moore Umgebung eine Freie Fläche, deren Kosten gleich oder unter ihrem wealth sind.
            Ist keine solche Fläche verfügbar, verschwindet die Zelle und hinterlässt Wohnraum mit Kosten, die ihren
            Wohlstand um 1 übersteigen.
        R3: Wenn die Umgebung um eine Person im Durchschnitt 1.75 Stufen günstiger ist, wird die Person versuchen auf
            eine höherpreise Wohnfläche abzuwandern. Die Wahl, welche der möglichen Flächen ausgewählt wird ist zufällig
            Ist keine passende freie Fläche verfügbar, wander die Person ab.
        R4: Wenn der Preis für eine Wohnfläche auf 0 fällt,wird sie von einer zufälligen externen Person bezogen.
        R5: Wenn eine Wohnfläche 1.5x günstiger ist, als die Flächen in ihrer Umgebung, ändert sich ihr Preis:
            40% Preis fällt
            60% Preis steigt

        Ist eine Fläche 1.5x günstiger, als die umliegenden Flächen o. Personen, erhöht sich mit 70-Prozentiger
            ihre Preiskategorie um 1. Mit 30-Prozentiger wahrscheinlichkeit senken die umliegenden Flächen ihren Preis
            um 1.75 oder mehr Stufen niedriger ist, als
        :param row: Zeilenindex
        :param col: Spaltenindex
        :param environment: Wirtschaftlicher Zustand der umgebenden Zellen
        :param surrounding_coords: Die Koordinaten der umgebenden Zellen
        """

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
    def culture_rule(self, row, col, surrounding_coords):
        """
        Kulturen werden im Folgenden mit Religionen gleichgesetzt.

        R6: Wenn eine Religion in der Umgebung mehrheitlich vertreten ist und diese Religion nicht der des Zentrums
            einer Umgebung (Person) entspricht, versucht sich diese Person von der Religionsgruppe zu entfernen.
        @:return Eine Objekt des typ "Zelle" oder ein Koordinatenarray
        """
        moving_options = []
        religions = [0, 0, 0, 0, 0, 0]
        switcher = {
            "C": 0,
            "I": 1,
            "H": 2,
            "N": 3,
            "B": 4,
            "": 5,
        }

        # R6 Cell trys to avoid clusters of other religions
        if self.cells[row][col].state_person == 1:
            for coord in surrounding_coords:
                religions[switcher[self.cells[coord[0]][coord[1]].state_culture]] += 1
                if self.cells[coord[0]][coord[1]].state_person == 0:
                    moving_options.append(coord)

            for i, rel in enumerate(religions[:-1]):  # Neglecting empty religion because its tied to empty cells
                if sum(religions[:-1]) > 0:
                    if rel > 4 and rel / sum(religions[:-1]) > 0.50 and switcher[self.cells[row][col].state_culture] != i:
                        if len(moving_options) == 0:
                            return Cell(person=0)  # No moving options, religious minority leaves
                        else:
                            return rnd.choice(moving_options)
                    else:
                        return self.cells[row][col]
                else:
                    return self.cells[row][col]
        else:
            return self.cells[row][col]

    # Skin Ruleset
    def skin_rule(self, row, col, surrounding_coords):
        """
        Hautfarbe hat einen maßgeblichen Einfluss auf das Zugehörigkeitsgefühl einer Person zu einer Gruppe, sie ist
        somit auch wichtiges Kriterium für Segregation. Im folgenden wird nur von den drei Hautfarben White, Black und
        Asian ausgegangen, die gleichverteilt sind.

        R7: Wie bei Religion auch versuchen sich unterschiedliche Hautfarben aus dem Weg zu gehen. Entsprechend ähnlich
            sind sich die Regeln.

        :return: Ein Objekt des Typ Zelle oder ein Koordinaten-Array
        """

        moving_options = []
        skin = [0, 0, 0, 0]
        switcher = {
            "W": 0,
            "B": 1,
            "A": 2,
            "": 3,
        }

        # R7 Cell trys to avoid clusters of other skin colores
        if self.cells[row][col].state_person == 1:
            for coord in surrounding_coords:
                skin[switcher[self.cells[coord[0]][coord[1]].state_skin]] += 1
                if self.cells[coord[0]][coord[1]].state_person == 0:
                    moving_options.append(coord)

            for i, s in enumerate(skin[:-1]):  # Neglecting empty skin because its tied to empty cells
                if sum(skin[:-1]) > 0:
                    if s > 4 and s / sum(skin[:-1]) > 0.50 and switcher[self.cells[row][col].state_skin] != i:
                        if len(moving_options) == 0:
                            return Cell(person=0)  # No moving options, skin minority leaves
                        else:
                            return rnd.choice(moving_options)
                    else:
                        return self.cells[row][col]
                else:
                    return self.cells[row][col]
        else:
            return self.cells[row][col]

    # Moore Environment - Sphere
    def select_cells(self, row, col):
        """
        Das Raster des Zellularautomaten ist eine Kugel, entsprechend führen Grenzübertretungen nach
        oben und nach unten sowie in den Ecken zum Einbezug von Zellen der gegnüberliegenden Seite.

        :param row: Zeile
        :param col: Spalte
        :return: Eindimensionales array mit 8 Elementen: den Koordinaten der umliegenden Zellen
        """

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
