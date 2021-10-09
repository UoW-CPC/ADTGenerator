#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Dimitris Kagialis
# Created Date: 05/10/2021
# version ='1.0'
# ---------------------------------------------------------------------------
""" Debugging tool which offers two levels of information:
    high level: logs the caller and the callee functions
                path: project-root-folder/logs/high_level.log
    low level:  logs the caller and the callee functions, plus the passing and returning arguments.
                path: project-root-folder/logs/low_level.log
    Usage:
    it can be initiated when calling the RestAPI or ...
    Implementation:
    Decorator
 """
# Packages wide imports
import sys

# Debugger global object
debugger = None # project wide debugger - Disabled by default

# Debugger object locals
_initialized = False # PRIVATE - Flag to check if debugger is initialized
_level = None # PRIVATE - Debugging level [high or low] - None by default
global _stack_counter # PRIVATE - Counts the depth of embedded function calls for each stack
global _program_counter # PRIVATE - Counts program flow (adding one for each new stack)

# Debugger logging globals
global caller # list with the sequence of packages where function calls where initiated
global caller_line # list with the sequence of lines where function calls was initiated
global callee_locals # Variables in the local namespace of a function
global callee_globals # Variables in the global namespace of a function

# Function to initiate the debugger
def init(path = sys.path[0],folder = 'debug',level = None):
    '''

    :param path:
    :param folder:
    :param level:
    :return:
    '''
    global debugger
    from utils.logger import logger
    global _initialized
    global _level
    if _initialized == False:
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
            _initialized = True
            globals()['_stack_counter'] = 0
            globals()['_program_counter'] = 0
            globals()['caller'] = []
            globals()['caller_line'] = []
            globals()['callee_locals'] = []
            globals()['callee_globals'] = []
            logger.info(f'Debugger has been initiated. [level:{level}]')
        elif level == None:
            logger.info(f'Debugger is disabled')
        else:
            exit(0, 'Unacceptable debugging level. Choose "high" or "low".')
    else:
        logger.warning(f'Debugger can be initiated only once.')

# Debugger decorator used for debugging
def debug(name, path, line):
    '''

    :param name:
    :param path:
    :param line:
    :return:
    '''

    def wrap_func(func):
        def wrapped_func(*args, **kwargs):
            if _initialized == True:
                globals()['_stack_counter'] += 1
                if globals()['_stack_counter'] == 1:
                    globals()['_program_counter'] += 1
                    debugger.info(f'Stack {globals()["_program_counter"]} begins\n')
            import inspect
            from  utils.logger import logger
            logger.info(inspect.stack()[1])
            logger.info('t')
            logger.info(inspect.stack()[1][0])
            logger.info('t')
            logger.info(inspect.stack()[1][1])
            logger.info('t')
            logger.info(inspect.stack()[1][2])
            logger.info('t')
            logger.info(inspect.stack()[1][3])
            logger.info('t')
            logger.info(inspect.stack()[1][4])
            #print(globals())
            print(globals())
            print(locals())
            ret = func(*args, **kwargs)
            #print(ret)
            if _initialized == True:
                globals()['_stack_counter'] -= 1
                message = f'{name}.{func.__name__} (level:{globals()["_stack_counter"]})\n caller: [{caller[-1]}] line: [{caller_line[-1]}]\n callee: [{path}] func: [{func.__name__}] line: [{line}]\n'
                if _level == "high":
                    debugger.info(message)
                elif _level == "low":
                    debugger.info(f'{message}\nARGs:\n[{args, kwargs}]\n\nReturn:\n[{ret}]\n')
                elif _level == "full":
                    import json
                    print(type(callee_locals[-1]))
                    callee_l = json.dumps(callee_locals[-1],sort_keys = True, indent = 4, default=str)
                    callee_g = json.dumps(callee_globals[-1],sort_keys = True, indent = 4, default=str)
                    debugger.info(f'{message}\nARGs:\n[{args, kwargs}]\n\nReturn:\n[{ret}]\n\nLocals:\n{callee_l}\n\nGlobals:\n{callee_g}\n')
                caller.pop()
                caller_line.pop()
                callee_locals.pop()
                callee_globals.pop()
                if len(caller) == 0:
                    debugger.info(f'Stack {globals()["_program_counter"]} completed\n======================================================================')
            return ret
        return wrapped_func
    return wrap_func