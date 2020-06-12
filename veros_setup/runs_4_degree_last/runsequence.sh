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
    echo "THIS INTEGRATION TOOK: $day"d "$hour"h "$min"m "$sec"s
}
years=(0 5 10 15 20 25 30 35 40 45 50 55 60 65)
 
ran=0
#check all folders
maxran=0
if [ -n "$1" ]; then
	torun=0
	for y in ${years[@]}; do
		if [ -d "Run${y}" ]; then
			if test -f "Run${y}/run_${y}ma.current_run"; then
        		    if test $(head -n 1 "Run${y}/run_${y}ma.current_run") -lt "$1"; then
			    	torun=$((torun + $((${1} - $(head -n 1 "Run${y}/run_${y}ma.current_run")))))
			    fi
			    if test $(head -n 1 "Run${y}/run_${y}ma.current_run") -gt "$maxran"; then
			    	maxran=$(head -n 1 "Run${y}/run_${y}ma.current_run")
			    fi
			else
			    torun=$((torun + $1))
			fi
		fi
	done
	echo "We have to run ${torun} times"
	echo "starting with $1 ending with $2 and time steps $3 for each year in between"
	
	eachrun=$(seq $1 $3 $2)
	for r in ${eachrun[@]}; do
	  SECONDS=0
	  echo "Running until $r"
	  sh run_all.sh $r
	  duration=$SECONDS
	  show_time $(($duration))
	done
else
  echo "Supply length!"
fi


