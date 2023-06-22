

WORD=$1

for dir in `ls -d */`; do ./extract_fields_from_json.sh $dir | grep -e "DIR" -e "$WORD"; done
