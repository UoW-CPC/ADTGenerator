import unittest
import os
from compiler import compile,init
from io import StringIO
from ruamel.yaml import YAML
from .test_dicts import *

class ComplilerTestCase(unittest.TestCase):
    def test_algodt(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, 'test_algodt.yaml'), "r") as dt:
            yaml = YAML()
            yaml.preserve_quotes = True
            yaml.width = 800
            template_yaml = yaml.load(dt)
            template_stream = StringIO()
            yaml.dump(template_yaml, template_stream)
            template = template_stream.getvalue()
            template = template[:template.rfind('\n')]
            print("----")
            print("YAML FILE")
            print(template)
            print("----")
            print("JINJA TEMPLATE")
            init('templates', ["k8s2adt1", "k8s2adt2"], True)
            print(compile("AlgoDT.yaml", algodt))
            assert compile("AlgoDT.yaml", algodt) == template

    def test_idt(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, 'test_idt.yaml'), "r") as dt:
            yaml = YAML()
            yaml.preserve_quotes = True
            yaml.width = 800
            template_yaml = yaml.load(dt)
            template_stream = StringIO()
            yaml.dump(template_yaml, template_stream)
            template = template_stream.getvalue()
            template = template[:template.rfind('\n')]
            print("----")
            print("YAML FILE")
           # print(template)
            print("----")
            #print("JINJA TEMPLATE")
            init('templates', ["k8s2adt1", "k8s2adt2"], True)
            print(compile("IDT.yaml", idt))
            assert compile("IDT.yaml", idt) == template

    def test_mdt(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, 'test_mdt.yaml'), "r") as dt:
            yaml = YAML()
            yaml.preserve_quotes = True
            yaml.width = 800
            template_yaml = yaml.load(dt)
            #print(template_yaml)
            template_stream = StringIO()
            yaml.dump(template_yaml, template_stream)
            template = template_stream.getvalue()
            template = template[:template.rfind('\n')]
            print("----")
            print("YAML FILE")
            print(template)
            print("----")
            print("JINJA TEMPLATE")
            init('templates', ["k8s2adt1", "k8s2adt2"], True)
            print(compile("MDT.yaml", mdt))
            assert compile("MDT.yaml", mdt) == template


if __name__ == '__main__':
    unittest.main()
