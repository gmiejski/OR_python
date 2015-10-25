class Debugger:
    def __init__(self, on=False, cell=False, table=False, history=False, program_info=False):
        self.program_info = program_info
        self.history = history
        self.on = on
        self.cell = cell
        self.history_file = open("history.txt", "w")
        self.table = table

    def print_cell(self, string):
        if self.on or self.cell:
            print(string)

    def print_table(self, table, you_sure=False):
        if self.on or self.table or you_sure:
            print(table)

    def print_history(self, row):
        if self.history:
            print(str(row))

    def print_program_info(self, string):
        if self.program_info:
            print(str(string))
