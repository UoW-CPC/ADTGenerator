#!/bin/bash

if [ -z "$1" ] ; then
  echo "Argument is missing. Please, specify an ID as argument!"
  exit 1
fi
#-w "%{http_code}"

curl -w "HTTP code: %{http_code}\n" http://127.0.0.1:4000/v1/adtg/status/$1 -X GET 
