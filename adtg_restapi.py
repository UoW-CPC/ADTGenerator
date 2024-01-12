from flask import Flask, jsonify, request, send_from_directory
import logging,logging.config, json, os
from flask_oidc import OpenIDConnect
from werkzeug.exceptions import BadRequest, InternalServerError
import adtg_conf
from functools import wraps
from typing import Any as EndpointResult
import threading

import adtg_generate
import adtg_compile
import adtg_utils

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
        rest_path = os.path.join(s3config['s3dir'],str(id))
    else:
        endpoint = adtg_conf.CONFIG.get('service',dict()).get('public_endpoint')
        rest_path = "/".join([i.strip("/").lstrip("/") for i in [adtg_conf.CONFIG.get('service',dict()).get('rest_root_path'),"download",str(id)]])

    log_route = "/".join([i.strip("/").lstrip("/") for i in [endpoint, rest_path, adtg_generate.FILE_LOG]])
    if success:
        adt_route = "/".join([i.strip("/").lstrip("/") for i in [endpoint, rest_path, adtg_generate.FILE_OUT]])
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
        id = adtg_generate.init_working_directory(root_wd)
        log.info('  ID: '+id)
    except Exception as e:
        log.info('ADT generation finished with ERROR.')
        log.exception(e)
        response = jsonify({"error": str(e)})
        log.info("Response JSON: "+str(response))
        return response, 500
    try:
        success, message = adtg_generate.launch_generate(log, root_wd, id, input_data)
        log.info('ADT generation finished with SUCCESS.')
        response = make_response(success, message, id)
        log.info("Response JSON: "+str(response))
        return response, 200
    except Exception as e:
        log.info('ADT generation finished with ERROR.')
        log.exception(e)
        response = make_response(False, str(e), id)
        log.info("Response JSON: "+str(response))
        return response, 400

@validate_json
def start():
    global log
    log.info('ADT generation starts in the background...')
    input_data = request.get_json()
    try:
        root_wd = adtg_conf.CONFIG.get('generator',dict())['working_directory']
        id = adtg_generate.init_working_directory(root_wd)
        log.info('  ID: '+id)
    except Exception as e:
        log.info('Starting the ADT generation process FAILED')
        log.exception(e)
        response = jsonify( {"success": False,
                             "message": "Starting the ADT generation process FAILED\n"+
                                        str(e)} )
        log.info("Response JSON: "+str(response))
        return response, 500
    try:
        th = threading.Thread(  target=adtg_generate.launch_generate,
                                args=(log, root_wd, id, input_data) )
        th.daemon = True
        th.start()
        log.info('Starting the ADT generation process DONE')
        response = jsonify( {"success": True,
                             "id" : id,
                             "message": "Starting the ADT generation process DONE"} )
        log.info("Response JSON: "+str(response))
        return response, 200
    except Exception as e:
        log.info('Starting the ADT generation process FAILED.')
        log.exception(e)
        response = jsonify( {"success": False,
                             "message": "Starting the ADT generation process FAILED\n"+
                                        str(e)} )
        log.info("Response JSON: "+str(response))
        return response, 400


def status(id):
    log.debug("status() invoked: "+id)
    root_wd = adtg_conf.CONFIG.get('generator',dict()).get('working_directory')
    full_wd = os.path.join(root_wd, str(id))
    if os.path.isdir(full_wd):
        response_file_path = os.path.join(full_wd, adtg_utils.response_file_name)
        if os.path.isfile(response_file_path):
            response = adtg_utils.read_file(response_file_path)
            response_json = jsonify(response)
            return response, 200 if response["success"] else 400
    return jsonify({"message": "Cannot find ADT generation with this ID!"}), 400

def download(dir,file):
    global log
    log.debug("download() invoked: "+dir+"/"+file)
    root_wd = adtg_conf.CONFIG.get('generator',dict()).get('working_directory')
    return send_from_directory(directory=root_wd, path=os.path.join(dir,file))

def health():
    return '', 200

def init():
    global log, app, oidc, oidc_enabled, compile, generate, start, status, download

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
        start= (oidc.accept_token(require_token=oidc_require_token))(start)
        status = (oidc.accept_token(require_token=oidc_require_token))(status)
        download = (oidc.accept_token(require_token=oidc_require_token))(download)
        
    endpoint=adtg_conf.rest_root_path+'/compile/<type>'
    log.debug("Registering compile() method for endpoint "+endpoint)
    app.add_url_rule(endpoint, methods=['POST'], view_func=compile)
    
    endpoint=adtg_conf.rest_root_path+'/generate'
    log.debug("Registering generate() method for endpoint "+endpoint)
    app.add_url_rule(endpoint, methods=['POST'], view_func=generate)
    
    endpoint=adtg_conf.rest_root_path+'/start'
    log.debug("Registering start() method for endpoint "+endpoint)
    app.add_url_rule(endpoint, methods=['POST'], view_func=start)
    
    endpoint=adtg_conf.rest_root_path+'/status/<id>'
    log.debug("Registering status() method for endpoint "+endpoint)
    app.add_url_rule(endpoint, methods=['GET'], view_func=status)

    endpoint=adtg_conf.rest_root_path+'/download/<dir>/<file>'
    log.debug("Registering download() method for endpoint "+endpoint)
    app.add_url_rule(endpoint, methods=['GET'], view_func=download)
 
    endpoint=adtg_conf.rest_root_path+'/health'
    log.debug("Registering health() method for endpoint "+endpoint)
    app.add_url_rule(endpoint, methods=['GET'], view_func=health)

    return
