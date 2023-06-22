#!/bin/sh

DIR=$1


echo "===>DIR: $DIR"
echo "==>DMA"
echo -n "Name:"
jq ."dma"."name" $DIR/inputs/input.json
echo -n "Author:"
jq ."dma"."author" $DIR/inputs/input.json
echo -n "Deployments:"
jq ."dma"."deployments" $DIR/inputs/input.json


echo "==>MODEL"
echo -n "Repository_uri:"
jq ."Model"."repository_uri" $DIR/inputs/input.json
echo -n "Path:"
jq ."Model"."path" $DIR/inputs/input.json
echo -n "Filename:"
jq ."Model"."filename" $DIR/inputs/input.json

echo "==>DATA"
IDMAX=`jq ".Data[]"."name" $DIR/inputs/input.json | wc -l`
for id in `seq 1 $IDMAX`; do
	ID=$((id-1))
	echo "=>DATA[$ID]";
	echo -n "Name:"
	jq ."Data[$ID]"."name" $DIR/inputs/input.json
	echo -n "Id:"
	jq ."Data[$ID]"."id" $DIR/inputs/input.json
done

echo "==>ALGORITHM"
echo -n "Name:"
jq ."Algorithm"."name" $DIR/inputs/input.json
echo -n "Author:"
jq ."Algorithm"."author" $DIR/inputs/input.json
echo -n "Deployment mapping:"
jq ."Algorithm"."deployment_mapping" $DIR/inputs/input.json
echo -n "Microservices:"
jq ."Algorithm"."list_of_microservices" $DIR/inputs/input.json


echo "==>MICROSERVICE"
IDMAX=`jq ".Microservices[]"."name" $DIR/inputs/input.json | wc -l`
for id in `seq 1 $IDMAX`; do
	ID=$((id-1))
	echo "=>MS[$ID]";
	echo -n "Name:"
	jq ."Microservices[$ID]"."name" $DIR/inputs/input.json
	echo -n "Author:"
	jq ."Microservices[$ID]"."author" $DIR/inputs/input.json
	echo -n "Deployment_format:"
	jq ."Microservices[$ID]"."deployment_format" $DIR/inputs/input.json
	echo -n "Deployment_data:"
	jq ."Microservices[$ID]"."deployment_data" $DIR/inputs/input.json
done
