import yaml
with open('config_test.yaml', 'r') as f:
    CONF = yaml.safe_load(f)

LOG_FORMAT = '%(asctime)s %(levelname)s: %(filename)s %(funcName)s:%(lineno)d : %(message)s'
