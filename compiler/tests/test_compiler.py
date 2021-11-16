import unittest
import os
import logging
from io import StringIO
from ruamel.yaml import YAML

from compiler.compiler import compile,init
from compiler.utils.configs import load
from compiler.tests.sample_dicts import *

log = logging.getLogger('testing-compiler')
log.setLevel(logging.DEBUG)

log.debug('compiler unit-testing')

# load sample config
config = load('./configs/compiler-unittest.yml')

class ComplilerTestCase(unittest.TestCase):
    def test_algodt(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        __location__ = os.path.realpath((os.path.join(__location__,'dts')))
        with open(os.path.join(__location__, 'algodt.yaml'), "r") as dt:
            yaml = YAML()
            yaml.preserve_quotes = True
            yaml.width = 800
            template_yaml = yaml.load(dt)
            template_stream = StringIO()
            yaml.dump(template_yaml, template_stream)
            template = template_stream.getvalue()
            template = template[:template.rfind('\n')]
            # print("----")
            # print("YAML FILE")
            # print(template)
            # print("----")
            # print("JINJA TEMPLATE")
            init(config['template_directory'], config['modules'], log)
            # print(compile("AlgoDT.yaml", algodt, log))
            assert compile("AlgoDT.yaml", algodt, log) == template

    def test_idt(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        __location__ = os.path.realpath((os.path.join(__location__, 'dts')))
        with open(os.path.join(__location__, 'idt.yaml'), "r") as dt:
            yaml = YAML()
            yaml.preserve_quotes = True
            yaml.width = 800
            template_yaml = yaml.load(dt)
            template_stream = StringIO()
            yaml.dump(template_yaml, template_stream)
            template = template_stream.getvalue()
            template = template[:template.rfind('\n')]
           #  print("----")
           #  print("YAML FILE")
           # # print(template)
           #  print("----")
           #  #print("JINJA TEMPLATE")
            init(config['template_directory'], config['modules'], log)
            # print(compile("IDT.yaml", idt, log))
            assert compile("IDT.yaml", idt, log) == template

    def test_mdt(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        __location__ = os.path.realpath((os.path.join(__location__, 'dts')))
        with open(os.path.join(__location__, 'mdt.yaml'), "r") as dt:
            yaml = YAML()
            yaml.preserve_quotes = True
            yaml.width = 800
            template_yaml = yaml.load(dt)
            #print(template_yaml)
            template_stream = StringIO()
            yaml.dump(template_yaml, template_stream)
            template = template_stream.getvalue()
            template = template[:template.rfind('\n')]
            # print("----")
            # print("YAML FILE")
            # print(template)
            # print("----")
            # print("JINJA TEMPLATE")
            init(config['template_directory'], config['modules'], log)
            # print(compile("MDT.yaml", mdt, log))
            assert compile("MDT.yaml", mdt, log) == template


if __name__ == '__main__':
    unittest.main()
