from mpi4py import MPI
import sys
from Bacteria import Bacteria
from Debugger import Debugger

from Mapper import Mapper
from Tab import Tab

#########################


def enum(**enums):
    return type('Enum', (), enums)

#########################
comm = MPI.COMM_WORLD

if len(sys.argv) < 3:
    comm.Abort()

N = int(sys.argv[1])
iterations = int(sys.argv[2])
# debug = True
debugger = Debugger(on=False, cell=False, table=False, program_info=False, history=True)

rank = comm.Get_rank()
processes = comm.Get_size()

if N % processes != 0:
    print("Error - cannot partition the problem")
    comm.Abort()

rows = int(N / processes)
mapper = Mapper(N, rank, rows, debugger)
table = Tab(N, rank, rows, mapper, debugger)

initial_rank = int(processes / 2)
debugger.print_program_info("initial_rank = " + str(initial_rank))
if rank == initial_rank:
    target_x = int(N / 2)
    target_y = int(N / 2)
    debugger.print_program_info("First cell = " + str(target_x) + "," + str(target_y))
    initial_bacteria = Bacteria(target_x, target_y, chance=1)
    table.update_table([initial_bacteria])


def split_bacterias_per_process(bacterias_info, min_x, max_x):
    send_up = list(filter(lambda bacteria: bacteria.target_x == min_x - 1, bacterias_info))
    send_down = list(filter(lambda bacteria: bacteria.target_x == max_x + 1, bacterias_info))
    # print(len(send_up), len(send_down), len(bacterias_info))
    # print(bacterias_info, min_x, max_x)
    assert (len(send_up) + len(send_down)) == len(bacterias_info)
    return send_up, send_down


def send_bacterias(processes, rank, bacterias_info, min_x, max_x):
    bacterias_up, bacterias_down = split_bacterias_per_process(bacterias_info, min_x, max_x)
    if rank - 1 >= 0:
        comm.send(bacterias_up, dest=rank - 1)
    if rank + 1 <= processes - 1:
        comm.send(bacterias_down, dest=rank + 1)


def receive_bacterias(processes, rank):
    rec1 = None
    rec2 = None
    if rank - 1 >= 0:
        rec1 = comm.recv(source=rank - 1)
    if rank + 1 <= processes - 1:
        rec2 = comm.recv(source=rank + 1)
    if rec1 is None:
        result = rec2
    elif rec2 is None:
        result = rec1
    else:
        result = rec1.extend(rec2)
    debugger.print_cell("Received :" + str(result) + " at rank : " + str(rank))
    return result


def block_and_print_table(with_rank=False, initial=False, with_delimeter=False, delimeter="", you_sure=False):
    comm.Barrier()
    if initial and rank == 0:
        debugger.print_program_info("Initial table info")
    comm.Barrier()
    for pp in range(0, processes):
        comm.Barrier()
        if pp == rank:
            comm.Barrier()
            if with_rank:
                debugger.print_program_info("rank = " + str(rank))
            comm.Barrier()
            table.print(you_sure)
    comm.Barrier()
    if with_delimeter and rank == 0:
        debugger.print_table(delimeter, you_sure)
    comm.Barrier()


def print_readable_format(with_delimeter=False, delimeter="", you_sure=False):
    comm.Barrier()
    if rank == 0:
        print("#" + str(i))
    comm.Barrier()
    for pp in range(0, processes):
        comm.Barrier()
        if pp == rank:
            comm.Barrier()
            table.print_readable(you_sure)
    comm.Barrier()
    if with_delimeter and rank == 0:
        debugger.print_table(delimeter, you_sure)
    comm.Barrier()


block_and_print_table(with_delimeter=True)

start = MPI.Wtime()

for i in range(0, iterations):
    if rank == 0:
        debugger.print_program_info("Iteration: " + str(i))
    comm.Barrier()
    if debugger.table:
        block_and_print_table(with_delimeter=True, delimeter="***")
    elif debugger.history:
        print_readable_format(i,you_sure=True)
        # comm.Barrier()
    bacterias_created = table.create_bacterias()
    local_bacterias, remote_bacterias = table.filter_local_bacterias(bacterias_created)
    debugger.print_cell(
        "returning bacterias from process " + str(rank) + " : LOCAL-> " + str(local_bacterias) + ", REMOTE-> " + str(
            remote_bacterias))
    table.update_table(local_bacterias)
    send_bacterias(processes, rank, remote_bacterias, table.x_range_up, table.x_range_down)
    received_bacterias = receive_bacterias(processes, rank)
    table.update_table(received_bacterias)
    table.update_cells_state()
    debugger.print_cell('Iteration: +' + str(i) + ' , after sending from ' + str(rank))
    comm.Barrier()

# block_and_print_table(you_sure=True)
# block_and_print_table()

end = MPI.Wtime()
print(end - start)
