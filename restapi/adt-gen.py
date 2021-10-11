from flask import Flask, jsonify, request
import yaml, logging,logging.config, json, argparse
from flask_oidc import OpenIDConnect
global CONFIG
log = None

app = Flask(__name__)

app.config.from_object(__name__)



# argument parsing

parser = argparse.ArgumentParser(description='DigitBrain ADT Generator: This service is used for compiling DigitBrain assets towards MiCADO ADT')


parser.add_argument('--config', dest = 'config_path', default = './config_test.yaml' ,
                    help='Specifies the path to the configuration file')

parser.add_argument('--host', dest='service_host', type = str, 
                    help = 'Specifies the host to connect service to')

parser.add_argument('--port', dest = 'service_port', type = int,
                    help='Specifies the port number where the service should listen')

parser.add_argument('--secrets', dest = 'secrets_json_path', type = str,
                    help='Specifies the list of secrets in a json file')


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

service_host = CONFIG.get('service',dict()).get('host','127.0.0.1')
service_host = args.service_host if args.service_host else service_host

service_port = CONFIG.get('service',dict()).get('port',4000)
service_port = args.service_port if args.service_port else service_port

rest_root_path = CONFIG.get('service',dict()).get('rest_root_path','/v1/adtg')

secrets_json_path = CONFIG.get('service',dict()).get('secrets_json_path', None)
secrets_json_path = args.secrets_json_path if args.secrets_json_path else secrets_json_path

#guarded with if oidc is enabled from config
oidc_enabled = CONFIG.get('service', dict()).get('enable_oidc', False)
if oidc_enabled:
    with open(secrets_json_path) as json_file:
        APP_CONFIG = json.load(json_file)
    app.config.update(APP_CONFIG)
    oidc = OpenIDConnect(app)

@app.route(rest_root_path + '/compile/mdt', methods = ["POST"])
#OIDC decorator should be able to be toggled on/off"
#solution: https://stackoverflow.com/questions/14636350/toggling-decorators
#@oidc.accept_token(require_token=CONFIG.get('service', dict()).get('check_user_token', False))
def compile_mdt():
    global log
    log.debug('Compile MDT started')
    if oidc_enabled:
        token = oidc.get_access_token()
    
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
@app.route(rest_root_path + '/compile/algodt', methods = ["POST"])
#@oidc.accept_token(require_token=CONFIG.get('service', dict()).get('check_user_token', False))
def compile_algodt():
    global log
    log.debug('Compile ALGODT started')
    if oidc_enabled:
        token = oidc.get_access_token()

    input_data = request.stream.read()
    if not input_data:
        raise RequestException(400, 'Empty POST data')
    log.debug('Received data: {0}'.format(input_data))
    # Token verification
    # ...
    # invoking library here ... #
    # .........
    log.debug('Compile ALGODT finished')
    return jsonify({'success':'This is ALGODT'}), 200   

@app.route(rest_root_path + '/compile/idt', methods = ["POST"])
#@oidc.accept_token(require_token=CONFIG.get('service', dict()).get('check_user_token', False))
def compile_idt():
    global log
    log.debug('Compile IDT started')
    if oidc_enabled:
        token = oidc.get_access_token()

    input_data = request.stream.read()
    if not input_data:
        raise RequestException(400, 'Empty POST data')
    log.debug('Received data: {0}'.format(input_data))
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
    app.run(debug=CONFIG.get('service', dict()).get('flask_debug_mode', True), 
            host=service_host, 
            port=service_port)
