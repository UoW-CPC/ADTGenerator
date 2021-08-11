from flask import Flask
import yaml, logging, logging.config, json, os
from logging.config import dictConfig

app = Flask(__name__)

try: 
    with open('config_test.yaml', 'r') as f:
        config = yaml.safe_load(f)
        app.config.from_object(config)
        app.logger.info('Loading is successful')
except Exception as e:
    app.logger.error('Failed to load config file: '+ str(e))

logging.basicConfig(filename='record.log', level=logging.DEBUG, 
    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
fileHandler = logging.FileHandler("summary.log")
fileHandler.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
app.logger.addHandler(fileHandler)
app.logger.addHandler(streamHandler)
app.logger.info("Logging is set up.")


logging_configuration = app.config.get('LOGGING')
if logging_configuration:
    logging.config.dictConfig(logging_configuration)

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
    mdt_test = "This is mdt"
    return 'This is MDT! {}'.format(app.config.get('LOGGING'))   

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
    mdt_test = "This is mdt"
    return 'This is ADT! {}'.format(app.config.get('LOGGING'))  

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
    mdt_test = "This is mdt"
    return 'This is IDT! {}'.format(app.config.get('LOGGING'))  

# composing code comes here once the results are gotten from compile libraries and functions
# def compose_dt(mdt_test, algodt_test, idt_test):
#  ....  getting libraries and put the results in CSAR


if __name__ == '__main__':
    app.run(host='localhost', debug=True)


