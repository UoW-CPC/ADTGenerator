from utils.logger import logger
from utils import debugger
import inspect

@debugger.debug(__name__, __file__, inspect.currentframe().f_lineno)
def add(a, b):
    logger.info('add')
    try:
        debugger.caller.append(inspect.stack()[2][1])
        debugger.caller_line.append(inspect.stack()[2][2])
    except:
        pass
    subadd(a,b)
    # try except to gather locals/globals for the debugger [required]
    try:
        debugger.callee_locals.append(locals())
        debugger.callee_globals.append(globals())
    except:
        pass
    return a+b

@debugger.debug(__name__, __file__, inspect.currentframe().f_lineno)
def subadd(a,b):
    logger.info('subadd')
    try:
        debugger.caller.append(inspect.stack()[2][1])
        debugger.caller_line.append(inspect.stack()[2][2])
    except:
        pass
    subsubadd(a,b)
    # try except to gather locals/globals for the debugger [required]
    try:
        debugger.callee_locals.append(locals())
        debugger.callee_globals.append(globals())
    except:
        pass
    return a+b+1

@debugger.debug(__name__, __file__, inspect.currentframe().f_lineno)
def subsubadd(a,b):
    logger.info('subsubadd')
    try:
        debugger.caller.append(inspect.stack()[2][1])
        debugger.caller_line.append(inspect.stack()[2][2])
    except:
        pass
    # try except to gather locals/globals for the debugger [required]
    try:
        debugger.callee_locals.append(locals())
        debugger.callee_globals.append(globals())
    except:
        pass
    return a+b+2
