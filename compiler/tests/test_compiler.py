import unittest
import os
import sys
import logging
from io import StringIO
from ruamel.yaml import YAML

from compiler.compiler import compile, init
from compiler.utils.configs import load_compiler_config
from compiler.tests.sample_dicts import *

log = logging.getLogger('testing-compiler')
log.setLevel(logging.DEBUG)

log.debug('compiler unit-testing')

# load_compiler_config sample config
config = load_compiler_config('./configs/compiler-unittest.yml')


# function to load_compiler_config sample DTs
# noinspection PyShadowingBuiltins
def load_sample_dts(type: str) -> str:
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 800
    yaml.boolean_representation = ['False', 'True']
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    __location__ = os.path.realpath((os.path.join(__location__, 'dts')))
    with open(os.path.join(__location__, type), "r") as dt:
        dt_yaml = yaml.load(dt)
        dt_stream = StringIO()
        yaml.dump(dt_yaml, dt_stream)
        dt_str = dt_stream.getvalue()
        dt_str = dt_str[:dt_str.rfind('\n')]
    return dt_str


# noinspection PyMethodMayBeStatic
class TestCompiler(unittest.TestCase):

    def test_init(self):
        init(log= log)
        from compiler.compiler import _modules, _templates_path
        assert _templates_path == sys.path[0] + '/templates'
        assert _modules == {}

    def test_algodt(self):
        init(config['template_directory'], config['modules'], log)
        sample_dt = load_sample_dts("algodt.yaml")
        assert compile("AlgoDT.yaml", algodt, log) == sample_dt

    def test_ddt(self):
        init(config['template_directory'], config['modules'], log)
        sample_dt = load_sample_dts('ddt.yaml')
        assert compile("dDT.yaml", ddt, log) == sample_dt

    def test_mdt_kube(self):
        init(config['template_directory'], config['modules'], log)
        sample_dt = load_sample_dts('mdt_kube.yaml')
        # print(compile("MDT.yaml", mdt, log))
        assert compile("MDT.yaml", mdt_kube, log) == sample_dt


if __name__ == '__main__':
    unittest.main()
