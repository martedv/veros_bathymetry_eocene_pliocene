#!/usr/bin/env bash
years=(0 5 10 15 20 25 30 35 40 45 50 55 60 65)

#  20 

ran=0

if [ -n "$1" ]; then
	for y in ${years[@]}; do
	  if [ -d "Run${y}" ]; then
		# for each dir
		ran=0
		if test -f "Run${y}/run_${y}ma.current_run"; then
		    ran=$(head -n 1 "Run${y}/run_${y}ma.current_run")
		fi
		if test "$1" -gt "$ran"; then
		  cd "Run${y}"

			for i in $(seq $(($ran+1)) 1 $1)
			do
        		   echo "Running ${y}Ma year: ${i}"
			   veros resubmit -i run_${y}ma -n $i -l 31104000 \
			    -c "mpirun -n 2 python3 4deg_basic_${y}.py -n 2 1"
			done
	          cd ".."
		fi
	  fi
	done
else
  echo "Supply length!"
fi


