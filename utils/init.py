#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Dimitris Kagialis
# Created Date: 05/10/2021
# version ='1.0'
# Contributors:
# Updated at  : 12/10/2021
# Tested at   : 12/10/2021
# ---------------------------------------------------------------------------
""" Init module
    Loads ADT generator configs from paths and initiate its components.
    Usage:
        To initialize the components:
            from utils.init import init
            init(path)
    Functions:
        init - initiate ADT generator components based on the loaded configs
        init_logger - initiate the logger
        init_debugger - initiate the debugger
        init_compiler - initiate the compiler
        init_restapi - initiate the restapi
    Implementation:
        Functional programming
    Tests: -
 """
# Module global imports
import sys

# Function to initiate the ADT-generator
def init(path):
    '''
    Load config YAML files from path and initiate components based on the loaded configs
    :param path: path to config files
    :return: None
    '''
    from utils import configs
    _configs =configs.load(path)
    init_logger(_configs.get('logger.yml'))
    init_debugger(_configs.get('debugger.yml'))
    init_compiler(_configs.get('compiler.yml'))
    init_restapi(_configs.get('restAPI.yml'))

# Function to initiate the logger
def init_logger(config):
    '''
    Initiate the logger based on the provided config
    :param config: dictionary with logger configs
    :return: None
    '''
    # Try to get configs from the dictionary, except use defaults
    try:
        path = config['logger']['path']
    except:
        path = sys.path[0]
    if path == None:
        path = sys.path[0]
    try:
        folder = config['logger']['folder']
    except:
        folder = 'logs'
    if folder == None:
        folder = 'logs'
    try:
        level = config['logger']['level']
    except:
        level = 'info'
    try:
        handler = config['logger']['handler']
    except:
        handler = 'file'
    # Import logger and initiate
    from utils import logger
    logger.init(path, folder, level, handler)
    # Test that logger can be initiated only once
    logger.init()

# Function to initiate the debugger
def init_debugger(config):
    '''
    Initiate the debugger based on the provided config
    :param config: dictionary with debugger configs
    :return: None
    '''
    # Try to get configs from the dictionary, except use defaults
    try:
        path = config['debugger']['path']
    except:
        path = sys.path[0]
    if path == None:
        path = sys.path[0]
    try:
        folder = config['debugger']['folder']
    except:
        folder = 'debugger'
    if folder == None:
        folder = 'debugger'
    try:
        level = config['debugger']['level']
    except:
        level = None
    from utils import configs
    try:
        debug_scope = configs.get_scope(config['debugger']['packages'])
    except:
        debug_scope = dict
    # Import debugger and initiate
    from utils import debugger
    debugger.init(path, folder, level, debug_scope)
    # test that debugger can be initiated only once
    debugger.init()
    debugger.init(sys.path[0], folder)


# Function to initiate the compiler
def init_compiler(config):
    '''
    Initiate the compiler based on the provided config
    :param config: dictionary with compiler configs
    :return: None
    '''
    # Try to get configs from the dictionary, except use defaults
    try:
        path = config['compiler']['path']
    except:
        path = sys.path[0]
    if path == None:
        path = sys.path[0]
    try:
        folder = config['compiler']['folder']
    except:
        folder = 'compiler/templates'
    if folder == None:
        path = 'compiler/templates'
    try:
        _modules = config['compiler']['modules']
    except:
        _modules = []
    # list of modules to import [used by jinja2]
    modules = []
    for module in _modules:
        # Append module name, import statement, functions
        modules.append([module,_modules[module]['import'],_modules[module]['functions']])
    # Path to templates  [used by jinja2]
    templates_path = path + '/' + folder
    # Import compiler and initiate
    from compiler import compiler
    compiler.init(templates_path,modules)

def init_restapi(config):
    '''
    Initiate the restapi based on the provided config
    :param config: dictionary with restapi configs
    :return: None
    '''
    # print(config)
    pass
