#!/bin/bash -l

veros resubmit -i 50_years -n 8 -l 1944000 -c "mpirun -n 4 python3 2degree_run.py -n 2 2" --callback "./runsim.sh"

