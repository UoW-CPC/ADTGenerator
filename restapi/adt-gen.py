from flask import Flask
import yaml, logging, logging.config, json, os
from logging.config import dictConfig
from app_config import LOG_FORMAT, CONF

app = Flask(__name__)

try:
    logging_configuration = app.config.update(CONF)
    if logging_configuration:
        logging.config.dictConfig(logging_configuration)
except Exception as e:
    app.logger.error('Failed to update config dictionary: ' + str(e))

@app.route('/mdt', methods = ["GET", "POST"])

def compile_mdt():
  

    # invoking library here ...
    # .........
    # Then invoking the libarary
    app.logger.info('The library has been invoked!')
    return 'This is MDT! {}'.format(app.config.get('logging'))   

@app.route('/algodt', methods = ["GET", "POST"])

def compile_algodt():

    # invoking library here ... #
    # .........
    # Then invoking the libarary
    app.logger.info('The library has been invoked!')
    return 'This is ADT! {}'.format(app.config.get('logging'))  

@app.route('/idt', methods = ["GET", "POST"])

def compile_idt():

    # invoking library here ... #
    # .........
    # Then invoking the libarary
    app.logger.info('The library has been invoked!')
    return 'This is IDT! {}'.format(app.config.get('logging'))  

# composing code comes here once the results are gotten from compile libraries and functions
# def compose_dt(mdt_test, algodt_test, idt_test):
#  ....  getting libraries and put the results in CSAR


if __name__ == '__main__':
    logging.basicConfig(format = LOG_FORMAT, filename = "record.log", level=logging.DEBUG)
    formatter = logging.Formatter(LOG_FORMAT,'%m-%d %H:%M:%S')
    fileHandler = logging.FileHandler("summary.log")
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)
    app.logger.addHandler(fileHandler)
    app.logger.addHandler(streamHandler)
    app.logger.info("Logging is set up.")
    app.run(debug=True, port=5001)


