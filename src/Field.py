import random
from Bacteria import Bacteria


class Field():
    # global x,y indexes
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "healthy"

    def state(self):
        return self.state

    def generate_bacterias(self):
        bacterias = []
        if self.state == "infected":
            bacterias.append(Bacteria(self.x - 1, self.y))
            bacterias.append(Bacteria(self.x + 1, self.y))
            bacterias.append(Bacteria(self.x, self.y - 1))
            bacterias.append(Bacteria(self.x, self.y + 1))
            assert len(bacterias) == 4
        return bacterias

    def can_get_bacteria(self, bacteria):
        return bacteria.target_x == self.x and bacteria.target_y == self.y

    def apply_bacteria(self, bacteria):
        if bacteria.target_x != self.x or bacteria.target_y != self.y:
            raise Exception("Field (" + str(self.x) + "," + str(self.y) + " cannot get bacteria for cell: (" + str(
                bacteria.target_x) + "," + str(bacteria.target_y))
        elif self.state == "protected":
            return False
        elif self.state == "healthy":
            if random.random() < bacteria.chance:
                self.state = "infected"
                return True
        return False

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "Field(" + str(self.x) + "," + str(self.y) + "," + self.state[0:6] + ")"