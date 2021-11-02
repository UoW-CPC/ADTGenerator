from flask import Flask, jsonify, request
import logging,logging.config, json
from flask_oidc import OpenIDConnect
import adtg_conf

from compiler import compiler

log = None
app = None
oidc = None
oidc_enabled = False

app = Flask(__name__)
app.config.from_object(__name__)

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


def perform_compile(type):
    global log
    log.debug('Compile '+type+' started')
    if oidc_enabled:
        token = oidc.get_access_token()    
    input_data = request.json
    if not input_data:
        raise RequestException(400, 'No valid JSON input found')
     
    log.debug('This is a JSON request: {0}'.format(input_data))
    print(input_data)
   
    template_file = adtg_conf.CONFIG.get('compiler',dict()).get('templates',dict()).get(type)
    result = compiler.compile(template_file, input_data, log)
    log.debug('Compile '+type+' finished')
    return jsonify(result), 200   


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
