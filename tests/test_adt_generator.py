from utils.logger import logger
from utils import debugger

@debugger.debug
def add(a, b):
    logger.info('add')
    subadd(a,b)
    return a+b

@debugger.debug
def subadd(a,b):
    logger.info('subadd')
    subsubadd(a,b)
    return a+b+1

@debugger.debug
def subsubadd(a,b):
    logger.info('subsubadd')
    return a+b+2

