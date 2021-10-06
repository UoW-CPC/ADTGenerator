from flask import Flask, jsonify, request
import yaml, logging, logging.config, json, argparse
from logging.config import dictConfig
from flask_restful import reqparse
#from flask_oidc import OpenIDConnect
from app_config import CONF

app = Flask(__name__)
#oidc = OpenIDConnect(app)


app_log = logging.getLogger('adtg_api')
app_log.info("ADT generator API Configuration")

compile_log = logging.getLogger('adtg_compiler')
compile_log.info("ADT generator compiler Configuration")

# argument parsing

parser = argparse.ArgumentParser(description='processing arguments.')
parser.add_argument('--port', type = int, default = '5001',
                     help='The services use this port')

parser.add_argument('--config', dest = 'config_path', default = './config_test.yaml' ,
                     help='Setting arguments')
args = parser.parse_args()

try:
    with open(args.config_path,'r') as conf_var:
      CONF.config(yaml.safe_load(conf_var))
except Exception as e:
     print('ERROR: Cannot read configuration file')

try:
    logging.config.dictConfig(CONF['logging'])
    log = logging.getLogger('adtg_compiler')
except Exception as e:
     print('ERROR: Cannot read configuration file', log)



@app.route('/v1/adtg/compile/mdt', methods = ["GET", "POST"])
#@oidc.accept_token(require_token=True)
def compile_mdt():
    # Token verification
    # ...
    # invoking library here ...
    # .........
    app.logger.info('The library has been invoked!')
    return jsonify({'success':'This is MDT'}), 200   
    #return 'This is MDT! {}'.format(app.config.get('logging'))  
@app.route('/v1/adtg/compile/algodt', methods = ["GET", "POST"])
#@oidc.accept_token(require_token=True)
def compile_algodt():
    # Token verification
    # ...
    # invoking library here ... #
    # .........
    app.logger.info('The library has been invoked!')
    return jsonify({'success':'This is ALGODT'}), 200   

@app.route('/v1/adtg/compile/idt', methods = ["GET", "POST"])
#@oidc.accept_token(require_token=True)
def compile_idt():
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
    logging.config.dictConfig(CONF['logging'])
    app.run(debug=True, port=5001)


