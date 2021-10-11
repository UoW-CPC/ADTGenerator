#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Dimitris Kagialis
# Created Date: 05/10/2021
# version ='1.0'
# ---------------------------------------------------------------------------
""" Compiler module
    Logs program flow and nested calls.
    Implementation:
        Use of the built-in logging package.
        Debugger can be initialized only once.
        Use of a decorator to wrap callee function and collect required information.
    Configuration parameters:
        path: path to debugging logs folder [Default value - project root path]
        folder: debugging logs folder name [Default value 'debug']
        level: debugging level - allowed values 'None', 'high', 'low', 'full' [default value 'None']
        - None, the debugger is disabled.
        - high, collects the caller module, function and line, and the callee module, function and line.
        - low, collects high + input arguments and return.
        - full, collects low + callee function globals.
        debug_scope: dictionary with packages, modules, functions to include in the debugging phase [default value -  empty dict, debugging enabled for the whole project]
    Functions:
        init - initialize the debugger.
        debug_func - debugger decorator, wraps the callee function and collects required information.
        debug - callable function of the decorator, enables the debugger to pass arguments in the decorator.
    Usage:
        To initialize the debugger:
            from utils import debugger
            debugger.init(path, folder, level, debug_scope)
        To use the debugger:
            from utils.debugger import debugger
            @debugger.debug
            def sammple_func():
                pass
 """
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
    global _templates_path
    global _templates_modules
    _templates_path = templates_path
    _templates_modules = templates_modules
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



