from flask import Flask
import yaml, logging, logging.config, json
from logging.config import dictConfig

app = Flask(__name__)


# Reading the config file and initializing the config dictionary
try: 
    with open('config_test.yaml', 'r') as f:
        config = yaml.safe_load(f)
        app.config.from_object(config)
        app.logger.info('Loading is successful')
except Exception as e:
    app.logger.error('Failed to load config file: '+ str(e))

try:
    logging_configuration = app.config.get('logging')
    if logging_configuration:
        logging.config.dictConfig(logging_configuration)
except Exception as e:
    app.logger.error('Failed to initialize config dictionary: ' + str(e))

@app.route('/mdt', methods = ["GET", "POST"])

def compile_mdt():
  
    with open('sample.json') as j:
        try:
            result = json.load(j)
            app.logger.debug("Valid json!")
            
        except ValidationError as err:
            app.logger.error("No valid json is found!")
    # invoking library here ...
    # .........
    # Then invoking the libarary
    app.logger.info('The library has been invoked!')
    return 'This is MDT! {}'.format(app.config.get('logging'))   

@app.route('/algodt', methods = ["GET", "POST"])

def compile_algodt():
    with open('sample.json') as j:
        try:
            result = json.load(j)
            app.logger.debug("Valid json!")
            
        except ValidationError as err:
            app.logger.error("No valid json is found!")
    # invoking library here ... #
    # .........
    # Then invoking the libarary
    app.logger.info('The library has been invoked!')
    return 'This is ADT! {}'.format(app.config.get('logging'))  

@app.route('/idt', methods = ["GET", "POST"])

def compile_idt():
    with open('sample.json') as j:
        try:
            result = json.load(j)
            app.logger.debug("Valid json!")
            
        except ValidationError as err:
            app.logger.error("No valid json is found!")
    # invoking library here ... #
    # .........
    # Then invoking the libarary
    app.logger.info('The library has been invoked!')
    return 'This is IDT! {}'.format(app.config.get('logging'))  

# composing code comes here once the results are gotten from compile libraries and functions
# def compose_dt(mdt_test, algodt_test, idt_test):
#  ....  getting libraries and put the results in CSAR


if __name__ == '__main__':
    logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    logging.basicConfig(format = logFormatStr, filename = "record.log", level=logging.DEBUG)
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
    app.run(debug=True, port=5001)


