#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Dimitris Kagialis
# Created Date: 07/10/2021
# version ='1.0'
# Contributors:
# Updated at  : 12/10/2021
# Tested at   : 12/10/2021
# ---------------------------------------------------------------------------
""" ADT-generator main module
    Initiate program components by calling an init function.
    Usage:
        Start the program from that modules.
    List of components:
        RestAPI
        Compiler
        Logger - always enabled
        Debugger - disabled by default
    Functions: -
    Implementation:
        Functional programming
    Tests: -

 """

# Module global imports - step 1
import sys # to get root path
from utils.init import init # to initiate ADT-generator

# Initiate ADT-generator components - step 2
# Question: how to pass the path? eg. ENV variable

# WARNING: init must run before importing any components
init(sys.path[0])

# Import logger and log first record - step 3
from utils.logger import logger
logger.info('ADT-generator has been started')


# Import debugger to decorator module functions - step 4
from utils import debugger


if __name__ == "__main__":
    # Main starts - step 4
    logger.info('Main has been started')

    #TESTS

    # Compiler
    from compiler import compiler
    from tests.test_compiler import test_compiler_dicts
    metadata = test_compiler_dicts.mdt
    test_run = compiler.compile("MDT.yaml", metadata)
    print(test_run)
    #print(type(test_run))

    #  Debugging
    # sample function to present debugger usage
    @debugger.debug
    def test():
        '''
        test docstring
        :return:
        '''
        # call functions from a get_scope package
        from tests.test_adt_generator import add, subadd
        logger.info('Call package functions from a get_scope function')
        ttt = 1
        ttt = 2
        add(1, 1)
        subadd(1, 1)
        add(1, 1)
        return 'test debugging from test'

    #Test debugger and logger
    # test()
    # from tests.test_adt_generator import add,subsubadd
    # logger.info('Call package functions from main')
    # add(1, 1)
    # subsubadd(1, 1)