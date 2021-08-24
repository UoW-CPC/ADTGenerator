# REST-API-ADT-GENRATOR
> This application is a FLASK-based REST API, as a part of ADT geenrator for the DigitiBrain project. 

## Table of Contents

* [General info and structure](#general-information)
* [Using the API](#using-api)
* [Building the API](#build-api)


## General info and structure
- The REST API for the project uses the Python as a programming language and the Flask technology to interact with different components of the ADT geenrator. Considering the architectural design, in the first phase the API gets configurations from the publisher interface as well as the required libraries for the compilation and compositions. In practice, the API exposes two different functionalities. The first one is to invoke compile libraries based on three main libraries such as Microservice Description Template (MDT), Algorithm Description Template (ADT), and Infrastructure Description Template (IDT). After invoking these libraries in the compile function, the results are passed to the compose function where all the results from the invoking process are packed in a CSAR file and passed to the publisher interface. 
- All the operations in the API are logged and stored in a configuration dictionary.   

## Using the API
- In order to run the API, it is required to run the following command:
`python flask.py`





