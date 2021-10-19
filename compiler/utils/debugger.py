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
""" Debugging module
    Collects information related to program flow and nested calls. Disabled by default.
    Usage:
         To initialize the debugger:
            from utils import debugger
            debugger.init(path, folder, level, debug_scope)
        To use the debugger decorate a function:
            from utils import debugger
            @debugger.debug
            def test():
                pass
    Configuration parameters:
        path: path to debugging logs folder [Default value - project root path]
        folder: debugging logs folder name [Default value 'debugger']
        level: debugging level - allowed values 'None', 'high', 'low', 'full' [default value 'None']
        - None, the debugger is disabled.
        - high, collects the caller module, function and line, and the callee module, function and line.
        - low, collects 'high' + callee input arguments and return.
        - full, collects 'low' + callee function globals.
        debug_scope: dictionary with packages, modules, functions to debug [default value 'empty dict {}' to debug whole program]
    Functions:
        init - initialize the debugger.
        _debug_func - [PRIVATE] debugger decorator, wraps the callee function and collects required information.
        debug - callable function of the decorator, enables the debugger to pass arguments in the decorator.
    Implementation:
        Use of the built-in logging package.
        Debugger can be initialized only once.
        Use of a decorator to wrap callee function and collect required information.
    Tests: -
 """
# Module global imports
import sys

# Debugger global object
debugger = None # project wide debugger - Disabled by default, even if calling the init

# Debugger object locals
_initialized = False # PRIVATE - Flag to check if debugger is initialized
_level = None # PRIVATE - Debugging level [accepted values 'high', 'low', 'full'] - None by default
_debug_scope = dict # PRIVATE - Debugging scope to enable debugging for specific packages, modules, functions  [default value -  empty dict, whole project debbugging]
_stack_counter = 0 # PRIVATE - Counts the depth of nested function calls for each stack
_program_counter = 0 # PRIVATE - Counts program flow (adding one for each new stack)


# Function to initiate the debugger
def init(path = sys.path[0],folder = 'degugger',level = None, debug_scope = dict):
    '''
    Debugger init function:
    Creates a debugger based on the below parameters and stores it to a package global debugger variable.
    :param path: path to debugging logs folder [Default value project root path]
    :param folder: debugging logs folder name [Default value 'debug']
    :param level: accepted values 'high', 'low', 'full' [default value 'None']
    :param debug_scope: select packages, modules, functions to debug [default value empty dict to debug the whole project]
    :return: None
    '''
    # Use of package global variables
    global debugger
    global _initialized
    global _level
    global _debug_scope
    # Import the logger to log debugger status
    from compiler.utils.logger import logger
    # Create the debugger if not initialized
    if not _initialized:
        # Evaluate input debugging level
        if level == 'high' or level == 'low' or level == 'full':
            # Create debugger file path
            import os
            abs_path = path + '/' + folder + '/' + level
            if not os.path.exists(abs_path):
                os.makedirs(abs_path)
            from datetime import datetime
            filename = datetime.now().strftime("%d-%m-%Y %H.%M.%S")
            full_path = abs_path + '/' + filename + '.log'
            # Create the debugger
            import logging
            debugger = logging.getLogger(__name__)
            # Set debugging level
            debugger.setLevel(logging.INFO)
            # Add file handler
            file_handler = logging.FileHandler(full_path)
            format = "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s"
            file_handler.setFormatter(logging.Formatter(format))
            debugger.addHandler(file_handler)
            _level = level

            _debug_scope = debug_scope
            _initialized = True
            logger.info(f'Debugger has been initiated. [level:{level}]')
        elif level == None:
            logger.info(f'Debugger is disabled.')
        else:
            exit(0, 'Unacceptable debugging level. Choose "high", "low", "full".')
    else:
        logger.warning(f'Debugger can be initiated only once.')

from functools import wraps
# PRIVATE: Debugger decorator used for debugging
def _debug_func():
    def wrap_func(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            # If debugger is initialized, evaluate and increase the counters
            if _initialized:
                # Use of package global variables
                global _stack_counter
                global _program_counter
                # Add one level in the stack
                _stack_counter += 1
                if _stack_counter == 1:
                    # Initiate a new stack
                    _program_counter += 1
                    debugger.info(f'Stack {_program_counter} begins\n')
            # Wrapped callee function - Runs always
            ret = func(*args, **kwargs)
            # Uncomment to see function return on screen
            #print(ret)
            # If debugger is initialized, collect information - based on debugging level and scope - and add them to the debugging log.
            if _initialized:
                _stack_counter -= 1
                # Set debugging scope
                global _debug_scope
                try:
                    _debug_scope.items()
                    scope = _debug_scope
                except:
                    scope = {'0':''}
                for item_id, item  in scope.items():
                    if item in f'{func.__module__}.{func.__name__}':
                        import inspect
                        message = f'{func.__module__}.{func.__name__} (level:{_stack_counter})\n caller: [{inspect.stack()[1][1]}] [{inspect.stack()[1][3]}] [{inspect.stack()[1][2]}]\n callee: [{inspect.getfile(func)}] [{func.__name__}] [{func.__code__.co_firstlineno}]\n'
                        if _level == "high":
                            debugger.info(message)
                        elif _level == "low":
                            debugger.info(f'{message}\nARGs:\n[{args, kwargs}]\n\nReturn:\n[{ret}]\n')
                        elif _level == "full":
                            import json
                            callee_globals = json.dumps(func.__globals__,sort_keys = True, indent = 4, default=str)
                            debugger.info(f'{message}\nARGs:\n[{args, kwargs}]\n\nReturn:\n[{ret}]\n\nGlobals:\n{callee_globals}\n')
                if _stack_counter == 0:
                    debugger.info(f'Stack {_program_counter} completed\n======================================================================')
            return ret
        return wrapped_func
    return wrap_func

# Call this to decorate a function
debug = _debug_func()