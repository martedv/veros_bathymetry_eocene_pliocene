#!/usr/bin/env bash
years=( 0 5 10 15 20 25 30 35 40 45 50 55 60 65 )
#
#  20 

ran=0

function show_time () {
    num=$1
    min=0
    hour=0
    day=0
    if((num>59));then
        ((sec=num%60))
        ((num=num/60))
        if((num>59));then
            ((min=num%60))
            ((num=num/60))
            if((num>23));then
                ((hour=num%24))
                ((day=num/24))
            else
                ((hour=num))
            fi
        else
            ((min=num))
        fi
    else
        ((sec=num))
    fi
    echo "Expected time left: $day"d "$hour"h "$min"m "$sec"s
}

if [ -n "$1" ]; then
	torun=0
	for y in ${years[@]}; do
		if [ -d "Run${y}" ]; then
			if test -f "Run${y}/run_${y}ma.current_run"; then
			    torun=$((torun + $((${1} - $(head -n 1 "Run${y}/run_${y}ma.current_run")))))
			else
			    torun=$((torun + $1))
			fi
		fi
	done
	echo "We have to run ${torun} times"
	
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
        		   SECONDS=0 
			   veros resubmit -i run_${y}ma -n $i -l 31104000 \
			    -c "mpirun -n 4 python3 4deg_basic_${y}.py -n 2 2" &> /dev/null
          		   duration=$SECONDS
          		   torun=$((torun-1))
			   echo "$(($duration / 60)):$(($duration % 60))"
			   show_time $(($duration*torun))
			   
			done
	          cd ".."
		fi
	  fi
	done
else
  echo "Supply length!"
fi


