#!/bin/bash

PDIR=env/adtg

echo "Reseting '$PDIR'"

rm -rf "$PDIR"

virtualenv -p python3 "$PDIR"
source "$PDIR"/bin/activate
pip install -r requirements.txt 

set +ex
echo "Now, you can execute 'run.sh' whenever you need the ADTG service"

