# person {0,1} with 0 = free Space, 1 = person
# wealth {0,1,2,3} with 0 = free Space, 1 = poor, 2 = medium, 3 = rich
import random as rnd

'''Propabilities'''
prop_person = 0.4
prop_wealth = [1, 0.4, 0.1]
state_person = 0
state_wealth = 0

class Cell:
    def __init__(self, **kwargs):
        if prop_person > rnd.uniform(0.0, 1.0):  # Person
            self.state_person = 1
        else:
            self.state_person = 0

        local_rnd = rnd.uniform(0.0, 1.0)        # Wealth
        if local_rnd < prop_wealth[2]:
            self.state_wealth = 3
        elif local_rnd < prop_wealth[1]:
            self.state_wealth = 2
        elif local_rnd < prop_wealth[0]:
            self.state_wealth = 1
        else:
            self.state_wealth = 0

        if kwargs is not None:                    # **kwargs
            for key, value in kwargs.items():
                if key == "person":
                    self.state_person = value
                if key == "wealth":
                    self.state_wealth = value
