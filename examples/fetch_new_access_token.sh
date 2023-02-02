#!/bin/bash

source ./emg_credentials

filename="emg_fetched_access_token"

credentials_json="{ \"username\" : \"$EMG_USERNAME\", \"password\" : \"$EMG_PASSWORD\", \"grant_type\" : \"password\", \"client_id\" : \"$EMG_CLIENT_ID\", \"client_secret\" : \"$EMG_CLIENT_SECRET\" }"

result_json=$( curl -s -X POST https://dbs-api.emgora.eu/v1/emgum/api/tokens -H "Content-Type: application/json" -d "$credentials_json" )

echo "Token fetching invoked:"
echo " Return code: "`jq -r ".code" <<<"$result_json"` 
echo " Message: "`jq -r ".message" <<<"$result_json"`
echo " Expires in: "`jq -r ".expires_in" <<<"$result_json"`

token=$( jq -r ".access_token" <<<"$result_json" )
echo "$token" > $filename

#cat $filename
echo "Token stored in file: $filename" 

