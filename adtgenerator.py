from flask import Flask, jsonify, request, current_app
import logging,logging.config, json
from flask.wrappers import Response
from flask_oidc import OpenIDConnect
from werkzeug.exceptions import BadRequest, InternalServerError
import adtg_conf
from compiler import compiler
from functools import wraps
from typing import Any as EndpointResult


log = None
input_data = None

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

def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):                  
        try:
            request.get_json()
        except BadRequest as e:
            msg = "POST request must be a valid json"
            log.error(msg)
            return jsonify({"error": msg}), 400
        return f(*args, **kw)
    return wrapper

@app.errorhandler(404)
def page_not_found(error):
   log.error('Page not found'), 400
   return jsonify({"Error":"Page not found; something went wrong!"}), 404

@app.errorhandler(InternalServerError)
def handle_unexpected_error(e: Exception) -> EndpointResult:
    log.exception('Unknown error', exc_info=e)
    return jsonify({
        'error_code': '500',
        'error_type': 'Internal Server Error',
    }), InternalServerError.code

@app.route(adtg_conf.rest_root_path + '/compile/mdt', methods = ["POST"])
@validate_json
#OIDC decorator should be able to be toggled on/off"
#solution: https://stackoverflow.com/questions/14636350/toggling-decorators
#@oidc.accept_token(require_token=CONFIG.get('service', dict()).get('check_user_token', False))
def compile_mdt():

    global log
    global input_data
    log.debug('Compile MDT started')
    if oidc_enabled:
        token = oidc.get_access_token()
    input_data = request.get_json()
    log.debug('This is a JSON request: {0}'.format(input_data))

    try:
        result = compiler.compile("mdt.yaml", input_data, log)
        return json.loads(json.dumps(result, sort_keys=True, indent=4, separators=(',', ': ')))
    except Exception as e:
        return jsonify({"error": str(e)})
        

@app.route(adtg_conf.rest_root_path + '/compile/algodt', methods = ["POST"])
@validate_json
#@oidc.accept_token(require_token=CONFIG.get('service', dict()).get('check_user_token', False))
def compile_algodt():
    global log
    log.debug('Compile ALGODT started')
    if oidc_enabled:
        token = oidc.get_access_token()    
    input_data = request.get_json()
    log.debug('This is a JSON request: {0}'.format(input_data))

    try:
        result = compiler.compile("algodt.yaml", input_data, log)
        return json.loads(json.dumps(result, sort_keys=True, indent=4, separators=(',', ': ')))
    except Exception as e:
        return jsonify({"error": str(e)})
         

@app.route(adtg_conf.rest_root_path + '/compile/idt', methods = ["POST"])
@validate_json
#@oidc.accept_token(require_token=CONFIG.get('service', dict()).get('check_user_token', False))
def compile_idt():
    global log
    log.debug('Compile IDT started')
    if oidc_enabled:
        token = oidc.get_access_token()    
    input_data = request.get_json()
    log.debug('This is a JSON request: {0}'.format(input_data))

    try:
        result = compiler.compile("idt.yaml", input_data, log)
        return json.loads(json.dumps(result, sort_keys=True, indent=4, separators=(',', ': ')))
    except Exception as e:
        return jsonify({"error": str(e)}) 

# composing code comes here once the results are gotten from compile libraries and functions
# def compose_dt(mdt_test, algodt_test, idt_test):
#  ....  getting libraries and put the results in CSAR



if __name__ == '__main__':
    from adtg_conf import CONFIG
    compiler.init(CONFIG['compiler'], log)
    app.run(debug=adtg_conf.CONFIG.get('service', dict()).get('flask_debug_mode', True), 
            host=adtg_conf.service_host, 
            port=adtg_conf.service_port)
