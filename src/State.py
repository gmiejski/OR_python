class State():
    def __init__(self):
        self.INFECTED_LENGTH = 6
        self.PROTECTED_LENGTH = 4
        self.healthy = True
        self.infected_turns_left = 0
        self.protection_turns_left = 0

    def update_state(self):
        if not self.healthy:
            if self.infected_turns_left > 0:
                self.infected_turns_left -= 1
                if self.infected_turns_left == 0:
                    self.protection_turns_left = self.PROTECTED_LENGTH
            elif self.protection_turns_left > 0:
                self.protection_turns_left -= 1
                if self.protection_turns_left == 0:
                    self.healthy = True

    def protected(self):
        return self.protection_turns_left > 0

    def infected(self):
        return self.infected_turns_left > 0

    def is_healthy(self):
        return self.healthy

    def infect(self):
        if self.healthy:
            self.healthy = False
            self.infected_turns_left = self.INFECTED_LENGTH

    def __repr__(self):
        return str(self)

    def __str__(self):
        if self.is_healthy():
            return "OK"
        if self.infected():
            return "I" + str(self.infected_turns_left)
        if self.protected():
            return "P" + str(self.protection_turns_left)
        raise Exception("Wrong field state!!!!!!!!!!!!!!!!!")