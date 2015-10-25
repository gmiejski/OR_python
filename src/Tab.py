import collections
from Field import Field


class Tab:
    def __init__(self, N, rank, rows, mapper):
        self.rows = rows
        self.rank = rank
        self.N = N
        self.mapper = mapper
        self.table = self.create_init_table(N, rows)
        self.infected = collections.defaultdict(lambda: {})

    def create_init_table(self, N, rows):
        tab = []
        for i in range(0, rows):
            row = []
            for j in range(0, N):
                global_x, global_y = self.mapper.to_global(i, j)
                row.append(Field(global_x, global_y))
            tab.append(row)
            assert len(row) == N
        assert len(tab) == rows
        return tab

    def create_bacterias(self):
        lists = []
        for x, y in self.infected.items():
            for xx, yy in y.items():
                lists.append(yy.generate_bacterias())
        result = sum(lists, [])
        filtered_result = list(filter(lambda bacteria: 0 <= bacteria.target_x < self.N and 0 <= bacteria.target_y < self.N, result))
        print("returning bacterias from process " + str(self.rank) + " : " + str(filtered_result))
        return filtered_result

    def filter_local_bacterias(self, bacterias_info):
        local = []
        remote = []
        for bacteria in bacterias_info:
            if self.is_local(bacteria):
                local.append(bacteria)
            else:
                remote.append(bacteria)
        return local, remote

    def is_local(self, bacteria):
        for row in self.table:
            for cell in row:
                if cell.can_get_bacteria(bacteria):
                    return True
        return False

    def update_table(self, bacterias):
        if bacterias is not None:
            for bacteria in bacterias:
                local_x, local_y = self.mapper.to_inner(bacteria.target_x, bacteria.target_y)
                print("Applying bacteria for " + str(local_x) + "," + str(local_y))
                got_infected = self.table[local_x][local_y].apply_bacteria(bacteria)
                if got_infected:
                    self.infected[local_x][local_y] = self.table[local_x][local_y]

    def print(self):
        for row in self.table:
            print(row)


