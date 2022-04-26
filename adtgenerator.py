import logging,logging.config

import adtg_conf
import adtg_restapi

log = None

if __name__ == '__main__':
    from adtg_conf import CONFIG

    adtg_conf.init()
    
    logging.config.dictConfig(adtg_conf.CONFIG['logging'])
    log = logging.getLogger('adtg')
    log.debug("CONFIG = "+str(adtg_conf.CONFIG))

    if not adtg_conf.CONFIG.get('generator',dict()).get('working_directory',None):
        raise Exception("No working_directory defined in config file")
    
    if not adtg_conf.CONFIG.get('generator',dict()).get('imports_directory',None):
        raise Exception("No imports_directory defined in config file")

    adtg_restapi.init()

    adtg_restapi.app.run(debug=adtg_conf.CONFIG.get('service', dict()).get('flask_debug_mode', True), 
            host=adtg_conf.service_host, 
            port=adtg_conf.service_port)
