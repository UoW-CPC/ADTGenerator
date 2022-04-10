import os, traceback, json, re
from datetime import datetime
import subprocess 
from micadoparser import set_template, MultiError
import boto3
import jinja2, jinja2schema
from adtg_file import *
from adtg_compile import compile
import adtg_conf

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

def store_input_json_as_file(log, input_data, full_wd):
    add_log(full_wd, 'Storing incoming json...\n')
    filefullpath=os.path.join(full_wd,DIR_IN,'input.json')
    f=open(filefullpath, "w")
    f.write(json.dumps(input_data, indent=4, sort_keys=True)+'\n')
    f.close()
    add_log(full_wd, 'Done.\n')

def prepare_and_validate_input_assets(log, input_data, full_wd):
    add_log(full_wd, 'Preparing incoming json starts...\n')
    #lowercase names of assets
    lc_data = {key.lower():value for key, value in input_data.items()}
    for asset in ['dma','ma','algorithm','microservices']:
        #check the existence of required assets
        if asset not in set(lc_data.keys()):
            raise ValueError("Missing asset \""+asset+"\" from input!")
    for asset in ['dma','ma','algorithm']:
        #check if the asset is a dictionary
        if not isinstance(lc_data[asset], dict):
            raise ValueError("Asset \""+asset+"\" is not a dictionary!")
    #lowercase parameter names in assets
    for keyd in ['dma','ma','algorithm']:
        if isinstance(lc_data[keyd],dict):
            newcontent = {key.lower():value for key, value in lc_data[keyd].items()}
            lc_data[keyd]=newcontent
    #check for id fields
    for asset in ['dma','ma','algorithm']:
        if 'id' not in lc_data[asset] or not isinstance(lc_data[asset]['id'],str):
            raise ValueError("Asset \""+asset+"\" does not contain the required 'id' field with string value!")
    #check type of microservices
    if not isinstance(lc_data['microservices'], list):
        raise ValueError("Asset \"microservices\" is not a list!")
    #lowercase parameter names in microservices assets
    newlist = []
    for item in lc_data['microservices']:
        if isinstance(item,dict):
            newitem = {key.lower():value for key, value in item.items()}
        else:
            newitem = item
        newlist.append(newitem)
    lc_data['microservices'] = newlist
    #check for id fields under the microservice assets
    index=0
    for asset in lc_data['microservices']:
        if 'id' not in asset or not isinstance(asset['id'], str):
            if 'name' in asset:
                raise ValueError("Microservice asset \""+asset['name']+"\" does not contain the required 'id' field with string value!")
            else:
                raise ValueError("Microservice asset at position "+str(index)+" does not contain the required 'id' field with string value!")
        index+=1
    #lowercase the 'id' key in model
    if 'model' in lc_data and isinstance(lc_data['model'],dict):
        new_model = dict()
        for key, value in lc_data['model'].items():
            if key.lower() == 'id':
                new_model['id'] = value
            else:
                new_model[key] = value
        lc_data['model'] = new_model
    #lowercase the 'id' key in data assets
    if 'data' in lc_data and isinstance(lc_data['data'],list):
        new_list = list()
        for item in lc_data['data']:
            new_item = dict()
            for key, value in item.items():
                if key.lower() == 'id':
                    new_item['id'] = value
                else:
                    new_item[key] = value
            new_list.append(new_item)
        lc_data['data']=new_list
    #convert string to dictionary for microservice deploymentdata
    for ms in lc_data['microservices']:
        if isinstance(ms['deploymentdata'],str):
            newdd = json.loads(ms['deploymentdata'])
            ms['deploymentdata']=newdd
    add_log(full_wd, 'Preparing incoming json finished.\n')
    return lc_data

def store_input_assets_as_files(log,input_data, full_wd):
    log.debug('Storing assets as files starts....')
    add_log(full_wd, 'Storing assets in files starts...\n')
    for component in ["dma","ma","model","algorithm"]:
        add_log(full_wd, "Storing "+component+"...\n")
        #log.debug(component+'====>'+str(input_data[component]))
        filefullpath=os.path.join(full_wd,DIR_IN,component+'_'+input_data[component]['id']+'.json')
        f=open(filefullpath, "w")
        f.write(json.dumps(input_data[component], indent=4, sort_keys=True)+'\n')
        f.close()
    for component in ['microservices','data']:
        index = 0
        for item in input_data[component]:
            #log.debug(component+'['+str(index)+']====>'+str(item))
            add_log(full_wd, "Storing "+component+"["+str(index)+"]...\n")
            filefullpath=os.path.join(full_wd,DIR_IN,component+'_'+str(index)+'_'+item['id']+'.json')
            f=open(filefullpath, "w")
            f.write(json.dumps(item, indent=4, sort_keys=True)+'\n')
            f.close()
            index+=1
    add_log(full_wd, 'Storing components as files finished.\n')
    return

def perform_substitution(template_dict, data_dict):
    patt = re.compile(r'(\{\{[^\{]*\}\})')
    template = json.dumps(template_dict)
    j2_expressions = patt.findall(template)
    for j2_expression in set(j2_expressions):
        try:
            jinja2.Template(j2_expression, undefined=jinja2.StrictUndefined).render(data_dict)
        except jinja2.UndefinedError:
            template = template.replace(j2_expression, f"{{% raw %}}{j2_expression}{{% endraw %}}")
    return json.loads(jinja2.Template(template).render(data_dict))

def perform_compile(log, full_wd, type, input):
    template_file = adtg_conf.CONFIG.get('compiler',dict()).get('templates',dict()).get(type)
    template_dir = adtg_conf.CONFIG.get('compiler',dict()).get('template_directory')
    result = compile(log, full_wd, type, input, os.path.join(template_dir,template_file))
    return result

def fname(type, id):
    return "{0}.{1}.yaml".format(type, id)

def create_csar(log, full_wd, algo_fname):
    puccini_csar_tool = adtg_conf.CONFIG.get('generator',dict()).get('puccini_csar_tool_path')
    if not puccini_csar_tool:
        msg = "Missing parameter \"puccini_csar_tool\" from configuration: no path to csarchiver binary defined!" 
        raise ValueError(msg)
    command = "ENTRY_DEFINITIONS={0} {1} {2} {3}".format(algo_fname, puccini_csar_tool, os.path.join(full_wd,FILE_OUT), os.path.join(full_wd,DIR_OUT))
    msg = "    Executing csar tool: \"{}\"".format(command)

    cmd = [puccini_csar_tool,  os.path.join(full_wd,FILE_OUT), os.path.join(full_wd,DIR_OUT)]
    puccini_env = os.environ.copy()
    puccini_env["ENTRY_DEFINITIONS"] = algo_fname
    p = subprocess.Popen(cmd, env=puccini_env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    add_log(full_wd, "  puccini-csar:\n")
    for line in p.stdout:
        log.debug(line.rstrip())
        add_log(full_wd, "    "+line)

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
    raise ValueError("Validation of the generated csar FAILED! See logs for details.")
    return

def upload_to_s3(log, s3config, source_dir, target_dir, zip_file, log_file):
    session = boto3.Session(
            aws_access_key_id=s3config['s3_aws_access_key'], 
            aws_secret_access_key=s3config['s3_aws_secret_key'])
    s3 = session.resource('s3')
    bucket = s3.Bucket(s3config['s3bucketname'])
    bucket.upload_file(os.path.join(source_dir,zip_file),os.path.join(target_dir,zip_file))
    bucket.upload_file(os.path.join(source_dir,log_file),os.path.join(target_dir,log_file))
    return

def collect_data_assets_for_mapping(input_data,msid):
    mappings = input_data.get("dma",dict()).get("dataassetsmapping",dict()).get(msid,None)
    if not mappings:
        return None, None
    data_collected = {}
    data_ids = []
    for datakey in mappings:
        dataid = mappings.get(datakey,None)
        if dataid:
            data_content = next((item for item in input_data.get('data',list()) if item["id"] == dataid), None)
            if data_content:
                data_collected[datakey]=data_content
                data_ids.append(dataid)
    return data_collected, data_ids

def perform_generate(log, root_wd, gen_wd, input_data):
    log.debug('Generate method has been invoked.')
    root_wd = adtg_conf.CONFIG.get('generator',dict()).get('working_directory')
    full_wd = os.path.join(root_wd, gen_wd)
    log.info('ADT generation starts here: '+full_wd)

    try:
        store_input_json_as_file(log, input_data, full_wd)
        input_data = prepare_and_validate_input_assets(log, input_data, full_wd)
        store_input_assets_as_files(log,input_data,full_wd)
        add_log(full_wd, "ADT generation process ID: "+gen_wd+"\n")

        out_wd = os.path.join(full_wd, DIR_OUT)
        dmaid = input_data['dma']['id']
        msg = 'DMA tuple ID: '+str(dmaid)+'\n'
        log.info(msg)
        add_log(full_wd, msg)

        for dmt_name, dmt_content in input_data['dma']['deployments'].items():
            add_log(full_wd, "Converting deployment \""+dmt_name+"\"... ")
            dmt_content['id']=dmt_name
            result = perform_compile(log, full_wd, 'ddt', dmt_content)
            add_log(full_wd, "done.\n")
            dmt_fname = fname('deployment',dmt_name)
            add_log(full_wd, "Saving deployment \""+dmt_name+"\" into file \""+dmt_fname+"\"... ")
            save_to_file(out_wd, dmt_fname, result)
            add_log(full_wd, "done.\n")

        alg_name = input_data['algorithm']['id']
        add_log(full_wd, "Converting algorithm \""+alg_name+"\"... ")
        result = perform_compile(log, full_wd, 'algodt', input_data['algorithm'])
        add_log(full_wd, "done.\n")
        alg_fname = fname('algorithm', alg_name)
        add_log(full_wd, "Saving algorithm \""+alg_name+"\" into file \""+alg_fname+"\"... ")
        save_to_file(out_wd, alg_fname, result)
        add_log(full_wd, "done.\n")

        for ms in input_data['microservices']:
            ms_id = ms['id']
            add_log(full_wd, "Collecting data for microservice \""+ms_id+"\"... ")
            data_content, data_ids = collect_data_assets_for_mapping(input_data, ms_id)
            if data_content:
                add_log(full_wd, "found: "+str(len(data_ids))+".\n")
                add_log(full_wd, "Rendering microservice \""+ms_id+"\" with data \""+str(data_ids)+"\"... ")
                ms = perform_substitution(ms, data_content) 
                add_log(full_wd, "done.\n")
            else:
                add_log(full_wd, "found: none.\n")
            model_content = dict()
            model_content['MODEL'] = input_data.get('model',None)
            if model_content:
                model_id = model_content['MODEL']['id']
                add_log(full_wd, "Rendering microservice \""+ms_id+"\" with model \""+model_id+"\"... ")
                ms = perform_substitution(ms, model_content)
                add_log(full_wd, "done.\n")
            add_log(full_wd, "Checking result of rendering DATA and MODEL assets for microservice \""+ms_id+"\"... ")
            undefvars = jinja2schema.infer(json.dumps(ms))
            if undefvars.items():
                add_log(full_wd, str(undefvars))
                add_log(full_wd,"\nList of unresolved variables:\n")
                add_log(full_wd,"\n".join("{}.{}".format(k,list(v.keys())[0]) for k,v in undefvars.items()))
                msg = "Found unresolved DATA/MODEL asset substitutions. See logs for details!"
                raise ValueError(msg)
            add_log(full_wd, "done.\n")
            add_log(full_wd, "Converting microservice \""+ms_id+"\"... ")
            result = perform_compile(log, full_wd, 'mdt', ms)
            add_log(full_wd, "done.\n")
            ms_fname = fname('microservice',ms_id)
            add_log(full_wd, "Saving microservice \""+ms_id+"\" into file \""+ms_fname+"\"... ")
            save_to_file(out_wd, ms_fname, result)
            add_log(full_wd, "done.\n")

        msg = "Creating csar zip starts... "
        log.info(msg)
        add_log(full_wd, msg+'\n')
        log.debug("Working directory: "+full_wd+"\nAlgorithm file: "+alg_fname)
        create_csar(log, full_wd, alg_fname)
        msg = "done."
        log.info(msg)
        add_log(full_wd, msg+'\n')

        msg = "Validating csar zip (with micadoparser) starts... "
        log.info(msg)
        add_log(full_wd, msg+'\n')
        log.debug("CSAR file:"+os.path.join(full_wd,FILE_OUT))
        #validate_csar(log, full_wd)
        msg = "done."
        log.info(msg)
        add_log(full_wd, msg+'\n')

        if adtg_conf.CONFIG.get('generator',dict()).get('s3_upload_config',dict()).get("enabled",False):
            s3_upload_config = adtg_conf.CONFIG.get('generator').get('s3_upload_config')
            log.info("s3config:"+str(s3_upload_config))
            log.info("source_dir:"+str(full_wd))
            log.info("target_dir:"+str(gen_wd))
            log.info("zip_file:"+str(FILE_OUT))
            log.info("log_file:"+str(FILE_LOG))
            upload_to_s3(log, s3_upload_config, full_wd, gen_wd, FILE_OUT, FILE_LOG)

    except ValueError as e:
        add_log(full_wd,"ERROR: "+str(e)+"\n")
        raise
    except Exception as e:
        add_log(full_wd,'\n'+traceback.format_exc())
        raise

    return True, "ADT generated successfully"
