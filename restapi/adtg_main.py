from flask import Flask, jsonify, request
import logging,logging.config, json
from flask_oidc import OpenIDConnect
import appconfig
log = None
app = Flask(__name__)

app.config.from_object(__name__)

appconfig.init_config()
logging.config.dictConfig(appconfig.CONFIG['logging'])
log = logging.getLogger('adtg_api')


# not part of the rest
oidc_enabled = appconfig.CONFIG.get('service', dict()).get('enable_oidc', False)
if oidc_enabled:
    with open(appconfig.secrets_json_path) as json_file:
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



@app.route(appconfig.rest_root_path + '/compile/mdt', methods = ["POST"])
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
    
    #check the type of input_data then log it
    # check how the input data could be converted to JSON
    #print(json.dumps(parsed, indent=4, sort_keys=True))
    # Token verification
    # ...
    # invoking library here ...
    # .........
    log.debug('Compile MDT finished')
    return jsonify(input_data), 200   
    #return 'This is MDT! {}'.format(app.config.get('logging'))  
@app.route(appconfig.rest_root_path + '/compile/algodt', methods = ["POST"])
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

@app.route(appconfig.rest_root_path + '/compile/idt', methods = ["POST"])
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
    app.run(debug=appconfig.CONFIG.get('service', dict()).get('flask_debug_mode', True), 
            host=appconfig.service_host, 
            port=appconfig.service_port)
