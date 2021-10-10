#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Dimitris Kagialis
# Created Date: 07/10/2021
# version ='1.0'
# ---------------------------------------------------------------------------
""" ADT-generator main
    Usage:
    Initiate program packages with function init.
    List of modules:
        RestAPI
        Compiler
        Logger   - always enabled
        Debugger - disabled by default
    Implementation:
    Functional programming
 """

# Packages wide imports - step 1
import sys # to get root path
from init import init # to initiate ADT-generator

# Initiate ADT-generator modules - step 2
init(sys.path[0])

# Import logger and log first record - step 3
from utils.logger import logger
logger.info('ADT-generator has been started')

from compiler import compiler
from tests import test_compiler_dicts
metadata = test_compiler_dicts.mdt
test_run = compiler.compile("MDT.yaml",metadata)
#print(test_run)
# Import debugger required packages to be able to use the debugger decorator on functions - step 4
from utils import debugger
import inspect

# sample function to present debugger usage
@debugger.debug
def test():
    '''
    testttttt
    :return:
    '''
    # call functions from a test package
    from tests.test_adt_generator import add, subadd
    logger.info('Call package functions from a test function')
    ttt = 1
    ttt = 2
    logger.info(globals())
    logger.info(locals())
    add(1,1)
    subadd(1,1)
    add(1, 1)

if __name__ == "__main__":
    # Main starts - step 4
    logger.info('Main has been started')
    #Testing debugger and logger
    test()
    from tests.test_adt_generator import add,subsubadd
    logger.info('Call package functions from main')
    add(1, 1)
    subsubadd(1, 1)