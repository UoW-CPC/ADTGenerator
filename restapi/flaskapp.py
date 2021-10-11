from flask import Flask, jsonify, request
import logging,logging.config, json
from flask_oidc import OpenIDConnect
import appconfig

app = Flask(__name__)

app.config.from_object(__name__)

api_cf = appconfig.app_cfg

oidc_enabled = api_cf.CONFIG.get('service', dict()).get('enable_oidc', False)
if oidc_enabled:
    with open(api_cf.secrets_json_path) as json_file:
        APP_CONFIG = json.load(json_file)
    app.config.update(APP_CONFIG)
    oidc = OpenIDConnect(app)

@app.route(api_cf.rest_root_path + '/compile/mdt', methods = ["POST"])
#OIDC decorator should be able to be toggled on/off"
#solution: https://stackoverflow.com/questions/14636350/toggling-decorators
#@oidc.accept_token(require_token=CONFIG.get('service', dict()).get('check_user_token', False))
def compile_mdt():
    api_cf.log.debug('Compile MDT started')
    if oidc_enabled:
        token = oidc.get_access_token()    
    input_data = request.json  
    if not input_data:
        raise RequestException(400, 'Empty POST data')
    api_cf.log.debug('Received data: {0}'.format(input_data))

    try:
        input_data = request.json  # put JSON-data to a variable
    except json.decoder.JSONDecodeError as err:
        api_cf.log.debug("Invalid JSON: {err}") # in case json is invalid
        
    api_cf.log.debug('valid json', input_data)



    
    #check the type of input_data then log it
    # check how the input data could be converted to JSON
    #print(json.dumps(parsed, indent=4, sort_keys=True))
    # Token verification
    # ...
    # invoking library here ...
    # .........
    api_cf.log.debug('Compile MDT finished')
    return jsonify(input_data), 200   
    #return 'This is MDT! {}'.format(app.config.get('logging'))  
@app.route(api_cf.rest_root_path + '/compile/algodt', methods = ["POST"])
#@oidc.accept_token(require_token=CONFIG.get('service', dict()).get('check_user_token', False))
def compile_algodt():
    api_cf.log.debug('Compile ALGODT started')
    if oidc_enabled:
        token = oidc.get_access_token()

    input_data = request.stream.read()
    if not input_data:
        raise RequestException(400, 'Empty POST data')
    api_cf.log.debug('Received data: {0}'.format(input_data))
    # Token verification
    # ...
    # invoking library here ... #
    # .........
    api_cf.log.debug('Compile ALGODT finished')
    return jsonify({'success':'This is ALGODT'}), 200   

@app.route(api_cf.rest_root_path + '/compile/idt', methods = ["POST"])
#@oidc.accept_token(require_token=CONFIG.get('service', dict()).get('check_user_token', False))
def compile_idt():
    api_cf.log.debug('Compile IDT started')
    if oidc_enabled:
        token = oidc.get_access_token()

    input_data = request.stream.read()
    if not input_data:
        raise RequestException(400, 'Empty POST data')
    api_cf.log.debug('Received data: {0}'.format(input_data))
    # Token versification
    # ...
    # invoking library here ... #
    # .........
    api_cf.log.debug('Compile IDT finished')
    return jsonify({'success':'This is IDT'}), 200  

# composing code comes here once the results are gotten from compile libraries and functions
# def compose_dt(mdt_test, algodt_test, idt_test):
#  ....  getting libraries and put the results in CSAR


if __name__ == '__main__':
    logging.config.dictConfig(api_cf.CONFIG['logging'])
    app.run(debug=api_cf.CONFIG.get('service', dict()).get('flask_debug_mode', True), 
            host=api_cf.service_host, 
            port=api_cf.service_port)
