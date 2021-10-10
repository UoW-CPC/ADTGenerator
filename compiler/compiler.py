#compiler.py

#init logger
import os.path
import sys

from utils.logger import logger
import inspect

#init jinja
from jinja2 import Environment, FileSystemLoader
_templates_path = None
_templates_modules = None

#init compiler (set jinja globals and logging level)
def init(templates_path, templates_modules):
    globals()['_templates_path'] = templates_path
    globals()['_templates_modules'] = templates_modules
    logger.info('Compiler has been initiated')


#compile jinja template (logger decorator)
#@logger_util.logger_func(__name__, __file__, inspect.currentframe().f_lineno)
def compile(type, metadata):
    # logger_util.caller = inspect.stack()[2][1]
    # logger_util.caller_line = inspect.stack()[2][2]
    env = Environment(loader=FileSystemLoader(_templates_path))
    dt = env.get_template(type)
    for module in _templates_modules:
        exec(module[1])
        for function in module[2]:
            function_call = f'{module[0]}.{function}'
            function_to_run = eval(function_call)
            dt.globals[function] = function_to_run
    return dt.render(metadata)



