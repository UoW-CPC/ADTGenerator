#compiler.py

#init logger
from utils import logger_util
import inspect

#init jinja
from jinja2 import Environment, FileSystemLoader
templates_path = None
templates_functions = None

#init compiler (set jinja globals and logging level)
def init(templates_path,templates_functions, logging_level=None):
    if logging_level == "INFO" or "DEBUG":
        logger_util._logging_level = logging_level
    globals()['templates_path'] = templates_path
    globals()['templates_functions'] = templates_functions

#compile jinja template (logger decorator)
@logger_util.logger_func(__name__, __file__, inspect.currentframe().f_lineno)
def compile(type, metadata):
    logger_util._caller = inspect.stack()[2][1]
    logger_util._line = inspect.stack()[2][2]
    env = Environment(loader=FileSystemLoader(templates_path))
    dt = env.get_template(type)
    for template_function in templates_functions:
        dt.globals[template_function] = globals()[template_function]
    return dt.render(metadata)


#TESTING
#passing functions to jinja templates (for Resmi's package)
def k8s2adt1(key):
    dict1 = {"var1":1,"var2":2,"var3":3}
    dict2 = {"var3": 1, "var4": 2, "var5": 3}
    if key == 1: return dict1
    if key == 2: return dict2
def k8s2adt2(key):
    dict3 = {"var11":11,"var22":22,"var33":33}
    dict4 = {"var33": 33, "var44": 44, "var55": 55}
    if key == 3: return dict3
    if key == 4: return dict4


