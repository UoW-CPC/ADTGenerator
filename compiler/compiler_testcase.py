#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Dimitris Kagialis
# Created Date: 07/10/2021
# version ='1.1'
# Contributors:
# Updated at  : 16/11/2021
# Tested at   : 16/11/2021
# ---------------------------------------------------------------------------
""" Test compiler

    Initiate compiler and render a template"""

import logging
import compiler
from utils.configs import load
from tests import sample_dicts

log = logging.getLogger('testing-compiler')
log.setLevel(logging.INFO)

log.debug('Testing compiler')

# load sample config
config = load('./tests/configs/compiler.yml')

# noinspection PyUnresolvedReferences
compiler.init(config['template_directory'], config['modules'], log)

metadata = sample_dicts.mdt

# noinspection PyUnresolvedReferences
test_run = compiler.compile("MDT.yaml", metadata, log)
print(test_run)
print(type(test_run))