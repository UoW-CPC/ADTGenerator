#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Dimitris Kagialis
# Created Date: 07/10/2021
# version ='1.0'
# Contributors:
# Updated at  : 20/10/2021
# Tested at   : 20/10/2021
# ---------------------------------------------------------------------------
""" Test compiler

    Initiate compiler and render a template"""

import logging
log = logging.getLogger('Test compiler')
log.setLevel(logging.INFO)

log.info('test compiler')

from tests.utils.configs import load
config = load('/Users/dimitriskagialis/development/Westminster/adt-gen-latest/config/config.yaml')

import compiler
compiler.init(config,log)

from tests import test_compiler_dicts

metadata = test_compiler_dicts.mdt

test_run = compiler.compile("MDT.yaml", metadata, log)
# print(test_run)
