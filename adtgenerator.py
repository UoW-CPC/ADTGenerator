import logging.config
import adtg_conf, adtg_restapi
from compiler import compiler


adtg_restapi.init()


if __name__ == '__main__':
    from adtg_conf import CONFIG
    compiler.init(CONFIG['compiler'], adtg_restapi.log)
    adtg_restapi.app.run(debug=adtg_conf.CONFIG.get('service', dict()).get('flask_debug_mode', True), 
            host=adtg_conf.service_host, 
            port=adtg_conf.service_port)
