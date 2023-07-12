

WORD=$1

for dir in `ls -d */`; do cd $dir; echo $dir; grep -e "$WORD" generate.log; cd ..; done
