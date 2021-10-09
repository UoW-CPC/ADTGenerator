#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Dimitris Kagialis
# Created Date: 05/10/2021
# version ='1.0'
# ---------------------------------------------------------------------------
""" Logger tool which offers two levels of information:
    Info level: logs the caller and the callee functions
                path: project-root-folder/logs/high_level.log
    Warning level:  logs the caller and the callee functions, plus the passing and returning arguments.
                path: project-root-folder/logs/low_level.log
    File
    Screen
    Usage:
    it can be initiated when calling the RestAPI or ...
    Implementation:
    Decorator
 """
# Packages wide imports
import sys

# Function to initiate the ADT-generator
def init(path):
    '''

    :param path:
    :return:
    '''
    import os
    configs_path = path + '/configs'
    if not os.path.exists(configs_path):
        os.makedirs(configs_path)
    import glob
    from ruamel.yaml import YAML
    configs = dict()
    for file in glob.glob(f'{configs_path}/*.yml'):
        with open(file, "r") as config:
            yaml = YAML()
            yaml.preserve_quotes = True
            yaml.width = 800
            config_yaml = yaml.load(config)
            configs[os.path.basename(file)] = config_yaml
    init_logger(configs.get('logger.yml'))
    init_debugger(configs.get('debugger.yml'))
    init_compiler(configs.get('compiler.yml'))
    init_restapi(configs.get('restAPI.yml'))

# Function to initiate the logger
def init_logger(config):
    '''

    :param config:
    :return:
    '''
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
    from utils import logger
    logger.init(path, folder, level, handler)
    logger.init()

# Function to initiate the debugger
def init_debugger(config):
    '''

    :param config:
    :return:
    '''
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
    from utils import debugger
    debugger.init(path, folder, level)
    debugger.init()
    debugger.init(sys.path[0], folder)

def init_compiler(config):
    '''

    :param config:
    :return:
    '''
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
        import_packages = config['compiler']['import_packages']
    except:
        import_packages = None
    packages = []
    for package in import_packages:
        packages.append([package,import_packages[package]['import_statement'],import_packages[package]['functions']])
    abs_path = path + '/' + folder
    from compiler import compiler
    compiler.init(abs_path,packages)

def init_restapi(config):
    pass
    #print(config)