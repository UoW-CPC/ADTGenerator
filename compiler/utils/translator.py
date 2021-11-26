import logging
from ruamel.yaml import YAML
from io import StringIO


def translate(topologody_metadata: dict = None, log: logging = None) -> str:
    topologody_type = _check_type(topologody_metadata)
    if topologody_type == 'manifest':
        adt_tmp = _translate_manifest(topologody_metadata)
        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.width = 800
        dt_stream = StringIO()
        yaml.dump(adt_tmp, dt_stream)
        adt_str = dt_stream.getvalue()
        adt = ''
        for line in adt_str.splitlines():
            adt = adt + '  ' + line + '\n'
        adt = adt[:adt.rfind('\n')]
        return adt
    elif topologody_type == 'compose':
        adt = translate_compose(topologody_metadata)
        # return json.dumps(adt)


def _check_type(topologody_metadata: dict = None, log: logging = None) -> str:
    topology_type = None
    artifacts = list(topologody_metadata)
    if 'apiVersion' in artifacts:
        topology_type = "manifest"
    elif 'version' in artifacts:
        topology_type = "compose"
    return topology_type


def _translate_manifest(topologody_metadata, log: logging = None):
    _adt = {"node_templates": {} }
    adt = _transform(topologody_metadata, 'manifest', _adt)
    return adt


def translate_compose(topologody_metadata, log: logging = None):
    _adt = {"node_templates": {} }
    adt = _transform(topologody_metadata, 'compose', _adt)
    return adt


def _transform(topologody_metadata: dict, topology_type, adt, log: logging = None):
    if topology_type == 'manifest':
        try:
            name = topologody_metadata["metadata"]["name"].lower()
            kind = topologody_metadata["kind"].lower()
            name_kind = f'{name}-{kind}'
            if kind in ['deployment', 'pod', 'statefulset', 'daemonset']:
                adt['node_templates'][name_kind] = _to_node(topologody_metadata)
        except KeyError:
            print('error')
    return adt


def _to_node(topologody_metadata, log: logging = None):
    topologody_metadata['metadata'].pop('annotations', None)
    topologody_metadata['metadata'].pop('creationTimestamp', None)
    topologody_metadata.pop('status', None)
    return {
        "type": "tosca.nodes.MiCADO.Kubernetes",
        "interfaces": {"Kubernetes": {"create": {"inputs": topologody_metadata}}},
    }
