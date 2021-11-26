# Compiler
>Populate data into YAML template by using Jinja2.

## Usage
### Initiate the compiler
To use the compiler first you must initiate it by passing its configuration
 - templates path
 - python modules required by the template

```
from compiler import compiler
compiler.init(templates_path, modules)
```
Configuration parameters
- [templates_path] path to YAML templates folder (Default value: None, sets the path under the compiler folder)
- [modules] list of modules with their import statements and functions to pass in Jinja2 (Default value: empty list)

### Render a template
To render a template pass to the compiler the template name and a dictionary with the data required by the template.
```
from compiler import compiler
data = data_dictionary
template = "template"
DT = compiler.compile(template, data)
```
Compile function returns a String object.

### Requirements
>Jinja2==3.0.1

### Tests and sample input - output
Unittests are defined in module tests/test_compiler.py
Sample input data in module tests/sample_dicts.py
Sample output in YAML format in directory tests/dts

#### Test Case
module: test_compiler.py

scope: asserts if  compile function output is equal with a sample YAML file.

steps:
1. initiate the compiler
2. load sample YAML file
2. render a template with sample data
3. assert if output is equal to the sample YAML file

Requirements:
>ruamel.aml