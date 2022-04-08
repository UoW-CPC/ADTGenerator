from adtg_file import *
from dockubeadt.translator import translate_dict
import jinja2
import yaml
from pathlib import Path
import json
import contextlib
import sys 
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

def compile(log, full_wd, asset_type, asset_dict, template_file):
    if asset_type == "mdt":
        with contextlib.redirect_stdout(StringIO()) as o, contextlib.redirect_stderr(StringIO()) as e:
            try:
                dockubeadt_result = translate_dict(
                    asset_dict.get('deploymentformat'),
                    asset_dict.get('deploymentdata'),
                    asset_dict.get('configurationdata',dict()))
                save_compile_stdout(log, full_wd, o.getvalue(), e.getvalue())
            except Exception:
                save_compile_stdout(log, full_wd, o.getvalue(), e.getvalue())
                raise
        
        asset_dict['adt_from_dockubeadt']=dockubeadt_result

    template = Path(template_file).read_text()
    asset_dict['raise'] = raise_helper
    return jinja2.Template(template).render(asset_dict)


