import random as rnd
import config

prop_person = config.prop_person
prop_wealth = config.prop_wealth
prop_culture = config.prop_culture
prop_skin = config.prop_skin
state_person = 0
state_skin = ""
state_culture = ""


class Cell:
    def __init__(self, **kwargs):
        if prop_person > rnd.uniform(0.0, 1.0):     # Person
            self.state_person = 1
        else:
            self.state_person = 0

        wealth_rnd = rnd.uniform(0.0, 1.0)          # Wealth
        if wealth_rnd < prop_wealth[2]:
            self.state_wealth = 3
        elif wealth_rnd < prop_wealth[1]:
            self.state_wealth = 2
        else:
            self.state_wealth = 1

        culture_rnd = rnd.uniform(0.0, 1.0)         # Culture
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

        skin_rnd = rnd.uniform(0.0, 1.0)            # Skin
        if skin_rnd < prop_skin[2]:
            self.state_skin = "W"
        elif skin_rnd < prop_skin[1]:
            self.state_skin = "B"
        else:
            self.state_skin = "A"

        if kwargs is not None:                      # **kwargs
            for key, value in kwargs.items():
                if key == "person":
                    self.state_person = value
                elif key == "wealth":
                    self.state_wealth = value
                elif key == "culture":
                    self.state_culture = value
                elif key == "skin":
                    self.state_skin = value

        # Cells that are uninhabited do not have religion oder skin-color
        if self.state_person == 0:
            self.state_culture = ""
            self.state_skin = ""
