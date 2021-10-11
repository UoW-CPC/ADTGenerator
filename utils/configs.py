#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Dimitris Kagialis
# Created Date: 05/10/2021
# version ='1.0'
# ---------------------------------------------------------------------------
""" Configs module
    Supportive function to load ADT-generator components' configuration from YAML files.
    Implementation:
        Use of ruamel.yaml package to load configs.
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
        init(path, folder, level, handler) - initialize the debugger.
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
def load(path):
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
    return configs

def get_scope(config):
    scope = parser(1)
    return scope

_scope = dict()
_scope_counter = 0

def parser(config):
    print(type(config))
    global _scope
    global _scope_counter
    if isinstance(config, dict):
        for key, values in config.items():
            try:
                _scope[str(_scope_counter)] += '.' + key
            except:
                _scope[str(_scope_counter)] = key
            if isinstance(values, dict):
                parser(values)
            else:
               try:
                   first = _scope_counter
                   _scope_counter += 1
                   for value in values:
                       _scope[str(_scope_counter)] = _scope[str(_scope_counter - 1)] + '.' + value
                       _scope_counter += 1
                   _scope.pop(str(first))
               except:
                   pass
        return _scope
    else:
        print(2)
        exit(1)