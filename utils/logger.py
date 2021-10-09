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

# Logger global object
#global logger # project wide logger - always enabled
logger = None # project wide logger - always enabled
# Logger object locals
#global _initialized # PRIVATE - Flag to check if logger is initialized
_initialized = False # PRIVATE - Flag to check if logger is initialized

# Function to initiate the logger
def init(path = sys.path[0],folder = 'logs',level = 'info',handler = 'file'):
    '''

    :param path:
    :param folder:
    :param level:
    :param handler:
    :return:
    '''
    global logger
    global _initialized
    if _initialized == False:
    #if globals()['_initialized'] == False:
    #if '_initialized' not in globals():
        if level == 'info' or level == 'warning':
            if handler == 'file' or handler == 'screen':
                # Create logger file path
                import os
                abs_path = path + '/' + folder
                if not os.path.exists(abs_path):
                    os.makedirs(abs_path)
                filename = 'ADT-generator.log'
                full_path = abs_path + '/' + filename
                # Create the logger
                import logging
                logger = logging.getLogger(__name__)
                # Set logging level
                if level == 'info':
                    logger.setLevel(logging.INFO)
                elif level == 'warning':
                    logger.setLevel(logging.WARNING)
                # Add handlers
                file_handler = logging.FileHandler(full_path)
                format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                file_handler.setFormatter(logging.Formatter(format))
                logger.addHandler(file_handler)
                if handler == 'screen':
                    stream_handler = logging.StreamHandler()
                    stream_handler.setLevel(logging.INFO)
                    stream_handler.setFormatter(logging.Formatter(format))
                    logger.addHandler(stream_handler)
                # Publish the logger
                #globals()['logger'] = logger
                _initialized = True
                #globals()['_initialized'] = True
                #globals()['logger'].info(f'Logger has been initiated. [level:{level}, handler:{handler}]')
                logger.info(f'Logger has been initiated. [level:{level}, handler:{handler}]')
            else:
                exit(0, 'Unacceptable logging handle. Choose "file" or "screen".')
        else:
            exit(0, 'Unacceptable logging level. Choose "info" or "warning".')
    else:
        #globals()['logger'].warning('Logger can be initiated only once.')
        logger.warning('Logger can be initiated only once.')

