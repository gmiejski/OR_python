from mpi4py import MPI
from Bacteria import Bacteria

from Mapper import Mapper
from Tab import Tab

#########################


def enum(**enums):
    return type('Enum', (), enums)

#########################

N = 6
debug = True
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
processes = comm.Get_size()

if N % processes != 0:
    print("Error - cannot partition the problem")
    comm.Abort()

rows = int(N / processes)
mapper = Mapper(N, rank, rows)
table = Tab(N, rank, rows, mapper)

initial_rank = int(processes / 2)
print("initial_rank = " + str(initial_rank))
if rank == initial_rank:
    target_x = N / 2
    target_y = N / 2
    print("First cell = " + str(target_x) + "," + str(target_y))
    initial_bacteria = Bacteria(target_x, target_y, chance=1)
    table.update_table([initial_bacteria])


def send_bacterias(processes, rank, bacterias_info):
    if rank - 1 >= 0:
        comm.send(bacterias_info, dest=rank - 1)
    if rank + 1 <= processes - 1:
        comm.send(bacterias_info, dest=rank + 1)


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
    print("Received :" + str
    (result) + " at rank : " + str(rank))
    return result


for i in range(0, 100):
    if debug:
        for i in range(0, processes):
            comm.Barrier()
            if i == rank:
                table.print()
        comm.Barrier()
    bacterias_info = table.create_bacterias()
    local_bacterias, bacterias_to_send = table.filter_local_bacterias(bacterias_info)
    print("returning bacterias from process " + str(rank) + " : LOCAL-> " + str(local_bacterias) + ", REMOTE-> " + str(
        bacterias_to_send))
    table.update_table(local_bacterias)
    send_bacterias(processes, rank, bacterias_to_send)
    received_bacterias = receive_bacterias(processes, rank)
    table.update_table(received_bacterias)
    print('Iteration: +' + str(i) + ' , after sending from ' + str(rank))
    comm.Barrier()

