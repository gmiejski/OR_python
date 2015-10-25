import time

from mpi4py import MPI

#########################




N = 6
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
processes = comm.Get_size()


asd = None
if rank == 0:
    asd = comm.recv( source=1)
    print(asd)

if rank == 1:
    time.sleep(1)
    comm.send([10], dest=0)