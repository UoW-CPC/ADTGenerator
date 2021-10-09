from utils.logger import logger
from utils import debugger

@debugger.debug
def add(a, b):
    logger.info('add')
    subadd(a,b)
    # try except to gather locals/globals for the debugger [required]
    try:
        debugger.callee_locals.append(locals())
        debugger.callee_globals.append(globals())
    except:
        pass
    return a+b

@debugger.debug
def subadd(a,b):
    logger.info('subadd')
    subsubadd(a,b)
    # try except to gather locals/globals for the debugger [required]
    try:
        debugger.callee_locals.append(locals())
        debugger.callee_globals.append(globals())
    except:
        pass
    return a+b+1

@debugger.debug
def subsubadd(a,b):
    logger.info('subsubadd')
    # try except to gather locals/globals for the debugger [required]
    try:
        debugger.callee_locals.append(locals())
        debugger.callee_globals.append(globals())
    except:
        pass
    return a+b+2
