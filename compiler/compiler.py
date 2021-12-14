#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Dimitris Kagialis
# Created Date: 05/10/2021
# version ='1.1'
# Contributors: Jozsef Kovacs
# Updated at  : 16/11/2021
# Tested at   : 16/11/2021
# ---------------------------------------------------------------------------
"""Create DTs (Description Templates) based on YAML files.
    Usage:
        To initiate the compile use the init function
        To render a template use the compile function"""

import logging

_templates_path: str  # PRIVATE - Path to templates
_modules: dict  # PRIVATE - dictionary of modules to import in Jinja2


# Function to initiate the compiler
def init(templates_path: str = None, modules: dict = None, log: logging = None) -> None:
    """Set templates_path, and modules to import in Jinja2.

    :param templates_path: Path to templates
    :param modules: List of modules to import in Jinja2
    :param log: logging

    :return: None"""
    import sys
    global _templates_path, _modules
    if not templates_path:
        templates_path = sys.path[0] + '/templates'
    _templates_path = templates_path
    if not modules:
        modules = dict()
    _modules = modules
    log.debug('Compiler has been initialised.')


# Function to get a DT of specific type based on the provided metadata
# noinspection PyShadowingBuiltins
def compile(type: str, metadata: dict, log: logging) -> str:
    """ Render a Description Template (DT) by using Jinja2.

    :param type: name of the template [available templates 'algodt.yml', idt.yml', 'mdt.yml']
    :param metadata: Dictionary with values to populate in the template.
    :param log: logging

    :return: DT as a string object
    """
    log.info(f'Attempting to render a(n) {type}')
    from jinja2 import Environment, FileSystemLoader, exceptions
    # Load all templates from path
    env = Environment(loader=FileSystemLoader(_templates_path))
    # Try to load input template, if not exists raise
    log.debug(f'Loading template: {type}')
    try:
        dt = env.get_template(type)
    except exceptions.TemplateNotFound as e:
        log.error(f'TemplateNotFound: {type}')
        raise e
    log.debug(f'Template loaded')
    # Try to import input functions to Jinja2
    log.debug(f'Importing modules and functions to jinja2 (if any)')
    for module_name, module_imports in _modules.items():
        try:
            # Execute import statement
            exec(module_imports['import'])
            log.debug(f'module imported: {module_name}')
        except Exception as e:
            log.error(f'Import failed: {e}')
            raise e
        log.debug(f'Loading module [{module_name}] functions to jinja2 (if any)')
        # noinspection PyBroadException
        try:
            for function in module_imports['functions']:
                function_call = f'{module_name}.{function}'
                try:
                    # Evaluate a function and add it to the jinja2 globals
                    function_to_run = eval(function_call)
                    dt.globals[function] = function_to_run
                    log.debug(f'Function loaded: [{function}]')
                except Exception as e:
                    log.error(f'Function cannot be loaded: [{function}], {e}')
        except Exception as e:
            log.warning(f'No functions loaded to jinja2 for module: {module_name}')
            log.warning(e)
    try:
        # Evaluate a function and add it to the jinja2 globals
        dt.globals['log'] = log
        log.debug(f'Logger loaded: [{log}]')
    except Exception as e:
        log.error(f'Logger cannot be loaded: [{log}], {e}')
    try:
        dt = dt.render(metadata)
        log.info('Compilation completed successfully')
        return dt
    except Exception as e:
        log.error(f'Compilation failed: {e}')
        raise e
