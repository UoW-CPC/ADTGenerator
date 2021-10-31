#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Dimitris Kagialis
# Created Date: 05/10/2021
# version ='1.0'
# Contributors:
# Updated at  : 12/10/2021
# Tested at   : 12/10/2021
# ---------------------------------------------------------------------------
"""Compiler module
    Creates DTs (Description Templates) by using Jinja2.
    Usage:
        To initiate the compile:
            from compiler import compiler
            compiler.init(templates_path,modules)
        To render a template:
            from compiler import compiler
            metadata = metadata_dictionary
            template = "MDT.yaml"
            DT = compiler.compile(template, metadata)
    Configuration parameters:
       templates_path: path to YAML templates folder [Default value 'None' sets the path under the compiler]
       modules: List of modules to import in Jinja2 [Default value 'None']
    Functions:
        init - initialize the compiler by setting templates path, and modules
        compile - select a template and provide metadeta to jinja to get a DT
    Implementation:
        Requirement - Jinja2
        Functional programming.
    Tests:
        Unit test wih pytest:
            module: tests.test_compiler.test_compiler.py
                    Test scope: asserts if the output DT is equal with a sample DT in YAML format
                    Test steps:
                                1. initiate the compiler
                                2. render a template with sample data
                                3. assert if output is equal to a sample expected sample DT
                    Requirement: ruamel.aml
 """

# TODO: update unit tests


# import logging
#
# log = logging.getLogger('Compiler')
# # Import the logger
# from utils.logger import logger
# logger.info('Compiler imported')
#
# # Import the debugger
# from utils import debugger

# Compiler global
_templates_path = None # PRIVATE - Path to templates
_modules = [] # PRIVATE - List of modules to import in Jinja2

# Function to initiate the compiler

def init(path=None, imodules=[], log=None):
    '''
    Compiler init function:
    Set globals templates_path, modules based on input arguments.
    :param templates_path: Path to templates
    :param modules: List of modules to import in Jinja2
    :return: None
    '''
    import sys
    if not path:
        path = sys.path[0] + '/templates'
    # list of modules to import [used by jinja2]
    # print(_modules)
    modules = []
    for module in imodules:
        # Append module name, import statement, functions
        modules.append([module,imodules[module]['import'],imodules[module]['functions']])
    # Path to templates  [used by jinja2]

    global _templates_path
    global _modules
    _templates_path = path
    _modules = modules
    log.info('Compiler has been initialised.')

# Function to get a DT of specific type based on the provided metadata
def compile(type, metadata, log):
    '''
    Compiler compile function:
    Get a DT by providing the type of the DT along with required metadata.
    :param type: String with the name of the template [available templates 'algodt.yml', idt.yml', 'mdt.yml']
    :param metadata: Dictionary with values to populate in the template.
    :return: String with the DT
    '''
    log.info(f'Attempting to render a(n) {type}')
    from jinja2 import Environment, FileSystemLoader
    #load the templates
    env = Environment(loader=FileSystemLoader(_templates_path))
    # Try to load the template, if not exists return an error
    log.info(f'Loading template: {type}')
    try:
        dt = env.get_template(type)
    except Exception as e:
        log.error(e.message)
        log.error(f'TemplateNotFound: {type}')
        return f'TemplateNotFound: {type}'
    log.info(f'Template loaded')
    log.info(f'Importing modules and functions (if any)')
    # Each module contains: position [0] module name, [1] import statement, [2] functions
    for module in _modules:
        # Try to import a module, if not exists return an error
        try:
            # execute import statement
            exec(module[1])
            log.info(f'module imported: [{module[0]}]')
        except Exception as e:
            log.error(f'ModuleNotFoundError: {e}')
            return f'ModuleNotFoundError: {e}'
        log.info(f'Loading module [{module[0]}] functions to jinja2 (if any)')
        # Try to load functions for a module, if not exist return an error
        try:
            for function in module[2]:
                function_call = f'{module[0]}.{function}'
                try:
                    # Evaluate a function and add it to the jinja2 globals
                    function_to_run = eval(function_call)
                    dt.globals[function] = function_to_run
                    log.info(f'Function loaded: [{function}]')
                except Exception as e:
                    print(f'Function [{function}] not exist: {e}')
                    log.error(f'Function [{function}] not exist: {e}')
        except:
            log.warning('No functions loaded to jinja2')
    log.info('Trying to compile the DT')
    try:
        dt = dt.render(metadata)
        log.info('Compilation completed successfully')
        return dt
    except Exception as e:
        log.error(f'Compilation failed: {e}')
        return f'Compilation failed: {e}'


