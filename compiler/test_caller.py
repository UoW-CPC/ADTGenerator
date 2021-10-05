#test_caller.py

import compiler
compiler.init('templates',["k8s2adt1","k8s2adt2"],"INFO")

from tests import test_dicts
metadata = test_dicts.mdt
test_run = compiler.compile("MDT.yaml",metadata)

#print(test_run)
