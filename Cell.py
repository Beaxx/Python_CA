# person {0,1} with 0 = free Space, 1 = person
# wealth {0,1,2,3} with 0 = free Space, 1 = poor, 2 = medium, 3 = rich

class Cell:
    def __init__(self, vector):
        self.state_person = vector[0]
        self.state_wealth = vector[1]
