from flask import Flask, jsonify
import yaml, logging, logging.config
from logging.config import dictConfig

# This is a dictionary to store configurartions that could be revised based on the application requirements
DEFAULT_LOGGING = {
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
}

app = Flask(__name__)
@app.route('/mdt', methods = ["GET", "POST"])

def compile_mdt():
    json_content = request.json
    try:
       result = json.load(json_content)
       logger.debug("Valid json!")
          
    except ValidationError as err:
      logger.error("No valid json is found!")
    # invoking library here ... #
    # .........
    # Then invoking the libarary
    app.logger.info('The library has been invoked!')
    mdt_test = "This is mdt"
    retrun mdt_test   

@app.route('/algodt', methods = ["GET", "POST"])

def compile_algodt():
    json_content = request.json
    try:
       result = json.load(json_content)
       logger.debug("Valid json!")
          
    except ValidationError as err:
       logger.error("No valid json is found!")
    # invoking library here ... #
    # .........
    # Then invoking the libarary
    app.logger.info('The library has been invoked!')
    mdt_test = "This is mdt"
    retrun mdt_test   

@app.route('/idt', methods = ["GET", "POST"])

def compile_idt():
    json_content = request.json
    try:
       result = json.load(json_content)
       logger.debug("Valid json!")
          
    except ValidationError as err:
      logger.error("No valid json is found!")
    # invoking library here ... #
    # .........
    # Then invoking the libarary
    app.logger.info('The library has been invoked!')
    mdt_test = "This is mdt"
    retrun mdt_test   

    # composing code comes here once the results are gotten from compile libraries and functions
# def compose_dt(mdt_test, algodt_test, idt_test):
#  ....  getting libraries and put the results in CSAR


if __name__ == '__main__':
    logging.config.dictConfig(DEFAULT_LOGGING)
    logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    logging.basicConfig(format = logFormatStr, filename = "global.log", level=logging.DEBUG)
    formatter = logging.Formatter(logFormatStr,'%m-%d %H:%M:%S')
    fileHandler = logging.FileHandler("summary.log")
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)
    app.logger.addHandler(fileHandler)
    app.logger.addHandler(streamHandler)
    app.logger.info("Logging is set up.")
    app.run(debug=True)
