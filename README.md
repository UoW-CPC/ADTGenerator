# REST-API-ADT-GENRATOR
> This application is a FLASK-based REST API, as a part of ADT geenrator for the DigitiBrain project. 

## Table of Contents

* [General info and structure](#general-information)
* [Using the API](#using-api)
* [Building the API](#build-api)


## General info and structure
- The REST API for the project uses the Python as a programming language and the Flask technology to interact with different components of the ADT geenrator. Considering the architectural design, in the first phase the API gets configurations from the publisher interface as well as the required libraries for the compilation and compositions. In practice, the API exposes two different functionalities. The first one is to invoke compile libraries based on three main libraries such as Microservice Description Template (MDT), Algorithm Description Template (ADT), and Infrastructure Description Template (IDT). After invoking these libraries in the compile function, the results are passed to the compose function where all the results from the invoking process are packed in a CSAR file and passed to the publisher interface. 
- All the operations in the API are logged and stored in a configuration dictionary. The logging levels of the API are categorized in `ERROR`, `INFO`, and `DEBUG`.  

## Using the API
- In order to run the API, it is required to execute the `python flask.py`
- Once the application starts to run, based on what has been set up in the designated routes in the API, it is required to execute a correct route in the web browser to access libraries and their contents. In the `flask.py` the routes are `/mdt`, `/adt`, and `/algodt`. Therefore, you may be able to access those route by typing `http://127.0.0.1/algodt`, `http://127.0.0.1/idt`, `http://127.0.0.1/mdt` in the web browser. By executing each of these URLs, the API will start to log the events for each function and library using any pre-defined configuration.       

## Building the API
- It is a best practice to dockerise the API and run it accordingly. To do this, first it is required to build the application using the following command:

                                         ```sudo docker build --tag adt-generator-app .```

- Once the image was build, the next step is running the API by executing the following command:
                                       
                        `sudo docker run --name flask-docker-demo-app -p 5001:5001 flask-docker-demo-app`



