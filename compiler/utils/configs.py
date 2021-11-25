#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Dimitris Kagialis
# Created Date: 11/10/2021
# version ='1.0'
# Contributors:
# Updated at  : 12/10/2021
# Tested at   : 12/10/2021
# ---------------------------------------------------------------------------
"""Load compiler config file from path"""


# Load config files from path
def load_compiler_config(path: str) -> dict:
    """Loads YAML files from path and creates a dictionary with all YAML objects.
    Requires ruamel.yaml

    :param path: path to the folder

    :return: dictionary with YAML objects"""

    from ruamel.yaml import YAML
    with open(path, "r") as config:
        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.width = 800
        config_yaml = yaml.load(config)
    return config_yaml['compiler']


def load_translator_manifest(path: str) -> dict:
    """Loads YAML files from path and creates a dictionary with all YAML objects.
    Requires ruamel.yaml

    :param path: path to the folder

    :return: dictionary with YAML objects"""

    from ruamel.yaml import YAML
    with open(path, "r") as config:
        yaml = YAML(typ='safe', pure=True)
        yaml.preserve_quotes = True
        yaml.width = 800
        config_yaml = yaml.load(config)
    return config_yaml
