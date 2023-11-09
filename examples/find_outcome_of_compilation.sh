

for dir in `ls -d */`; 
	do 
		cd $dir;

		START=`grep -e "Generating ADT for Process" generate.log | grep -e "starts..."`
		FINISH=`grep -e "Generating ADT for Process" generate.log | grep -e "finished."`;

		DMA=`echo $START | sed -e 's/Generating ADT for Process //' | sed -e 's/ starts...//'`;
		#id=`echo $DMA | cut -f3 -d"\""`
		id=""
		name=`echo $DMA | cut -f2 -d"\""`

		if [[ ! -z "$FINISH" ]]; then
			echo "SUCCESS: $dir$id $name";
		else	
			echo "FAILURE: $dir$id $name";
		fi
		cd ..;
	done
