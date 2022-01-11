import os, traceback, json
from datetime import datetime
import subprocess 
from micadoparser import set_template, MultiError

import adtg_conf
from compiler import compiler

DIR_IN='inputs'
DIR_OUT='csar'
FILE_LOG='generate.log'
FILE_OUT='dma_adt.csar'

def save_to_file(dir, file, content):
    f = open(os.path.join(dir,file), "a")
    f.write(str(content)+'\n')
    f.close()
    return

def add_log(full_wd, message):
    f = open(os.path.join(full_wd,FILE_LOG), "a")
    f.write(message)
    f.close()
    return

def init_working_directory(log, root_wd):
    while(1):
        gen_wd = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
        full_wd = os.path.join(root_wd,gen_wd)
        if not os.path.exists(full_wd):
            break
    os.makedirs(full_wd)
    os.makedirs(os.path.join(full_wd,DIR_IN))
    os.makedirs(os.path.join(full_wd,DIR_OUT))
    f = open(os.path.join(full_wd,FILE_LOG), "a")
    f.write("Log of generating CSAR archive based on DMA metadata:\n")
    f.close()
    return gen_wd

def check_input_validity(log,input_data):
    log.debug('Checking input validity.')
    #TO BE IMPLEMENTED LATER
    return

def store_input_components_as_files(log,input_data, full_wd):
    log.debug('Storing components as files.')
    for component in ["DMA","MA","MODEL","ALGORITHM"]:
        log.debug(component+'====>'+str(input_data[component]))
        filefullpath=os.path.join(full_wd,DIR_IN,component+'_'+input_data[component]['id']+'.json')
        f=open(filefullpath, "w")
        f.write(json.dumps(input_data[component], indent=4, sort_keys=True)+'\n')
        f.close()
    for component in ['MICROSERVICES','DATA']:
        index = 0
        for item in input_data[component]:
            log.debug(component+'['+str(index)+']====>'+str(item))
            filefullpath=os.path.join(full_wd,DIR_IN,component+'_'+str(index)+'_'+item['id']+'.json')
            f=open(filefullpath, "w")
            f.write(json.dumps(item, indent=4, sort_keys=True)+'\n')
            f.close()
            index+=1
    filefullpath=os.path.join(full_wd,DIR_IN,'GENERATE.json')
    f=open(filefullpath, "w")
    f.write(json.dumps(input_data, indent=4, sort_keys=True)+'\n')
    f.close()
    return

def perform_compile(log, type, input):
    template_file = adtg_conf.CONFIG.get('compiler',dict()).get('templates',dict()).get(type)
    result = compiler.compile(template_file, input, log)
    return result

def fname(type, id):
    return "{0}.{1}.yaml".format(type, id)

def create_csar(log, full_wd, algo_fname):
    puccini_csar_tool = adtg_conf.CONFIG.get('generator',dict()).get('puccini_csar_tool_path')
    if not puccini_csar_tool:
        msg = "Missing parameter \"puccini_csar_tool\" from configuration: no path to csarchiver binary defined!" 
        raise Exception(msg)
    command = "ENTRY_DEFINITIONS={0} {1} {2} {3}".format(algo_fname, puccini_csar_tool, os.path.join(full_wd,FILE_OUT), os.path.join(full_wd,DIR_OUT))
    msg = "Executing csar tool: \"{}\"".format(command)
    log.debug(msg)
    add_log(full_wd, msg+'\n')

    cmd = [puccini_csar_tool,  os.path.join(full_wd,FILE_OUT), os.path.join(full_wd,DIR_OUT)]
    puccini_env = os.environ.copy()
    puccini_env["ENTRY_DEFINITIONS"] = algo_fname
    p = subprocess.Popen(cmd, env=puccini_env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout:
        log.debug(line.rstrip())
        add_log(full_wd, line)

    return

def validate_csar(log, full_wd):
    try:
        set_template(os.path.join(full_wd, FILE_OUT))
        return
    except MultiError as e:
        msg = "ERROR: exception occured during validation, details:"
        log.error(msg)
        log.error(str(e))
        add_log(full_wd, msg+'\n')
        add_log(full_wd, str(e))
    raise Exception("ERROR: Validation of the generated csar FAILED! See logs for details.")
    return

def perform_generate(log, root_wd, gen_wd, input_data):
    log.debug('Generate method has been invoked.')
    root_wd = adtg_conf.CONFIG.get('generator',dict()).get('working_directory')
    log.debug('Generate: root wd: '+root_wd)
    full_wd = os.path.join(root_wd, gen_wd)
    log.debug('Generate: full wd: '+full_wd)

    try:
        check_input_validity(log,input_data)
        store_input_components_as_files(log,input_data,full_wd)
        add_log(full_wd, "ADT generation process ID: "+gen_wd+"\n")

        out_wd = os.path.join(full_wd, DIR_OUT)
        dmaid = input_data['DMA']['id']
        msg = 'DMA tuple ID: '+str(dmaid)+'\n'
        log.info(msg)
        add_log(full_wd, msg)

        for dmt_name, dmt_content in input_data['DMA']['deployments'].items():
            add_log(full_wd, "Converting deployment \""+dmt_name+"\"...")
            dmt_content['id']=dmt_name
            result = perform_compile(log, 'ddt', dmt_content)
            add_log(full_wd, " done.\n")
            dmt_fname = fname('deployment',dmt_name.split('.')[1])
            add_log(full_wd, "Saving deployment \""+dmt_name+"\" into file \""+dmt_fname+"\" ...")
            save_to_file(out_wd, dmt_fname, result)
            add_log(full_wd, " done.\n")

        alg_name = input_data['ALGORITHM']['id']
        add_log(full_wd, "Converting algorithm \""+alg_name+"\"...")
        result = perform_compile(log, 'algodt', input_data['ALGORITHM'])
        add_log(full_wd, " done.\n")
        alg_fname = fname('algorithm', alg_name)
        add_log(full_wd, "Saving algorithm \""+alg_name+"\" into file \""+alg_fname+"\" ...")
        save_to_file(out_wd, alg_fname, result)
        add_log(full_wd, " done.\n")

        for ms in input_data['MICROSERVICES']:
            ms_name = ms['id']
            add_log(full_wd, "Converting microservice \""+ms_name+"\"...")
            result = perform_compile(log, 'mdt', ms)
            add_log(full_wd, " done.\n")
            ms_fname = fname('microservice',ms_name)
            add_log(full_wd, "Saving deployment \""+ms_name+"\" into file \""+ms_fname+"\" ...")
            save_to_file(out_wd, ms_fname, result)
            add_log(full_wd, " done.\n")

        msg = "Creating csar zip starts..."
        log.info(msg)
        add_log(full_wd, msg+'\n')
        log.debug("Working directory: "+full_wd+"\nAlgorithm file: "+alg_fname)
        create_csar(log, full_wd, alg_fname)
        msg = "Creating csar zip finished."
        log.info(msg)
        add_log(full_wd, msg+'\n')

        msg = "Validating csar zip (with micadoparser) starts..."
        log.info(msg)
        add_log(full_wd, msg+'\n')
        log.debug("CSAR file:"+os.path.join(full_wd,FILE_OUT))
        validate_csar(log, full_wd)
        msg = "Validating csar zip finished."
        log.info(msg)
        add_log(full_wd, msg+'\n')

    except Exception as e:
        add_log(full_wd,'\n'+traceback.format_exc())
        raise

    #raise Exception("unexpected error during generation")
    return True, "ADT generated successfully"
