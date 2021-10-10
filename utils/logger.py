#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Dimitris Kagialis
# Created Date: 05/10/2021
# version ='1.0'
# ---------------------------------------------------------------------------
""" Logger module
    Configuration parameters:
        path: path to logs folder [Default value project root path]
        folder: logs folder name [Default value 'logs']
        level: logging level - allowed values 'info', 'warning' [default value 'info']
        handler: logging handler - allowed values 'file', 'screen' [default value 'file'] - 'screen' saves also to file.
    Methods:
        init(path, folder, level, handler)
    Usage:
        To initialize the logger:
            from utils import logger
            logger.init(path, folder, level, handler)
        To use the logger:
            from utils.logger import logger
            logger.info('msg')
            logger.warning('msg')
    Implementation:
        Use of the built-in logging package.
        Logger can be initialized only once.
 """

# Packages wide imports
import sys

# Logger global object
logger = None  # Project wide logger - enabled when calling the init

# Logger object locals
_initialized = False  # PRIVATE - Flag to check if logger is initialized


# Function to initiate the logger
def init(path=sys.path[0], folder='logs', level='info', handler='file'):
    '''
    Logger init function:
    Creates a logger based on the below parameters and stores it to a package global logger variable.
    :param path: path to logs folder [Default value project root path]
    :param folder: logs folder name [Default value 'logs']
    :param level: allowed values 'info', 'warning' [default value 'info']
    :param handler: logging handler - allowed values 'file', 'screen' [default value 'file'] - 'screen' saves also to file.
    :return: None
    '''
    # Use package global variables
    global logger
    global _initialized
    # Create the logger if not initialized
    if not _initialized:
        # Evaluate input logging level
        if level == 'info' or level == 'warning':
            # Evaluate input logging handler
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
                _initialized = True
                logger.info(f'Logger has been initiated. [level:{level}, handler:{handler}]')
            else:
                exit(0, 'Unacceptable logging handle. Choose "file" or "screen".')
        else:
            exit(0, 'Unacceptable logging level. Choose "info" or "warning".')
    else:
        logger.warning('Logger can be initiated only once.')