import random
from Bacteria import Bacteria
from State import State


class Field():
    # global x,y indexes
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = State()

    def generate_bacterias(self):
        bacterias = []
        if self.state.infected():
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
        elif self.state.protected():
            return False
        elif self.state.is_healthy():
            if random.random() < bacteria.chance:
                self.state.infect()
                return True
        return False

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "Field(" + str(self.x) + "," + str(self.y) + "," + str(self.state) + ")"

    def update_state(self):
        self.state.update_state()

    def can_infect_others(self):
        return self.state.infected()

    def readable_state(self):
        return str(self.state)