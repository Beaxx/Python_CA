# person {0,1} with 0 = free Space, 1 = person
# wealth {0,1,2,3} with 0 = free Space, 1 = poor, 2 = medium, 3 = rich
import random as rnd

'''Propabilities'''
prop_person = 0.2
prop_wealth = [1, 0.4, 0.1]
prop_culture = [1, 0.659, 0.397, 0.225, 0.059]  # Christians, Islam, Hinduism, No religion, Buddhism
prop_skin = [1, 0.66, 0.33]  # White, Black, Asian
state_person = 0
state_skin = ""
state_culture = ""


class Cell:
    def __init__(self, **kwargs):
        if prop_person > rnd.uniform(0.0, 1.0):  # Person
            self.state_person = 1
        else:
            self.state_person = 0

        wealth_rnd = rnd.uniform(0.0, 1.0)        # Wealth
        if wealth_rnd < prop_wealth[2]:
            self.state_wealth = 3
        elif wealth_rnd < prop_wealth[1]:
            self.state_wealth = 2
        else:
            self.state_wealth = 1

        culture_rnd = rnd.uniform(0.0, 1.0)       # Culture
        if culture_rnd < prop_culture[4]:
            self.state_culture = "B"
        elif culture_rnd < prop_culture[3]:
            self.state_culture = "N"
        elif culture_rnd < prop_culture[2]:
            self.state_culture = "H"
        elif culture_rnd < prop_culture[1]:
            self.state_culture = "I"
        else:
            self.state_culture = "C"

        skin_rnd = rnd.uniform(0.0, 1.0)          # Skin
        if skin_rnd < prop_skin[2]:
            self.state_skin = "W"
        elif skin_rnd < prop_skin[1]:
            self.state_skin = "B"
        else:
            self.state_skin = "A"

        if kwargs is not None:                    # **kwargs
            for key, value in kwargs.items():
                if key == "person":
                    self.state_person = value
                elif key == "wealth":
                    self.state_wealth = value
                elif key == "culture":
                    self.state_culture = value
                elif key == "skin":
                    self.state_skin = value

        if self.state_person == 0:
            self.state_culture = ""
            self.state_skin = ""
