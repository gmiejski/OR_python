class Bacteria:
    def __init__(self, target_x, target_y, chance=1.0):
        self.target_x = target_x
        self.target_y = target_y
        self.chance = chance

    def chance(self):
        return self.chance

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "Bac(" + str(self.target_x) + "," + str(self.target_y) + ")"