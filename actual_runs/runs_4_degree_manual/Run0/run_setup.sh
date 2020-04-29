#!/bin/bash
echo "Year: $1"
echo "Number of years to run: $2"

veros resubmit -i run_$1ma -n $2 -l 31104000 \
    -c "mpirun -n 4 python3 4deg_basic_$1.py -n 2 2" \
    --callback "./run_setup.sh $1 $2"
