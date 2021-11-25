#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Dimitris Kagialis
# Created Date: 17/11/2021
# version ='1.1'
# Contributors:
# Updated at  : 17/11/2021
# Tested at   : 17/11/2021
# ---------------------------------------------------------------------------
""" Test translator"""

import logging
from configs import load_translator_manifest
from translator import translate

log = logging.getLogger('testing-translator')
log.setLevel(logging.DEBUG)

log.debug('testing translator')

# load_translator_config sample config
manifest = load_translator_manifest('../tests/translator/sample_manifest.yaml')

adt = translate(manifest)
print(adt)