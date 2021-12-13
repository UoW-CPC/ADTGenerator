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
from configs import load_topology_from_file
from translator import translate

log = logging.getLogger('testing-translator')
log.setLevel(logging.DEBUG)

log.debug('testing translator')

# load_translator_config sample config
topology = load_topology_from_file('../tests/translator/sample_manifest.yaml')
adt = translate('manifest',topology)
print(adt)