#!/bin/bash

PDIR=env/adtg

echo "Reseting '$PDIR'"

rm -rf "$PDIR"

virtualenv -p python3 "$PDIR"
source "$PDIR"/bin/activate

REQFILEDIR=`dirname $0`
pip install -r $REQFILEDIR/requirements.txt 

curl -L https://github.com/kubernetes/kompose/releases/download/v1.26.1/kompose-linux-amd64 -o $PDIR/bin/kompose
chmod +x $PDIR/bin/kompose

#Note: IMPORTDIR must be a separate directory (will be deleted when reseting)
IMPORTDIR=./imports
rm -r $IMPORTDIR
mkdir -p $IMPORTDIR
curl -L https://github.com/micado-scale/tosca/releases/download/v0.11.0/micado_types.tar -o $IMPORTDIR/micado_types.tar
tar xvf $IMPORTDIR/micado_types.tar --directory $IMPORTDIR
rm $IMPORTDIR/micado_types.tar

set +ex
echo "Do not forget to activate your virtual environment: source $PDIR/bin/activate"
echo "If environment is activated, 'run.sh' to launch the ADT Generator service"

