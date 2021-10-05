# logger_util.py

import logging

global _logging_level
global _caller
global _line
_log_format = "%(asctime)s - [%(levelname)s] - %(message)s"

def logger_func(name, path, line):
    def wrap_func(func):
        def wrapped_func(*args, **kwargs):
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.INFO)
            ret = func(*args, **kwargs)
            if _logging_level == "INFO":
                file_handler = logging.FileHandler("logs/info.log")
                file_handler.setFormatter(logging.Formatter(_log_format))
                logger.addHandler(file_handler)
                logger.info(f'{name}.{func.__name__} \n caller: [{_caller}] line: [{_line}]: \n callee: [{path}] func: [{func.__name__}] line: [{line}]')
            if _logging_level == "DEBUG":
                file_handler = logging.FileHandler("logs/debug.log")
                file_handler.setFormatter(logging.Formatter(_log_format))
                logger.addHandler(file_handler)
                logger.info(f'{name}.{func.__name__} \n caller: [{_caller}] line: [{_line}]: \n callee: [{path}] func: [{func.__name__}] line: [{line}] \n\n ARGs: \n [{args, kwargs}] \n\n Returns: \n [{ret}]')
            return ret
        return wrapped_func
    return wrap_func
