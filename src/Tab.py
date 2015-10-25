import collections
from Field import Field


class Tab:
    def __init__(self, N, rank, rows, mapper, debugger):
        self.rows = rows
        self.rank = rank
        self.N = N
        self.mapper = mapper
        self.table = self.create_init_table(N, rows)
        self.infected = collections.defaultdict(lambda: collections.defaultdict(lambda: None))
        self.debugger = debugger
        self.x_range_up = None
        self.x_range_down = None
        self.init_x_range()

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
        for row in self.table:
            for cell in row:
                if cell.can_infect_others():
                    lists.append(cell.generate_bacterias())
        result = sum(lists, [])
        filtered_result = list(
            filter(lambda bacteria: 0 <= bacteria.target_x < self.N and 0 <= bacteria.target_y < self.N, result))
        self.debugger.print_cell("returning bacterias from process " + str(self.rank) + " : " + str(filtered_result))
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
                self.debugger.print_cell(
                    "Applying bacteria for rank= " + str(self.rank) + " -> (" + str(local_x) + "," + str(
                        local_y) + "), len(table)= " + str(len(self.table)) +
                    ", len(table[local_x])= " + str(len(self.table[local_x])))
                self.debugger.print_cell(str(self.table[local_x]))
                self.table[local_x][local_y].apply_bacteria(bacteria)

    def print(self, you_sure=False):
        for row in self.table:
            self.debugger.print_table(row, you_sure)

    def update_cells_state(self):
        for row in self.table:
            for cell in row:
                cell.update_state()

    def x_range(self):
        return self.x_range

    def init_x_range(self):
        x_range = set()
        for row in self.table:
            x_range.add(row[0].x)
        self.x_range_up = min(x_range)
        self.x_range_down = max(x_range)
        self.debugger.print_table("min and max for rank: " + str(self.rank) + " - " + str(self.x_range_up) + "," +
                                  str(self.x_range_down))

    def print_readable(self, you_sure):
        for row in self.table:
            mapped_row = list(map(lambda field: field.readable_state(), row))
            self.debugger.print_history(mapped_row)


