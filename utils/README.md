# Utils
> Tools to support ADT generator components.

## Init
Loads ADT generator configs and initiate its components.

Configuration parameters:
- [path] path to config YAML files (Needs to be specified)

## Configs
ADT generator components' config handling.
- load configs from YAML files
- Get a list with nested YAML elements

Requirements:
>ruamel.yaml

## Logger
Configurable global logger based on built-in logging.

Configuration parameters:
- [path] path to logs folder (Default value: project root path)
- [folder] logs folder name (Default value: 'logs')
- [level] logging level - allowed values 'info', 'warning' (Default value: 'info')
- [handler] logging handler - allowed values 'file', 'screen' (Default value: 'file'), 'screen' saves also to file.

## Debugger
Collects information related to program flow and nested calls. Disabled by default.

Debugger is configured at a function level by decorating a function.
```
from utils import debugger
    @debugger.debug
    def test():
        pass
```
Configuration parameters:
- [path] path to debugger logs folder (Default value: project root path)
- [folder] debugger logs folder name (Default value: 'debugger')
- [level] debugging level - allowed values 'None', 'high', 'low', 'full' (Default value: 'None')
-- None, the debugger is disabled.
-- high, collects the caller module, function and line, and the callee module, function and line.
-- low, collects 'high' + callee input arguments and return.
-- full, collects 'low' + callee function globals.
- [debug_scope] dictionary with packages, modules, functions to debug [default value: empty dict which debugs whole program]