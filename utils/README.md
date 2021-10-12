#Utils
> Tools to support ADT generator components.

##Logger
Configurable global logger based on built-in logging.
Configuration parameters:
- [path] path to logs folder (Default value project root path)
- [folder] logs folder name (Default value 'logs')
- [level] logging level - allowed values 'info', 'warning' (default value 'info')
- [handler] logging handler - allowed values 'file', 'screen' (default value 'file'), 'screen' saves also to file.

##Debugger
Collects information related to program flow and nested calls. Disabled by default.
    Usage:
         To initialize the debugger:
            from utils import debugger
            debugger.init(path, folder, level, debug_scope)
        To use the debugger decorate a function:
            from utils import debugger
            @debugger.debug
            def test():
                pass
    Configuration parameters:
        path: path to debugging logs folder [Default value - project root path]
        folder: debugging logs folder name [Default value 'debugger']
        level: debugging level - allowed values 'None', 'high', 'low', 'full' [default value 'None']
        - None, the debugger is disabled.
        - high, collects the caller module, function and line, and the callee module, function and line.
        - low, collects 'high' + callee input arguments and return.
        - full, collects 'low' + callee function globals.
        debug_scope: dictionary with packages, modules, functions to debug [default value 'empty dict {}' to debug whole program]

##

##