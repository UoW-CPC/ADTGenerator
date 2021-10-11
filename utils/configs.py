#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Dimitris Kagialis
# Created Date: 11/10/2021
# version ='1.0'
# ---------------------------------------------------------------------------
""" Configs module
    Supportive functions to load ADT-generator components' configuration from YAML files
    and get configs trees from nested YAML elements.
    Implementation:
        Use of ruamel.yaml package to load configs.
        Use of recursion to parse a tree of YAML elements and create a unique records for each branch.
    Functions:
        load - loads all YAML files from the specified path.
        get_scope - takes a dictionary with nested dictionaries and returns a dictionaries with all paths to branches.
        parser - parses a dictionary  with nested dictionaries an create a dictionaries with all paths to branches.
 """
# Load ADT generator config files from path
def load(path):
    '''
    Loads YAML files from path and creates a dictionary with all YAML objects.
    Requires ruamel.yaml
    :param path: path to the folder
    :return: dictionary with YAML objects
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
    return configs

# Get tree's branches from a config
def get_scope(config):
    '''
    Receives a dictionary and returns a new dictionary with all paths to branches.
    :param config: dictionary
    :return: dictionary
    '''
    scope = _parser(config)
    return scope

# parser function globals
_scope = dict() # PRIVATE - dictionary with all branches
_key = 0 # PRIVATE - key of the dictionary (implemented as a counter)

# Create paths to branches for a config
def _parser(config):
    '''
    Receives a dictionary and returns a new dictionary with all paths to branches.
    Hidden function implemented with a recursion.
    :param config: dictionary
    :return: dictionary
    '''
    global _scope
    global _key
    if isinstance(config, dict):
        for key, values in config.items():
            try:
                _scope[str(_key)] += '.' + key
            except:
                _scope[str(_key)] = key
            if isinstance(values, dict):
                _parser(values)
            else:
               try:
                   parent_key = _key
                   _key += 1
                   for value in values:
                       _scope[str(_key)] = _scope[str(parent_key)] + '.' + value
                       _key += 1
                   _scope.pop(str(parent_key))
               except:
                   pass
        return _scope