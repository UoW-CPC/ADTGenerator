

for dir in `ls -d */`; 
	do 
		cd $dir;
	        #echo $dir

		START=`grep -e "Generating ADT for Process" generate.log | grep -e "starts..."`
		FINISH=`grep -e "Generating ADT for Process" generate.log | grep -e "finished."`;
		#echo "START: $START"
		#echo "FINISH: $FINISH"

		if [[ ! -z "$FINISH" ]]; then
			DMA=`echo $FINISH | sed -e 's/Generating ADT for Process //' | sed -e 's/ finished.//'`; 
			echo "SUCCESS: $dir $DMA";
		else	
			DMA=`echo $START | sed -e 's/Generating ADT for Process //' | sed -e 's/ starts...//'`;
			echo "FAILURE: $dir $DMA";
		fi
		cd ..;
	done
