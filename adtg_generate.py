import adtg_conf
import os, json
from datetime import datetime
from compiler import compiler

DIR_IN='inputs'
DIR_OUT='csar'
FILE_LOG='generate.log'
FILE_OUT='dma_csar.zip'

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
    f = open(os.path.join(full_wd,FILE_OUT), "a")
    f.write("Here comes the final CSAR archive content:\n")
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

def perform_generate(log, root_wd, gen_wd, input_data):
    log.debug('Generate method has been invoked.')
    root_wd = adtg_conf.CONFIG.get('service',dict()).get('working_directory',os.getcwd())
    log.debug('Generate: root wd: '+root_wd)
    full_wd = os.path.join(root_wd, gen_wd)
    log.debug('Generate: full wd: '+full_wd)

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

    #raise Exception("unexpected error during generation")
    return True, "ADT generated successfully"
