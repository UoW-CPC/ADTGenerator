from adtg_file import *
from dockubeadt.translator import translate_dict
import jinja2
import ruamel.yaml
from pathlib import Path
import json
import contextlib
import sys, io 
import re
from io import StringIO

def raise_helper(msg):
    raise Exception(msg)

def save_compile_stdout(log, full_wd, stdout, stderr):
    if full_wd=="":
        log.info("\nDocKubeADT:\n"+stdout+"\n"+stderr)
    else:
        add_log(full_wd, "\n  DocKubeADT:\n")
        lines=(stdout+"\n"+stderr).strip().splitlines()
        for l in lines:
            add_log(full_wd, "    "+l+"\n")

def rendering_open_parameters(data):
    if isinstance(data, dict):
        return {k: rendering_open_parameters(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [rendering_open_parameters(i) for i in data]
    elif isinstance(data, str):
        # Match the value of the key/value pair
        match = re.match(r'^open_parameter\{"?(.*?)"?\}$', data)
        if match:
            return {'get_input': match.group(1).strip()}
        
        # Match within the string
        matches = re.findall(r'open_parameter\{"?(.*?)"?\}', data)
        for match in matches:
            param_value = match.strip().strip('\"').strip('\'')
            replace_value = f'{{ get_input: {param_value} }}'
            data = data.replace(f'open_parameter{{{match}}}', replace_value)
        return data
    return data

def compile(log, full_wd, asset_type, asset_dict, template_file):
    if asset_type == "mdt":

        with contextlib.redirect_stdout(StringIO()) as o, contextlib.redirect_stderr(StringIO()) as e:
            try:
                df = asset_dict.get('deployment_format') 
                if df == "docker-compose" and type(asset_dict.get('deployment_data')) == list:
                    dd = asset_dict.get('deployment_data')[0]
                else:
                    dd = asset_dict.get('deployment_data')
                cd = asset_dict.get('configuration_data',dict())
                dockubeadt_result = translate_dict( df, dd, cd)
                save_compile_stdout(log, full_wd, o.getvalue(), e.getvalue())
            except Exception:
                save_compile_stdout(log, full_wd, o.getvalue(), e.getvalue())
                raise
        
        yaml = ruamel.yaml.YAML()
        yaml.preserve_quotes = True
        #workaround due to the fact that dockubeadt returns node_templates as yaml instead of dict
        dockubeadt_result = yaml.load(str(dockubeadt_result))
        #workaround finishes here
        ms_dict = rendering_open_parameters(dockubeadt_result)
        buf = io.BytesIO()
        yaml.dump(ms_dict,buf)
        ms_yaml = str(buf.getvalue().decode("utf-8"))
        ms_yaml_with_2spaces = ""
        for line in ms_yaml.split('\n'):
            ms_yaml_with_2spaces +="  "+line+"\n"
        asset_dict['adt_from_dockubeadt']=ms_yaml_with_2spaces

    template = Path(template_file).read_text()
    asset_dict['raise'] = raise_helper
    return jinja2.Template(template).render(asset_dict)


