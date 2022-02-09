# ADT Generator
> This application is a FLASK-based service with [REST API](https://docs.google.com/document/d/17BnZmhsPvmcwem9EyXSTUissXRAz9NW3ornpWKea3qc), called ADT Generator developed for the [DigitiBrain project](https://digitbrain.eu/). It performs the conversion of [DigitBrain metadata assets](https://digitbrain.github.io/deployment/) into a ready-to-run multi-file [ADT](https://micado-scale.readthedocs.io/en/latest/application_description.html) to be deployed and orchestrated on the cloud by [MiCADO](https://micado-scale.readthedocs.io).

# Deployment

Everybody, who is interested in collecting experiences with ADTG should perform the following steps:

Step1: download the source code
```
git clone https://github.com/UoW-CPC/ADTGenerator.git github-adtg
```
Step2: create a virtual environment (called "adtg") and install requirements into it
```
cd github-adtg
./reset-env.sh
```
Step3: optionally, fine tune config.yaml under config subdirectory, only need to fine tune the directories, current settings are ok if source is cloned under /home/ubuntu/github-adtg)
```
vi github-adtg/config/config.yaml
```
Step4: launch the ADTGenerator service 
```
./run.sh
```
Step5: to invoke the ADT Generator with an example input json, run the following commands in another shell:
```
cd github-adtg/examples
./generate-adt.sh metadata_RISTRA.json
```
