from flask import Flask, jsonify, request
import logging,logging.config, json
from flask_oidc import OpenIDConnect
from werkzeug.exceptions import BadRequest, InternalServerError
import adtg_conf
from compiler import compiler
from functools import wraps
from typing import Any as EndpointResult

from compiler import compiler

log = None
app = None
oidc = None
oidc_enabled = False

app = Flask(__name__)
app.config.from_object(__name__)

def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):                  
        try:
            request.get_json()
        except BadRequest as e:
            msg = "POST request must be a valid json"
            log.error(msg)
            return jsonify({"Bad Request": msg, "error code": 400})
        return f(*args, **kw)
    return wrapper

@app.errorhandler(404)
def page_not_found(error):
   log.error('Page not found'), 404
   return jsonify({"error_code": 404, "message":"Page not found; something went wrong!"})

@app.errorhandler(InternalServerError)
def handle_unexpected_error(e: Exception) -> EndpointResult:
    log.exception('Unknown error', exc_info=e)
    return jsonify({
        'error_code': '500',
        'error_type': 'Internal Server Error',
    }), InternalServerError.code


def perform_compile(type):
    global log
    log.debug('Compile '+type+' started')
    if oidc_enabled:
        token = oidc.get_access_token()    
    input_data = request.get_json()
    log.debug('This is a JSON request: {0}'.format(input_data))
   
    try:
        template_file = adtg_conf.CONFIG.get('compiler',dict()).get('templates',dict()).get(type)
        result = compiler.compile(template_file, input_data, log)
        log.debug('Compile '+type+' finished')
        return jsonify(result), 200   
    except Exception as e:
        return jsonify({"error": str(e)})

def init():
    global log, app, oidc, oidc_enabled, perform_compile

    logging.config.dictConfig(adtg_conf.CONFIG['logging'])
    log = logging.getLogger('adtg')

    
    oidc_enabled = adtg_conf.CONFIG.get('service', dict()).get('enable_oidc', False)
    oidc_require_token = adtg_conf.CONFIG.get('service', dict()).get('check_user_token', False)
    if oidc_enabled:
        with open(adtg_conf.secrets_json_path) as json_file:
            APP_CONFIG = json.load(json_file)
        app.config.update(APP_CONFIG)
        oidc = OpenIDConnect(app)
        perform_compile = (oidc.accept_token(require_token=oidc_require_token))(perform_compile)
        
    endpoint=adtg_conf.rest_root_path+'/compile/<type>'
    #log.debug("Registering compilation of "+target+" at endpoint "+endpoint)
    app.add_url_rule(endpoint, methods=['POST'], view_func=perform_compile)

    return
