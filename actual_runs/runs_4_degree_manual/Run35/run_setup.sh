veros resubmit -i run_45ma -n 1 -l 31104000 \
    -c "mpirun -n 4 python3 4deg_basic_10.py -n 2 2" \
    --callback "./run_setup.sh"
