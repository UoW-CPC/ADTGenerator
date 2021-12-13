import logging
from ruamel.yaml import YAML
from io import StringIO


def translate(deployment_format: str = None, topologody_metadata: dict = None, log: logging = None) -> str:
    if deployment_format == 'kubernetes':
        adt = _translate('kubernetes', topologody_metadata)
        return _build_adt(adt)
    elif deployment_format == 'docker':
        adt = _translate('docker', topologody_metadata)
        return _build_adt(adt)
    else:
        topologody_type = _check_type(topologody_metadata)
        if topologody_type == 'kubernetes':
            adt = _translate('kubernetes', topologody_metadata)
            return _build_adt(adt)
        elif topologody_type == 'docker':
            adt = _translate('docker', topologody_metadata)
            return _build_adt(adt)
        else:
            raise 'input error'


def _build_adt(adt_in: dict) -> str:
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 800
    dt_stream = StringIO()
    yaml.dump(adt_in, dt_stream)
    adt_str = dt_stream.getvalue()
    adt = ''
    for line in adt_str.splitlines():
        adt = adt + '  ' + line + '\n'
    adt = adt[:adt.rfind('\n')]
    return adt


def _check_type(topologody_metadata: dict = None, log: logging = None) -> str:
    topology_type = None
    artifacts = list(topologody_metadata)
    if 'apiVersion' in artifacts:
        topology_type = "kubernetes"
    elif 'version' in artifacts:
        topology_type = "docker"
    return topology_type


def _translate(deployment_format: str, topologody_metadata: dict, log: logging = None) -> dict:
    adt = {"node_templates": {}}
    if deployment_format == 'kubernetes':
        try:
            name = topologody_metadata["metadata"]["name"].lower()
            kind = topologody_metadata["kind"].lower()
            name_kind = f'{name}-{kind}'
            if kind in ['deployment', 'pod', 'statefulset', 'daemonset']:
                topologody_metadata['metadata'].pop('annotations', None)
                topologody_metadata['metadata'].pop('creationTimestamp', None)
                topologody_metadata.pop('status', None)
                adt['node_templates'][name_kind] = {"type": "tosca.nodes.MiCADO.Kubernetes",
                                                    "interfaces": {"Kubernetes":
                                                                       {"create":
                                                                            {"inputs": topologody_metadata}}}, }
        except KeyError as e:
            raise e
    if deployment_format == 'docker':
        try:
            for service, values in topologody_metadata["services"].items():
                adt['node_templates'][service] = {'type': 'tosca.nodes.MiCADO.Container.Application.Docker.Deployment',
                                                  'properties': values}
            for volume, values in topologody_metadata["volumes"].items():
                adt['node_templates'][volume] = {'type': 'tosca.nodes.MiCADO.Container.Volume', 'properties': values}
        except KeyError as e:
            raise e
    return adt
