import re
from ruamel.yaml import YAML

def handle_env_braces(deploy_data: dict, ms_params: list) -> dict:
    """
    Turn ${} env-style braces into either {{ }} or open_parameter()

    Args:
        deploy_data (dict): Deployment data (Compose or Kubernetes)
        ms_params (list[dict]): Open parameters

    Returns:
        dict: Updated deployment data
    """
    params = [
        param.get("name") 
        for param in ms_params
        if param.get("name")
    ]

    def replacer(match: re.Match) -> str:
        """
        Replace matched string patterns according to open params. To
        be used by recursive_replace().
        """
        variable_name = match.group(1)
        if variable_name in params:
            return f'open_parameter{{{variable_name}}}'
        else:
            return f'{{{{ {variable_name} }}}}'  

    def recursive_replace(item):
        """
        Recursively find and replace ${} in the deployment data.
        """
        if isinstance(item, str):
            return re.sub(r'\$\{(.*?)\}', replacer, item)
        elif isinstance(item, dict):
            return {key: recursive_replace(value) for key, value in item.items()}
        elif isinstance(item, list):
            return [recursive_replace(i) for i in item]
        else:
            return item

    return recursive_replace(deploy_data)


status_file_name = "generate.status"

def write_status_file(filename, status):
  yaml = YAML()
  with open(filename, 'w') as file:
    yaml.dump(status, file)
  return

def read_status_file(filename):
  yaml = YAML()
  with open(filename, 'r') as file:
    status = yaml.load(file)
  return status

