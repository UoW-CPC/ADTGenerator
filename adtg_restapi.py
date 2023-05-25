from flask import Flask, jsonify, request, send_from_directory
import logging,logging.config, json, os
from flask_oidc import OpenIDConnect
from werkzeug.exceptions import BadRequest, InternalServerError
import adtg_conf
from functools import wraps
from typing import Any as EndpointResult

import adtg_generate
import adtg_compile

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
def route_not_found(error):
   log.error('REST route not supported'), 404
   return jsonify({"error_code": 404, "message":"the specified rest route is not supported by adtgenerator!"})

@app.errorhandler(InternalServerError)
def handle_unexpected_error(e: Exception) -> EndpointResult:
    log.exception('Unknown error', exc_info=e)
    return jsonify({
        'error_code': '500',
        'error_type': 'Internal Server Error',
    }), InternalServerError.code

@validate_json
def compile(type):
    global log
    log.debug('compile('+type+') invoked')
    if oidc_enabled:
        token = oidc.get_access_token()    
    input_data = request.get_json()
    log.debug('This is a JSON request: {0}'.format(input_data))
   
    try:
        template_file = adtg_conf.CONFIG.get('compiler',dict()).get('templates',dict()).get(type)
        template_dir = adtg_conf.CONFIG.get('compiler',dict()).get('template_directory')
        result = adtg_compile.compile(log, "", type, input_data, os.path.join(template_dir,template_file))
        log.debug('Compile '+type+' finished')
        return json.loads(json.dumps(result, sort_keys=True, indent=4, separators=(',', ': ')))
    except Exception as e:
        return jsonify({"error": str(e)})

def make_response(success, message, id):
    if adtg_conf.CONFIG.get('generator',dict()).get('s3_upload_config',dict()).get('enabled',False):
        s3config = adtg_conf.CONFIG['generator']['s3_upload_config']
        endpoint = s3config['s3urlprefix']
        rest_path = s3config['s3bucketname']
    else:
        endpoint = adtg_conf.CONFIG.get('service',dict()).get('public_endpoint')
        rest_path = "/".join([i.strip("/").lstrip("/") for i in [adtg_conf.CONFIG.get('service',dict()).get('rest_root_path'),"download"]])

    log_route = "/".join([i.strip("/").lstrip("/") for i in [endpoint, rest_path, str(id), adtg_generate.FILE_LOG]])
    if success:
        adt_route = "/".join([i.strip("/").lstrip("/") for i in [endpoint, rest_path, str(id), adtg_generate.FILE_OUT]])
    else:
        adt_route = None
    response = dict(success=success,
                    message=message,
                    log=log_route,
                    adt=adt_route)
    return json.loads(json.dumps(response, sort_keys=False, indent=4))

@validate_json
def generate():
    global log
    log.info('ADT generation invoked.')
    input_data = request.get_json()
    try:
        root_wd = adtg_conf.CONFIG.get('generator',dict())['working_directory']
        id = adtg_generate.init_working_directory(log, root_wd)
        log.info('  ID: '+id)
    except Exception as e:
        log.info('ADT generation finished with ERROR.')
        log.exception(e)
        return jsonify({"error": str(e)}), 500
    try:
        success, message = adtg_generate.perform_generate(log, root_wd, id, input_data)
        log.info('ADT generation finished with SUCCESS.')
        return make_response(success, message, id), 200
    except Exception as e:
        log.info('ADT generation finished with ERROR.')
        log.exception(e)
        if adtg_conf.CONFIG.get('generator',dict()).get('s3_upload_config',dict()).get("enabled",False):
            s3_upload_config = adtg_conf.CONFIG.get('generator').get('s3_upload_config')
            full_wd = os.path.join(root_wd, id)
            adtg_generate.upload_to_s3(log, s3_upload_config, full_wd, id, "", adtg_generate.FILE_LOG)
        return make_response(False, str(e), id), 400

def download(dir,file):
    global log
    log.debug("download() invoked: "+dir+"/"+file)
    root_wd = adtg_conf.CONFIG.get('generator',dict()).get('working_directory')
    return send_from_directory(directory=root_wd, path=os.path.join(dir,file))

def health():
    return '', 200

def init():
    global log, app, oidc, oidc_enabled, compile, generate, download

    logging.config.dictConfig(adtg_conf.CONFIG['logging'])
    log = logging.getLogger('adtg')
    
    oidc_enabled = adtg_conf.CONFIG.get('service', dict()).get('enable_oidc', False)
    oidc_require_token = adtg_conf.CONFIG.get('service', dict()).get('check_user_token', False)
    if oidc_enabled:
        with open(adtg_conf.secrets_json_path) as json_file:
            APP_CONFIG = json.load(json_file)
        app.config.update(APP_CONFIG)
        oidc = OpenIDConnect(app)
        compile = (oidc.accept_token(require_token=oidc_require_token))(compile)
        generate = (oidc.accept_token(require_token=oidc_require_token))(generate)
        download = (oidc.accept_token(require_token=oidc_require_token))(download)
        
    endpoint=adtg_conf.rest_root_path+'/compile/<type>'
    log.debug("Registering compile() method for endpoint "+endpoint)
    app.add_url_rule(endpoint, methods=['POST'], view_func=compile)
    
    endpoint=adtg_conf.rest_root_path+'/generate'
    log.debug("Registering generate() method for endpoint "+endpoint)
    app.add_url_rule(endpoint, methods=['POST'], view_func=generate)

    endpoint=adtg_conf.rest_root_path+'/download/<dir>/<file>'
    log.debug("Registering download() method for endpoint "+endpoint)
    app.add_url_rule(endpoint, methods=['GET'], view_func=download)
 
    endpoint=adtg_conf.rest_root_path+'/health'
    log.debug("Registering health() method for endpoint "+endpoint)
    app.add_url_rule(endpoint, methods=['GET'], view_func=health)

    return
