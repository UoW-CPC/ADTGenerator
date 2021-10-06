from flask import Flask, jsonify, request
import yaml, logging,logging.config, json, argparse
#from flask_oidc import OpenIDConnect
global CONFIG
log = None
app = Flask(__name__)
#oidc = OpenIDConnect(app)

# argument parsing

parser = argparse.ArgumentParser(description='DigitBrain ADT Generator: This service is used for compiling DigitBrain assets towards MiCADO ADT')
parser.add_argument('--port', dest = 'port_number', type = int, default = '5001',
                     help='Specifies the port number where the service should listen')

parser.add_argument('--config', dest = 'config_path', default = 'config_test.yaml' ,
                     help='Specifies the path to the configuration file')
args = parser.parse_args()

try:
    with open(args.config_path,'r') as conf_var:
      CONFIG = yaml.safe_load(conf_var)
except Exception as e:
     print('Cannot read configuration file:', args.config_path)
     print(e)

try:
    logging.config.dictConfig(CONFIG['logging'])
    log = logging.getLogger('adtg_compiler')
except Exception as e:
     log.info('Unable to initialize the dictionary')

log.info('ADT generator started.')


@app.route('/v1/adtg/compile/mdt', methods = ["GET", "POST"])
#@oidc.accept_token(require_token=True)
def compile_mdt():
    global log
    log.debug('Compile MDT started')
    input_data = request.stream.read()
    if not input_data:
        raise RequestException(400, 'Empty POST data')
    log.debug('Received data: {0}'.format(input_data))
    #print(json.dumps(parsed, indent=4, sort_keys=True))
    # Token verification
    # ...
    # invoking library here ...
    # .........
    log.debug('Compile MDT finished')
    return jsonify({'success':'This is MDT'}), 200   
    #return 'This is MDT! {}'.format(app.config.get('logging'))  
@app.route('/v1/adtg/compile/algodt', methods = ["GET", "POST"])
#@oidc.accept_token(require_token=True)
def compile_algodt():
    global log
    log.debug('Compile ALGODT started')
    # Token verification
    # ...
    # invoking library here ... #
    # .........
    log.debug('Compile ALGODT finished')
    return jsonify({'success':'This is ALGODT'}), 200   

@app.route('/v1/adtg/compile/idt', methods = ["GET", "POST"])
#@oidc.accept_token(require_token=True)
def compile_idt():
    global log
    log.debug('Compile IDT started')
    # Token versification
    # ...
    # invoking library here ... #
    # .........
    log.debug('Compile IDT finished')
    return jsonify({'success':'This is IDT'}), 200  

# composing code comes here once the results are gotten from compile libraries and functions
# def compose_dt(mdt_test, algodt_test, idt_test):
#  ....  getting libraries and put the results in CSAR

if __name__ == '__main__':
    logging.config.dictConfig(CONFIG['logging'])
    app.run(debug=True, port=args.port_number)


