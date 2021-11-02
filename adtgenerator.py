import logging,logging.config, adtg_restapi
import adtg_conf
from compiler import compiler
import adtg_restapi


adtg_conf.init_config()
logging.config.dictConfig(adtg_conf.CONFIG['logging'])
log = logging.getLogger('adtg')
log.debug("CONFIG = "+str(adtg_conf.CONFIG))
compiler_log = logging.getLogger('adtg_compiler')
compiler.init(adtg_conf.CONFIG.get('compiler',dict()).get('template_directory',None),
adtg_conf.CONFIG.get('compiler',dict()).get('modules',None), log)
adtg_restapi.init()


if __name__ == '__main__':
    from adtg_conf import CONFIG
    compiler.init(CONFIG['compiler'], adtg_restapi.log)
    adtg_restapi.app.run(debug=adtg_conf.CONFIG.get('service', dict()).get('flask_debug_mode', True), 
            host=adtg_conf.service_host, 
            port=adtg_conf.service_port)
