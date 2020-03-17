
from mpi4py import MPI
import h5py
import numpy as np


n = 100000000
channels = 4
num_processes = MPI.COMM_WORLD.size
rank = MPI.COMM_WORLD.rank  # The process ID (integer 0-3 for 4-process run)

np.random.seed(746574366 + rank)

f = h5py.File('parallel_test.hdf5', 'w', driver='mpio', comm=MPI.COMM_WORLD)
dset = f.create_dataset('test', (channels, n), dtype='f')

for i in range(channels):
    if i % num_processes == rank:
       #print("rank = {}, i = {}".format(rank, i))
       data = np.random.uniform(size=n)
       dset[i] = data

f.close()
