# Compiler
>Populate data in YAML template by using Jinja2.


## Usage:

### Initiate the compile
To use the compiler first you must initiate it by passing templates path and the list of functions required by the template.
```
from compiler import compiler
compiler.init(templates_path,modules)
```
parameters:

templates_path: path to YAML templates folder [Default value 'None' sets the path under the compiler folder]

modules: List of modules and their functions to import in Jinja2 [Default value an empty list]

### Render a template:
To render a template pass to the compiler the template name to use and a dictionary with the data required by the template.
```
from compiler import compiler
data = data_dictionary
template = "template"
DT = compiler.compile(template, data)
```

### Requirements
>Jinja2==3.0.1

### Tests and sample data
Unittest are defined under path tests/test_compiler and test data under path tests/test_data.

#### Test
module: test_compiler.py

scope: asserts if the Jinja2 output is equal with a sample YAML file.

test case:
1. initiate the compiler
2. load sample YAML file
2. render a template with sample data
3. assert if output is equal to the sample YAML file
Requirements:
>ruamel.aml