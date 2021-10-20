# REST-API-ADT-GENRATOR
> This application is a FLASK-based REST API, as a part of ADT generator for the DigitiBrain project. 

## Table of Contents

* [General info and structure](#general-information)
* [Using the API](#using-api)
* [Building the API](#build-api)


## General info and structure
- The REST API uses the Python and Flask to interact with different components of ADT generator. Considering the architectural design, in the first phase the API gets configurations from the publisher interface as well as the required libraries for the compilation and compositions. In practice, the API exposes two different functionalities. The first one is the invokation of compile libraries based on three main libraries, Microservice Description Template (MDT), Algorithm Description Template (ADT), and Infrastructure Description Template (IDT). After invoking these libraries in the compile function, the results are passed to the compose function where all the results from the invoking process are packed in a CSAR file and passed to the publisher interface. 
- All the operations in the API are logged and stored in a configuration dictionary. 

## Using the API
- It is noted that the API is configurable so that it is executable using default or customizable configuration. The execution of the API is possible through calling the API in the server side and sending post requests throug the client side. Accordingly, in the server side, execute the following command. Please note that the configuration could be set to any configuration such as port, config, path, etc. 

#### Example
`python3 flaskapp.py --config ./config/config.yaml --port 1234`


Then in the client side, it is necessary to send a post request. In the following example we use a JSON file to post it through a CURL command. 

#### Example
`curl -X POST -H "Content-Type: application/json" -d @examples/mdt.json http://<LOCAL_HOST>:5001/v1/adtg/compile/mdt`
    

## Building the API
- It is a best practice to dockerise the API and run it accordingly. To do this, first of all it is required to build the application using the following command:

                               sudo docker build --tag adt-generator-app .

- Once the image was build, the next step is running the API by executing the following command:
                                       
                 sudo docker run --name adt-generator-app -p 5001:5001 adt-generator-app


