from flask import Flask, jsonify, request
import yaml, logging, logging.config, json
from logging.config import dictConfig
from flask_restful import reqparse
#from flask_oidc import OpenIDConnect
from app_config import LOG_FORMAT, CONF

app = Flask(__name__)
#oidc = OpenIDConnect(app)
try:
    app.config.from_object(__name__)
    logging_configuration = app.config.update(CONF)
    if logging_configuration:
        logging.config.dictConfig(logging_configuration)
except Exception as e:
    app.logger.error('Failed to update config dictionary: ' + str(e))


@app.route('/v1/adtg/compile/mdt', methods = ["GET", "POST"])
#@oidc.accept_token(require_token=True)
def compile_mdt(id):
    parser = reqparse.Requestparser()
    parser.add_argument('id', type=str, required=True)
    id = args['id']
    # Token verification
    # ...
    # invoking library here ...
    # .........
    app.logger.info('The library has been invoked!')
    return jsonify({'success':'This is MDT'}), 200   

@app.route('/v1/adtg/compile/algodt', methods = ["GET", "POST"])
#@oidc.accept_token(require_token=True)
def compile_algodt(id):
    parser = reqparse.Requestparser()
    parser.add_argument('id', type=str, required=True)
    id = args['id']
    # Token verification
    # ...
    # invoking library here ... #
    # .........
    app.logger.info('The library has been invoked!')
    return jsonify({'success':'This is ALGODT'}), 200   

@app.route('/v1/adtg/compile/idt', methods = ["GET", "POST"])
#@oidc.accept_token(require_token=True)
def compile_idt(id):
    parser = reqparse.Requestparser()
    parser.add_argument('id', type=str, required=True)
    id = args['id']
    # Token versification
    # ...
    # invoking library here ... #
    # .........
    app.logger.info('The library has been invoked!')
    return jsonify({'success':'This is IDT'}), 200  

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


