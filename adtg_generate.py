import shutil, os, traceback, json, re
from datetime import datetime
import subprocess 
from micadoparser import set_template, MultiError
import boto3
import jinja2, jinja2schema
from adtg_file import *
from adtg_compile import compile
import adtg_conf
import adtg_utils as utils
from urllib.parse import urlparse
import requests

def init_working_directory(root_wd):
    while(1):
        gen_wd = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
        full_wd = os.path.join(root_wd,gen_wd)
        if not os.path.exists(full_wd):
            break
    os.makedirs(full_wd)
    os.makedirs(os.path.join(full_wd,DIR_IN))
    os.makedirs(os.path.join(full_wd,DIR_OUT))
    f = open(os.path.join(full_wd,FILE_LOG), "a")
    f.write("Log of generating CSAR archive based on Process metadata:\n")
    f.close()
    return gen_wd

def store_input_json_as_file(input_data, full_wd):
    add_log(full_wd, 'Storing incoming json starts...\n')
    filefullpath=os.path.join(full_wd,DIR_IN,'input.json')
    f=open(filefullpath, "w")
    f.write(json.dumps(input_data, indent=4, sort_keys=True)+'\n')
    f.close()
    add_log(full_wd, 'Storing incoming json finised.\n')

def download_asset_from_amr(baseurl, asset_in_msg, asset_in_amr, id, full_wd):
    add_log(full_wd, "  Trying to retrieve \""+asset_in_msg+
                    "\" with id(\""+str(id)+"\") from AMR...\n")
    url = baseurl if baseurl.endswith("/") else f"{baseurl}/"
    url = url + asset_in_amr + "?id=eq." + str(id)
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("ERROR: querying "+asset_in_msg+" from AMR failed! Result of query: "+str(response))
    response_json = response.json()
    if not response_json:
        raise ValueError("ERROR: "+asset_in_msg+" with id ("+str(id)+") not found in AMR. Querying the asset from AMR FAILED!")
    add_log(full_wd, "  Downloading "+asset_in_msg+" from AMR is successful.\n")
    return response_json

def prepare_and_validate_input_assets(input_data, amr_endpoint, full_wd):
    add_log(full_wd, 'Validating incoming json starts...\n')
    #lowercase names of assets
    lc_data = {key.lower():value for key, value in input_data.items()}
    for asset, asset_name in zip(['dma','data'],['process','data']):
        #check the existence of required assets
        if asset not in set(lc_data.keys()):
            raise ValueError("Missing asset \""+asset_name+"\" from input!")
    
    #check the existence of MAPAIR asset
    if "ma" not in set(lc_data.keys()):
        add_log(full_wd, '  Missing asset: Behaviour\n')
        id = lc_data.get("dma",{}).get("ma_pair", 0)
        if not id:
            raise ValueError("ERROR: Behaviour id parameter not found in Process! Constructing the Process from AMR FAILED!")
        asset = \
            download_asset_from_amr(amr_endpoint, "Behaviour", "ma_pair", id, full_wd) 
        lc_data["ma"]=asset[0]

    #check the existence of MODEL asset
    if "model" not in set(lc_data.keys()):
        add_log(full_wd, '  Missing asset: model\n')
        id = lc_data.get("ma",{}) .get("m_asset",0)
        if not id:
            raise ValueError("ERROR: model id parameter not found in Behaviour! Constructing the Process from AMR FAILED!")
        asset = \
            download_asset_from_amr(amr_endpoint, "model", "model", id, full_wd) 
        lc_data["model"]=asset[0]

    #check the existence of ALGORITHM asset
    if "algorithm" not in set(lc_data.keys()):
        add_log(full_wd, '  Missing asset: algorithm\n')
        id = lc_data.get("ma",{}) .get("a_asset",0)
        if not id:
            raise ValueError("ERROR: algorithm id parameter not found in behaviour! Constructing the Process from AMR FAILED!")
        asset = \
            download_asset_from_amr(amr_endpoint, "algorithm", "algorithm", id, full_wd) 
        lc_data["algorithm"]=asset[0]

    #check the existence of MICROSERVICES asset
    if "microservices" not in set(lc_data.keys()):
        add_log(full_wd, '  Missing asset: microservices\n')
        ids = lc_data.get("algorithm",{}).get("list_of_microservices",0)
        if not ids:
            raise ValueError("ERROR: microservice id parameter not found in algorithm! Constructing the Process from AMR FAILED!")
        microservices=list()
        for id in ids:
            asset = \
                download_asset_from_amr(amr_endpoint, "microservice", "microservice", id, full_wd) 
            microservices.append(asset[0])
        lc_data["microservices"]=microservices

    for asset, asset_name in zip(['ma','model','algorithm','microservices'],['behaviour','model','algorithm','microservices']):
        #check the existence of required assets
        if asset not in set(lc_data.keys()):
            raise ValueError("Missing asset \""+asset_name+"\" from input!")
    
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
            #check for obligatory parameters in data
            for param in ["name","kind","direction","type","uri","auth_type"]:
                if param not in new_item:
                    if "name" in new_item:
                        msg = "Data \""+new_item['name']+"\" ("+new_item['id']+") does not contain required field '"+param+"'!"
                    else:
                        msg = "Data \"<noname>\" ("+new_item['id']+") does not contain required field '"+param+"'!"
                    raise ValueError(msg)
        lc_data['data']=new_list
    #check for obligatory parameters in dma
    for param in ["name","version","ip_instance","provider","ma_pair","deployments"]:
        if param not in lc_data["dma"]:
            raise ValueError("Process does not contain required field '"+param+"'!")
    #check for obligatory parameters in ma
    for param in ["name","ip_family","m_asset","a_asset"]:
        if param not in lc_data["ma"]:
            raise ValueError("Behaviour does not contain required field '"+param+"'!")
    #check for obligatory parameters in model
    for param in ["name", "repository_uri", "path", "filename"]:
        if param not in lc_data["model"]:
            if "name" in lc_data["model"]:
                msg = "Model \""+lc_data['model']['name']+"\" ("+lc_data['model']['id']+") does not contain required field '"+param+"'!"
            else:
                msg = "Model \"<noname>\" ("+lc_data['model']['id']+") does not contain required field '"+param+"'!"
            raise ValueError(msg)
    #check for obligatory parameters in algorithm
    for param in ["name","description","classification_schema","type","list_of_microservices"]:
        if param not in lc_data["algorithm"]:
            raise ValueError("Algorithm does not contain required field '"+param+"'!")
    #check for obligatory parameters in microservices
    for ms in lc_data['microservices']:
        for param in ["name","description","classification_schema","type","deployment_format","deployment_data"]:
            if param not in ms:
                if 'name' in ms:
                    raise ValueError("Microservice '"+ms['name']+"' does not contain required field '"+param+"'!")
                else:
                    raise ValueError("Microservice '"+ms['id']+"' does not contain required field '"+param+"'!")

    #convert string to dictionary for microservice deployment_data
    for ms in lc_data['microservices']:
        if isinstance(ms['deployment_data'],str):
            newdd = json.loads(ms['deployment_data'])
            ms['deployment_data']=newdd
        
        ms["deployment_data"] = utils.handle_env_braces(
            ms["deployment_data"], ms.get("parameters", [])
        )
    add_log(full_wd, 'Validating incoming json finished.\n')

    #handling extra "hosts" parameter in Alg asset with backward compatibility
    if "hosts" in lc_data["algorithm"]:
        #add_log(full_wd, 'In Algorithm asset, hosts parameter is found. Converting...\n')
        #add_log(full_wd, 'deployment_data BEFORE:\n'+
        #                  str(lc_data["algorithm"]["deployment_mapping"])+'\n')
        #add_log(full_wd, 'microservice BEFORE:\n'+
        #                  str(lc_data["algorithm"]["list_of_microservices"])+'\n')
        lc_data["algorithm"]["deployment_mapping"]=dict()
        #lc_data["algorithm"]["list_of_microservices"]=list()
        for host in lc_data["algorithm"]["hosts"]:
            #add_log(full_wd, 'Host '+host+' found.\n')
            if "microservices" not in lc_data["algorithm"]["hosts"][host]:
                raise ValueError("Algorithm does not contain the required field 'microservices'! Incorrect input format.")
            for ms in lc_data["algorithm"]["hosts"][host]["microservices"]:
                #add_log(full_wd, '  MS '+ms+' found.\n')
                lc_data["algorithm"]["deployment_mapping"][ms]=host
                #lc_data["algorithm"]["list_of_microservices"].append(ms)
            if "cloud_config" in lc_data["algorithm"]["hosts"][host]:
                cloud_config=lc_data["algorithm"]["hosts"][host]["cloud_config"]
                type=lc_data["dma"]["deployments"][host]["type"]
                lc_data["dma"]["deployments"][host][type]["cloud_config"]=cloud_config
                #add_log(full_wd, '  host: {}\n  cc: {}\n'.format(host,cloud_config))
        #add_log(full_wd, 'deployment_data AFTER:\n'+
        #                  str(lc_data["algorithm"]["deployment_mapping"])+'\n')
        #add_log(full_wd, 'microservice AFTER:\n'+
        #                  str(lc_data["algorithm"]["list_of_microservices"])+'\n')

    return lc_data

def store_input_assets_as_files(input_data, full_wd):
    add_log(full_wd, 'Storing assets in files starts...\n')
    for component, component_name in zip(["dma","ma","model","algorithm"],["process","behaviour","model","algorithm"]):
        add_log(full_wd, "Storing "+component_name+"...\n")
        filefullpath=os.path.join(full_wd,DIR_IN,component+'_'+input_data[component]['id']+'.json')
        f=open(filefullpath, "w")
        f.write(json.dumps(input_data[component], indent=4, sort_keys=True)+'\n')
        f.close()
    for component in ['microservices','data']:
        index = 0
        for item in input_data[component]:
            add_log(full_wd, "Storing "+component+"["+str(index)+"]...\n")
            filefullpath=os.path.join(full_wd,DIR_IN,component+'_'+str(index)+'_'+item['id']+'.json')
            f=open(filefullpath, "w")
            f.write(json.dumps(item, indent=4, sort_keys=True)+'\n')
            f.close()
            index+=1
    add_log(full_wd, 'Storing assets as files finished.\n')
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

def copy_imports(log, full_wd):
    importdir = adtg_conf.CONFIG.get('generator',dict()).get('imports_directory')
    if not importdir:
      add_log(full_wd, "  No \"imports_directory\" defined in config. Skipping copy import files...\n")
      return
    targetdir = os.path.join(full_wd,DIR_OUT)
    files = os.listdir(importdir)
    for fname in files:
        shutil.copy2(os.path.join(importdir,fname), targetdir)
        add_log(full_wd, "  "+fname+"\n")
    return


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
    s3dir = s3config['s3dir']
    if zip_file:
        bucket.upload_file(os.path.join(source_dir,zip_file),os.path.join(s3dir,target_dir,zip_file))
    if log_file:
        bucket.upload_file(os.path.join(source_dir,log_file),os.path.join(s3dir,target_dir,log_file))
    return

def extract_fields_from_uri(url):
    fields = dict()
    o = urlparse(url)
    fields['scheme']=o.scheme
    fields['username']=o.username if o.username else ""
    fields['password']=o.password if o.password else ""
    fields['host']=o.hostname if o.hostname else ""
    fields['port']=str(o.port) if o.port else ""
    fields['path']=o.path
    fields['query']=o.query
    fields['fragment']=o.fragment
    return fields

def collect_data_assets_for_mapping(input_data,msid):
    mappings = input_data.get("dma",dict()).get("data_assets_mapping",dict()).get(msid,None)
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
                #adding extra key-value pairs for fields of uri
                urifields=extract_fields_from_uri(
                        data_content.get("uri",data_content.get("data_uri",data_content.get("repository_uri",""))))
                #add key-values which are not yet defined i.e. skip overwriting
                for k,v in urifields.items():
                    if k not in data_collected[datakey].keys():
                        data_collected[datakey][k]=v
                data_ids.append(dataid)
    return data_collected, data_ids

def prepare_autogenerate_CE(full_wd, insertCE):
    if not insertCE:
        add_log(full_wd, "\n  Auto-insert DigitBrain Condition Evaluator microservice is DISABLED in Process. Skipping...\n")
        return False, ""
    insertCE = adtg_conf.CONFIG.get('generator',dict()).get('condition_evaluator',dict()).get('enable',False)
    if not insertCE:
        add_log(full_wd, "\n  Auto-insert DigitBrain Condition Evaluator microservice is DISABLED in DigitBrain ADT Generator configuration. Skipping...\n")
        return False, ""
    add_log(full_wd, "\n  Auto-insert DigitBrain Condition Evaluator microservice is ENABLED.\n")
    mh_endpoint = adtg_conf.CONFIG.get('generator',dict()).get('condition_evaluator',dict()).get('insert_MH_endpoint',"")
    if mh_endpoint == "":
        add_log(full_wd, "  Message Handler endpoint for CE is not defined in ADTG config. Trying to query...\n")
        query_endpoint = adtg_conf.CONFIG.get('generator',dict()).get('condition_evaluator',dict()).get('query_MH_endpoint_from',"")
        if query_endpoint:
            try: 
                f = requests.get(query_endpoint)
                mh_endpoint = json.loads(f.text)['EMGMH']
            except Exception as e:
                add_log(full_wd, "  Querying Message Handler endpoint failed: \n"+str(e)+"\n")
                add_log(full_wd, "  Unable to auto-generate Condition Evaluator. Skipping...\n")
                return False, ""
        else:
            add_log(full_wd, "  Query URL for Message Handler endpoint is not defined in ADTG config.\n")
            add_log(full_wd, "  Unable to auto-generate Condition Evaluator. Skipping...\n")
            return False, ""
    add_log(full_wd, "  Endpoint of Message Handler for Condition Evaluator: "+mh_endpoint+"\n")
    return True, mh_endpoint

def perform_generate(log, root_wd, gen_wd, input_data):
    response = {
        "success": True,
        "progress": 0,
        "message": "validating inputs",
        "log": None,
        "adt": None
    }
    full_wd = os.path.join(root_wd, gen_wd)
    os.chdir(full_wd)

    try:
        response_file_path = os.path.join(root_wd, gen_wd, utils.response_file_name)
        utils.write_file(response_file_path, response)

        add_log(full_wd, "ADT generation process ID: "+gen_wd+"\n")
        store_input_json_as_file(input_data, full_wd)
        amr_endpoint = adtg_conf.CONFIG.get('generator',dict()).get('asset_metadata_registry',dict()).get("endpoint","")
        input_data = prepare_and_validate_input_assets(input_data, amr_endpoint, full_wd)
        store_input_assets_as_files(input_data,full_wd)

        response["progress"] = 10
        response["message"] = "converting deployments"
        utils.write_file(response_file_path, response)

        out_wd = os.path.join(full_wd, DIR_OUT)
        dma_id = input_data['dma']['id']
        dma_name = input_data['dma']['name']
        add_log(full_wd, "\nGenerating ADT for Process \""+dma_name+"\" ("+dma_id+") starts...\n")

        for dmt_name, dmt_content in input_data['dma']['deployments'].items():
            add_log(full_wd, "\nConverting deployment \""+dmt_name+"\"... ")
            dmt_content['id']=dmt_name
            result = perform_compile(log, full_wd, 'ddt', dmt_content)
            add_log(full_wd, "done.\n")
            dmt_fname = fname('deployment',dmt_name)
            add_log(full_wd, "Saving deployment \""+dmt_name+"\" into file \""+dmt_fname+"\"... ")
            save_to_file(out_wd, dmt_fname, result)
            add_log(full_wd, "done.\n")
        
        response["progress"] = 20
        response["message"] = "converting algorithm"
        utils.write_file(response_file_path, response)

        alg_id = input_data['algorithm']['id']
        alg_name = input_data['algorithm']['name']
        add_log(full_wd, "\nConverting algorithm \""+alg_name+"\" ("+alg_id+")... ")

        #Auto-generate Condition Evaluator microservice
        insertCE, mh_endpoint = prepare_autogenerate_CE(full_wd,
                input_data['dma'].get("insertConditionEvaluator",True))
        input_data['algorithm']['insertConditionEvaluator'] = insertCE
        input_data['algorithm']['endpointMessageHandler'] = mh_endpoint

        result = perform_compile(log, full_wd, 'algodt', input_data['algorithm'])
        add_log(full_wd, "done.\n")
        alg_fname = fname('algorithm', alg_id)
        add_log(full_wd, "Saving algorithm \""+alg_name+"\" into file \""+alg_fname+"\"... ")
        save_to_file(out_wd, alg_fname, result)
        add_log(full_wd, "done.\n")

        progress_ms_id = 0
        progress_ms_number = len(input_data['microservices'])
        for ms in input_data['microservices']: 
            response["progress"] = int(30+(progress_ms_id/progress_ms_number)*20)
            progress_ms_id+=1
            response["message"] = "converting microservice {0}/{1}".format(
                                 str(progress_ms_id),str(progress_ms_number))
            utils.write_file(response_file_path, response)

            ms_id = ms['id']
            ms_name = ms['name']
            add_log(full_wd, "\nConverting microservice \""+ms_name+"\" ("+ms_id+") starts...")
            add_log(full_wd, "\nCollecting data for microservice \""+ms_name+"\"...\n")
            data_content, data_ids = collect_data_assets_for_mapping(input_data, ms_id)
            if data_content:
                add_log(full_wd, "  Found "+str(len(data_ids))+" linked data:\n")
                for dln,dlc in data_content.items():
                    add_log(full_wd, "    \""+dln+"\" will be resolved by \""+dlc['name']+"\" ("+dlc['id']+")\n")
                add_log(full_wd, "Rendering microservice \""+ms_name+"\" with aformentioned data... ")
                ms = perform_substitution(ms, data_content)
                add_log(full_wd, "done.\n")
            else:
                add_log(full_wd, "  No data found.\n")
            model_content = dict()
            model_content['MODEL'] = input_data.get('model',None)
            if model_content:
                model_id = model_content['MODEL']['id']
                model_name = model_content['MODEL']['name']
                #adding extra key-value pairs for fields of uri
                urifields=extract_fields_from_uri(
                        model_content['MODEL'].get("uri",model_content['MODEL'].get("repository_uri","")))
                #add key-values which are not yet defined i.e. skip overwriting
                for k,v in urifields.items():
                    if k not in model_content['MODEL'].keys():
                        model_content['MODEL'][k]=v
                add_log(full_wd, "Rendering microservice \""+ms_name+"\" with model \""+model_name+"\" ("+model_id+")... ")
                ms = perform_substitution(ms, model_content)
                add_log(full_wd, "done.\n")
            add_log(full_wd, "Checking result of rendering DATA and MODEL assets for microservice \""+ms_name+"\"... ")
            undefvars = jinja2schema.infer(json.dumps(ms))
            if undefvars.items():
                add_log(full_wd,"\nList of unresolved variables:\n")
                for k,v in undefvars.items():
                    for kk in list(v.keys()):
                        add_log(full_wd, "  {}.{}\n".format(k,kk))
                msg = "Found unresolved DATA/MODEL asset substitutions for microservice \""+ms_name+"\". See logs for details!"
                raise ValueError(msg)
            add_log(full_wd, "done.\n")
            add_log(full_wd, "Translating microservice \""+ms_name+"\"... ")
            result = perform_compile(log, full_wd, 'mdt', ms)
            add_log(full_wd, "done.\n")
            ms_fname = fname('microservice',ms_id)
            add_log(full_wd, "Saving microservice \""+ms_name+"\" into file \""+ms_fname+"\"... ")
            save_to_file(out_wd, ms_fname, result)
            add_log(full_wd, "done.\n")
            add_log(full_wd, "Converting microservice \""+ms_name+"\" ("+ms_id+") finished.\n")

        response["progress"] = 50
        response["message"] = "creating ADT"
        utils.write_file(response_file_path, response)

        add_log(full_wd, "\nCopying micado type import files starts...\n")
        copy_imports(log, full_wd)
        add_log(full_wd, "done.\n")

        add_log(full_wd, "\nCreating csar zip starts...\n")
        create_csar(log, full_wd, alg_fname)
        add_log(full_wd, "done.\n")

        response["progress"] = 60
        response["message"] = "validating ADT"
        utils.write_file(response_file_path, response)
        
        add_log(full_wd, "\nValidating csar zip (with micadoparser) starts...\n")
        validate_csar(log, full_wd)
        add_log(full_wd, "done.\n")

        response["progress"] = 90
        response["message"] = "uploading ADT to storage"
        utils.write_file(response_file_path, response)

        add_log(full_wd, "\nGenerating ADT for Process \""+dma_name+"\" ("+dma_id+") finished.\n")

        if adtg_conf.CONFIG.get('generator',dict()).get('s3_upload_config',dict()).get("enabled",False):
            s3_upload_config = adtg_conf.CONFIG.get('generator').get('s3_upload_config')
            upload_to_s3(log, s3_upload_config, full_wd, gen_wd, FILE_OUT, FILE_LOG)
    
    except ValueError as e:
        add_log(full_wd,"ERROR: "+str(e)+"\n")
        raise
    except Exception as e:
        add_log(full_wd,'\n'+traceback.format_exc())
        raise

    return True, "ADT generated successfully."

def launch_generate(log, root_wd, gen_wd, input_data):
    response_file_path = os.path.join(root_wd, gen_wd, utils.response_file_name)
    try:
        perform_generate(log, root_wd, gen_wd, input_data)
        log.info('ADT generation finished with SUCCESS. ID:{}'.format(gen_wd))
        response = utils.read_file(response_file_path)
        response["success"] = True
        response["progress"] = 100
        response["message"] = "ADT generated successfully"
    except Exception as e:
        log.info('ADT generation finished with ERROR. ID:{}'.format(gen_wd))
        log.exception(e)
        response = utils.read_file(response_file_path)
        response["success"] = False
        response["message"] = "ADT generation finished with ERROR. See logs for details!"
        if adtg_conf.CONFIG.get('generator',dict()).get('s3_upload_config',dict()).get("enabled",False):
            s3_upload_config = adtg_conf.config.get('generator').get('s3_upload_config')
            full_wd = os.path.join(root_wd, gen_wd)
            upload_to_s3(log, s3_upload_config, full_wd, gen_wd, "", FILE_LOG)
    finally:
        if adtg_conf.CONFIG.get('generator',dict()).get('s3_upload_config',dict()).get("enabled",False):
            s3_upload_config = adtg_conf.config.get('generator').get('s3_upload_config')
            endpoint = s3_upload_config['s3urlprefix']
            rest_path = os.path.join(s3_upload_config['s3dir'],str(gen_wd))
        else:
            endpoint = adtg_conf.CONFIG.get('service',dict()).get('public_endpoint')
            rest_path = "/".join([i.strip("/").lstrip("/") for i in [adtg_conf.CONFIG.get('service',dict()).get('rest_root_path'),"download",str(gen_wd)]])
        log_route = "/".join([i.strip("/").lstrip("/") for i in [endpoint, rest_path, FILE_LOG]])
        adt_route = "/".join([i.strip("/").lstrip("/") for i in [endpoint, rest_path, FILE_OUT]])
        
        response["log"] = log_route
        response["adt"] = adt_route if response["success"] else None
        utils.write_file(response_file_path, response)
        
        return response["success"], response["message"]








