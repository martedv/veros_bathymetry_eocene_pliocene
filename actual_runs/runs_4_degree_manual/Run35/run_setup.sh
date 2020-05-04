#!/bin/bash
#echo "Year: $1"
#echo "Number of years to run: $2"

ran=0

if test -f "run_${1}ma.current_run"; then
    ran=$(head -n 1 "run_${1}ma.current_run")
fi

if test "$ran" -lt "$2"; then
veros resubmit -i run_$1ma -n $2 -l 31104000 \
    -c "mpirun -n 2 python3 4deg_basic_$1.py -n 2 1" \
    --callback "./run_setup.sh $1 $2"
fi


