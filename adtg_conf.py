import yaml, json, logging,logging.config, argparse
log = None
CONFIG = None
service_host = None
service_port = None
rest_root_path = None
secrets_json_path = None


def init():
     global CONFIG, log, service_host, service_port, rest_root_path, secrets_json_path
     parser = argparse.ArgumentParser(description='DigitBrain ADT Generator: This service is used for compiling DigitBrain assets towards MiCADO ADT')


     parser.add_argument('--config', dest = 'config_path', default = './config/config.yaml' ,
                         help='Specifies the path to the configuration file')

     parser.add_argument('--host', dest='service_host', type = str, 
                         help = 'Specifies the host to connect service to')

     parser.add_argument('--port', dest = 'service_port', type = int,
                         help='Specifies the port number where the service should listen')

     parser.add_argument('--secrets', dest = 'secrets_json_path', type = str,
                         help='Specifies the list of secrets in a json file')


     args = parser.parse_args()

     try:
          with open(args.config_path,'r') as conf_var:
               CONFIG = yaml.safe_load(conf_var)
     except Exception as e:
          print('Cannot read configuration file:', args.config_path)
          print(e)

     try:
          logging.config.dictConfig(CONFIG['logging'])
          log = logging.getLogger('adtg')
     except Exception as e:
          log.info('Unable to initialize the dictionary')

     log.info('ADT generator started.')
     log.info('Using config file: '+args.config_path)

     service_host = CONFIG.get('service',dict()).get('host','127.0.0.1')
     service_host = args.service_host if args.service_host else service_host

     service_port = CONFIG.get('service',dict()).get('port',4000)
     service_port = args.service_port if args.service_port else service_port

     rest_root_path = CONFIG.get('service',dict()).get('rest_root_path','/v1/adtg')

     secrets_json_path = CONFIG.get('service',dict()).get('secrets_json_path', None)
     secrets_json_path = args.secrets_json_path if args.secrets_json_path else secrets_json_path

     if CONFIG.get('generator',dict()).get('s3_upload_config',dict()).get("enabled",False):
        s3_upload_config = CONFIG.get('generator').get('s3_upload_config')
        for key in ['s3bucketname','s3urlprefix','s3_keys_json_path']:
            if s3_upload_config.get(key,None) is None:
                raise Exception("Missing key in ADT Generator configuration: "+key)
        with open(s3_upload_config['s3_keys_json_path']) as json_file:
            data = json.load(json_file)
            if data.get('s3_aws_access_key',None) is None:
                raise Exception("Missing key in s3_keys_json_path of ADT Generator configuration: s3_aws_access_key")
            if data.get('s3_aws_secret_key',None) is None:
                raise Exception("Missing key in s3_keys_json_path of ADT Generator configuration: s3_aws_secret_key")
            CONFIG['generator']['s3_upload_config']['s3_aws_access_key']=data['s3_aws_access_key']
            CONFIG['generator']['s3_upload_config']['s3_aws_secret_key']=data['s3_aws_secret_key']

