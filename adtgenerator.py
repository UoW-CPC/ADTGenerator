from flask import Flask, jsonify, request
import logging,logging.config, json
from flask_oidc import OpenIDConnect
import adtg_conf
from compiler import compiler
from compiler.tests import test_compiler_dicts

log = None


app = Flask(__name__)

app.config.from_object(__name__)


adtg_conf.init_config()
logging.config.dictConfig(adtg_conf.CONFIG['logging'])
log = logging.getLogger('adtg_api')


# not part of the rest
oidc_enabled = adtg_conf.CONFIG.get('service', dict()).get('enable_oidc', False)
if oidc_enabled:
    with open(adtg_conf.secrets_json_path) as json_file:
        APP_CONFIG = json.load(json_file)
    app.config.update(APP_CONFIG)
    oidc = OpenIDConnect(app)
# from here until the if main=name shoud go to the adtg_rest.py
class RequestException(Exception):
    def __init__(self, status_code, reason, *args):
        super(RequestException, self).__init__(*args)
        self.status_code, self.reason = status_code, reason
    def to_dict(self):
        return dict(status_code=self.status_code,
                    reason=self.reason,
                    message=str(self))


@app.errorhandler(RequestException)
def handled_exception(error):
    log.error('An exception occured: %r', error)
    #print error.to_dict()
    return jsonify(error.to_dict())


@app.route(adtg_conf.rest_root_path + '/compile/mdt', methods = ["POST"])
#OIDC decorator should be able to be toggled on/off"
#solution: https://stackoverflow.com/questions/14636350/toggling-decorators
#@oidc.accept_token(require_token=CONFIG.get('service', dict()).get('check_user_token', False))
def compile_mdt():
    global log
    log.debug('Compile MDT started')
    if oidc_enabled:
        token = oidc.get_access_token()    
    input_data = request.json
    if not input_data:
        raise RequestException(400, 'No valid JSON input found')
     
    log.debug('This is a JSON request: {0}'.format(input_data))
    print(input_data)
    # Token verification
    # ...
    # invoking library here ...
    result = compiler.compile("mdt.yaml", input_data, log)
    log.debug('Compile MDT finished')
    return jsonify(result), 200   
@app.route(adtg_conf.rest_root_path + '/compile/algodt', methods = ["POST"])
#@oidc.accept_token(require_token=CONFIG.get('service', dict()).get('check_user_token', False))
def compile_algodt():
    global log
    log.debug('Compile ALGODT started')
    if oidc_enabled:
        token = oidc.get_access_token()    
    input_data = request.json
    if not input_data:
        raise RequestException(400, 'No valid JSON input found')
     
    log.debug('This is a JSON request: {0}'.format(input_data))
    print(input_data)
    # Token verification
    # ...
    # invoking library here ...
    result = compiler.compile("algodt.yaml", input_data, log)
    log.debug('Compile AlgoDT finished')
    return jsonify(result), 200     

@app.route(adtg_conf.rest_root_path + '/compile/idt', methods = ["POST"])
#@oidc.accept_token(require_token=CONFIG.get('service', dict()).get('check_user_token', False))
def compile_idt():
    global log
    log.debug('Compile IDT started')
    if oidc_enabled:
        token = oidc.get_access_token()    
    input_data = request.json
    if not input_data:
        raise RequestException(400, 'No valid JSON input found')
     
    log.debug('This is a JSON request: {0}'.format(input_data))
    print(input_data)
    # Token verification
    # ...
    # invoking library here ...
    result = compiler.compile("idt.yaml", input_data, log)
    log.debug('Compile IDT finished')
    return jsonify(result), 200    

# composing code comes here once the results are gotten from compile libraries and functions
# def compose_dt(mdt_test, algodt_test, idt_test):
#  ....  getting libraries and put the results in CSAR


if __name__ == '__main__':
    from adtg_conf import CONFIG
    compiler.init(CONFIG['compiler'], log)
    app.run(debug=adtg_conf.CONFIG.get('service', dict()).get('flask_debug_mode', True), 
            host=adtg_conf.service_host, 
            port=adtg_conf.service_port)
