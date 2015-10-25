class Debugger:
    def __init__(self, on=False, cell=False, table=False):
        self.on = on
        self.cell = cell
        self.table = table

    def print_cell(self, string):
        if self.on or self.cell:
            print(string)


    def print_table(self, table):
        if self.on or self.table:
            print(table)

