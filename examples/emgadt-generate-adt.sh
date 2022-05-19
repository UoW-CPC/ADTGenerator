#!/bin/bash

if [ -z "$1" ] ; then
  echo "Argument is missing. Please, specify a DMA json file as argument!"
  exit 1
fi

curl https://dbs-api.emgora.eu/v1/emgadt/generate -X POST -H "Content-Type: application/json" -d @"$1" 
