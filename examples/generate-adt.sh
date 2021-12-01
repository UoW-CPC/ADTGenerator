#!/bin/bash

if [ -z "$1" ] ; then
  echo "Argument is missing. Please, specify a DMA json file as argument!"
  exit 1
fi

curl http://127.0.0.1:4000/v1/adtg/generate -X POST -H "Content-Type: application/json" -d @"$1" 
