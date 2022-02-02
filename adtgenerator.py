import logging,logging.config

import adtg_conf
import adtg_restapi

from compiler import compiler

log = None

if __name__ == '__main__':
    from adtg_conf import CONFIG

    adtg_conf.init()
    
    logging.config.dictConfig(adtg_conf.CONFIG['logging'])
    log = logging.getLogger('adtg')
    log.debug("CONFIG = "+str(adtg_conf.CONFIG))
    
    compiler_log = logging.getLogger('adtg_compiler')
    compiler.init(adtg_conf.CONFIG.get('compiler',dict()).get('template_directory',None), 
                  adtg_conf.CONFIG.get('compiler',dict()).get('modules',None),
                  compiler_log)
    
    adtg_restapi.init()

    adtg_restapi.app.run(debug=adtg_conf.CONFIG.get('service', dict()).get('flask_debug_mode', True), 
            host=adtg_conf.service_host, 
            port=adtg_conf.service_port)
