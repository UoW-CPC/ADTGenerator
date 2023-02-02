#!/bin/bash

if [ -z "$1" ] ; then
  echo "Argument is missing. Please, specify a DMA json file as argument!"
  exit 1
fi

token=`cat emg_fetched_access_token`

curl https://dbs-api.emgora.eu/v1/emgadt/generate -X POST -H "Authorization: Bearer $token" -H "Content-Type: application/json" -d @"$1" 
