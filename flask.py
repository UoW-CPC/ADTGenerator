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
    app.logger.warning('A warning occurred')
    app.logger.error('An error occurred')
    app.logger.info('Info')
    return "mdt"

@app.route('/algodt', methods = ["GET", "POST"])

def compile_algodt():
    app.logger.warning('A warning occurred')
    app.logger.error('An error occurred')
    app.logger.info('Info')
    return "algodt"

@app.route('/idt', methods = ["GET", "POST"])

def compile_idt():
    app.logger.warning('A warning occurred')
    app.logger.error('An error occurred')
    app.logger.info('Info')
    return "idt"


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
