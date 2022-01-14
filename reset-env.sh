#!/bin/bash

PDIR=env/adtg

echo "Reseting '$PDIR'"

rm -rf "$PDIR"

virtualenv -p python3 "$PDIR"
source "$PDIR"/bin/activate
pip install -r requirements.txt 

curl -L https://github.com/kubernetes/kompose/releases/download/v1.26.1/kompose-linux-amd64 -o $PDIR/bin/kompose
chmod +x $PDIR/bin/kompose

set +ex
echo "Do not forget to activate your virtual environment: source $PDIR/bin/activate"
echo "If environment is activated, 'run.sh' to launch the ADT Generator service"

