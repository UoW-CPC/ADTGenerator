import logging
from ruamel.yaml import YAML
from io import StringIO


def translate(deployment_format: str = None, topologody_metadata: dict = None, log: logging = None) -> str:
    if deployment_format == 'kubernetes-manifest':
        adt = _translate('kubernetes-manifest', topologody_metadata, log)
        return _build_adt(adt, log)
    elif deployment_format == 'docker-compose':
        adt = _translate('docker-compose', topologody_metadata, log)
        return _build_adt(adt, log)
    else:
        log.warning(f'Topology format is undefined, trying to specify')
        topologody_type = _check_type(topologody_metadata, log)
        if topologody_type == 'kubernetes-manifest':
            adt = _translate('kubernetes-manifest', topologody_metadata, log)
            return _build_adt(adt, log)
        elif topologody_type == 'docker-compose':
            adt = _translate('docker-compose', topologody_metadata, log)
            return _build_adt(adt, log)
        else:
            log.error("Wrong deploymentFormat! Please, specify \"docker-compose\" or \"kubernetes-manifest\"!")
            raise Exception("Wrong deploymentFormat! Please, specify \"docker-compose\" or \"kubernetes-manifest\"!")


def _build_adt(adt_in: dict,  log: logging = None) -> str:
    log.debug('Building the ADT')
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
    log.info('Translation completed successfully')
    return adt


def _check_type(topologody_metadata: dict = None, log: logging = None) -> str:
    log.warning(f'Trying to specify topology format')
    topology_type = None
    artifacts = list(topologody_metadata)
    if 'apiVersion' in artifacts:
        topology_type = "kubernetes-manifest"
    elif 'version' in artifacts:
        topology_type = "docker-compose"
    return topology_type


def _translate(deployment_format: str, topologody_metadata: dict, log: logging = None) -> dict:
    adt = {"node_templates": {}}
    if deployment_format == 'kubernetes-manifest':
        try:
            log.info(f'Translating a kubernetes-manifest')
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
            log.error("Wrong kubernetes-manifest format!")
            raise e
    if deployment_format == 'docker-compose':
        try:
            log.info(f'Translating a docker-compose')
            for service, values in topologody_metadata["services"].items():
                adt['node_templates'][service] = {'type': 'tosca.nodes.MiCADO.Container.Application.Docker.Deployment',
                                                  'properties': values}
            for volume, values in topologody_metadata.get("volumes",dict()).items():
                adt['node_templates'][volume] = {'type': 'tosca.nodes.MiCADO.Container.Volume', 'properties': values}
        except KeyError as e:
            log.error("Wrong docker-compose format!")
            raise e
    return adt
