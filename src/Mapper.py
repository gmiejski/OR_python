class Mapper():
    def __init__(self, N, rank, rows):
        self.rank = rank
        self.N = N
        self.rows = rows

    def to_inner(self, x, y):
        print("Mapping bacteria for rank " + str(self.rank) + ": (" + str(x) + "," + str(y) + ") -> (" + str(
            x - self.rows * self.rank) + "," + str(
            y) + ")")
        return int(x - self.rows * self.rank), int(y)

    def to_global(self, x, y):
        return int(x + self.rows * self.rank), int(y)
