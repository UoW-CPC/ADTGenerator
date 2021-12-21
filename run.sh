#!/bin/bash

set +ex

source ./env/adtg/bin/activate
python3 adtgenerator.py --config ./config/config.yaml
