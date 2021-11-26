# algodt_old = {'description':
#               {'id': 'algorithm_10824912410291',
#                'name': 'Object Detection Algorithm for detection of faulty weld seams',
#                'description': 'This algorithm can be used to solve a specifc problem, and applies some fancy technologies.',
#                'classificationSchema': 'ML',
#                'type':
#                    ['neural network',
#                     'deep learning'
#                     ],
#                'author': 'DFKI',
#                'date': '06/04/2021',
#                'version': '1.0'
#                },
#             'algorithm':
#                 {'listOfMicroservices':
#                      ['microserviceA',
#                       'microserviceB',
#                       'microserviceC'],
#                   'abstractHostDefinition':
#                       [{'microserviceA': 'host1'},
#                        {'microserviceB': 'host2'},
#                        {'microserviceC': 'host3'}
#                        ]
#                  }
#           }
#
# idt_old = {'description':
#               {'id': 'algorithm_10824912410291',
#                'name': 'Object Detection Algorithm for detection of faulty weld seams',
#                'description': 'This algorithm can be used to solve a specifc problem, and applies some fancy technologies.',
#                'classificationSchema': 'ML',
#                'type':
#                    ['neural network',
#                     'deep learning'
#                     ],
#                'author': 'DFKI',
#                'date': '06/04/2021',
#                'version': '1.0'
#                }
#        }
#
#
# mdt_old = {'description':
#             {'id': 'microservice_12312124',
#              'name': 'Object Detection for faulty parts',
#              'author': 'DFKI',
#              'date': '06/04/2021',
#              'version': '1.0',
#              'description': 'This microservices solves a certain problem using very specific methods. It supports some special input types, and allows results to be presented in chosen format.',
#              'classificationSchema': 'other',
#              'type':
#                  ['neural network',
#                   'deep learning'
#                   ],
#              'software':
#                ['Apache Kafka',
#                 'TensorFlow'
#                 ],
#              'softwareVersion':
#                  ['Kafka 2.7.0',
#                   'TensorFlow 2.4.1'
#              ]},
# 'service':
#         {'containerFormat': 'Docker',
#          'image': 'dockerhub://dfki/object_detection/stuff',
#          'deploymentFormat': 'docker run',
#          'deploymentData': 'docker run image-name -p 8080:8080',
#          'dependencyRequirements': 'MicroserviceAsset_ID_123',
#          'storageRequirements': 'needs to share volume with MicroserviceAsset_ID_123',
#          'limitations': 'can only work with jpg files'},
# 'containerConfiguration':
#         {'name': 'stuff_detection',
#          'command': '["sudo ./start.sh"]',
#          'args': '["-h", "test_argument"]',
#          'labels': '["label1", "label2"]',
#          'env': '["env1", "env2"]',
#          'optional1': '["optional1"]',
#          'opitonal2': '["optional1"]'},
# 'hardwareRequirements':
#            {'recommendedNumberOfGPUCores': 2,
#             'minimumNumberOfGPUCores': 1,
#             'recommendedGPURAM': 6,
#             'minimumGPURAM': 1,
#             'gpuType': 'NVidia (compute capability >= 7.0)',
#             'hpcRequired': '"True"',
#             'hpcType': 'hpcType',
#             'edgeType': 'NVIDIA Jetson AGX',
#             'recommendedRAM': 16,
#             'minimumRAM': 2,
#             'recommendedCPUs': 4,
#             'minimumCPUs': 2,
#             'requiredDiskSpace': 42},
# 'OSRequirements':
#            {'osArch': 'x86_64',
#             'osType': 'linux',
#             'osDistribution': 'ubuntu',
#             'osVersion': '20.04'},
# 'inputData':
#            {'inputData':
#                 {'DATA_KIND': 'FILE, STREAM',
#                  'DATA_DIRECTION': 'SOURCE'},
#             'dataObjects':
#                 {'DATA_KIND':
#                      ['FILE',
#                       'STREAM'
#                       ],
#                  'DATA_DIRECTION':
#                      ['SINK',
#                       'BIDIRECTIONAL'
#                       ],
#                  'DATA_FORMAT':
#                      ['application/zip',
#                       'image/jpg'
#                       ],
#                  'DATA_SOURCE_TYPE':
#                      ['MYSQL', 'KAFKA'
#                       ],
#                  'DATA_PROTOCOL':
#                      ['HTTP',
#                       'HTTPS'
#                       ],
#                  'DATA_AUTH_TYPE':
#                      ['tls_mutual',
#                       'userpass'
#                       ],
#                  'DATA_MYSQL_DIALECT':
#                      ['mariadbdialect',
#                       'sampledialect'
#                       ],
#                  'DATA_MQTT_PROTOCOL_VERSION':
#                      ['2.3.1',
#                       '2.3.2'],
#                  'DATA_KAFKA_BROKER_VERSION':
#                      ['2.7.1',
#                       '2.5'
#                       ],
#                  'DATA_S3_REGION':
#                      ['eu-central-1',
#                       'eu-central-2'],
#                  'DATA_SCHEMA':
#                      ['jpg',
#                       'png'
#                       ]}},
# 'outputData':
#         {'outputData':
#              {'DATA_KIND': 'FILE, STREAM',
#               'DATA_DIRECTION': 'SINK'},
#          'dataObjects':
#              {'DATA_KIND':
#                   ['FILE',
#                    'STREAM'
#                    ],
#               'DATA_DIRECTION':
#                   ['SINK',
#                    'BIDIRECTIONAL'
#                    ],
#               'DATA_FORMAT':
#                   ['application/zip',
#                    'image/jpg'
#                    ],
#               'DATA_SOURCE_TYPE':
#                   ['MYSQL',
#                    'KAFKA'
#                    ],
#               'DATA_PROTOCOL':
#                   ['HTTP',
#                    'HTTPS'
#                    ],
#               'DATA_AUTH_TYPE':
#                   ['tls_mutual',
#                    'userpass'],
#               'DATA_MYSQL_DIALECT':
#                   ['mariadbdialect',
#                    'sampledialect'
#                    ],
#               'DATA_MQTT_PROTOCOL_VERSION':
#                   ['2.3.1',
#                    '2.3.2'
#                    ],
#               'DATA_KAFKA_BROKER_VERSION':
#                   ['2.7.1',
#                    '2.5'
#                    ],
#               'DATA_S3_REGION':
#                   ['eu-central-1',
#                    'eu-central-2'],
#               'DATA_SCHEMA':
#                   ['jpg',
#                    'png'
#                    ]}},
#          'model':
#              {'modelTypes':
#                   ['SavedModel1 (Tensorflo1)',
#                    'SavedModel2 (Tensorflo2)'],
#              'modelRecommendedAuthTools':
#                   ['SavedModel1 (Tensorflo3)',
#                    'SavedModel2 (Tensorflo4)']}}
#
#
# mdt_temp = {'description':
#             {'id': 'microservice_12312124',
#              'name': 'Object Detection for faulty parts',
#              'author': 'DFKI',
#              'date': '06/04/2021',
#              'version': '1.0',
#              'description': 'This microservices solves a certain problem using very specific methods. It supports some special input types, and allows results to be presented in chosen format.',
#              'classificationSchema': 'other',
#              'type':
#                  ['neural network',
#                   'deep learning'
#                   ],
#              'software':
#                ['Apache Kafka',
#                 'TensorFlow'
#                 ],
#              'softwareVersion':
#                  ['Kafka 2.7.0',
#                   'TensorFlow 2.4.1'
#              ]},
# 'service':
#         {'containerFormat': 'Docker',
#          'image': 'dockerhub://dfki/object_detection/stuff',
#          'deploymentFormat': 'docker run',
#          'deploymentData': 'docker run image-name -p 8080:8080',
#          'dependencyRequirements': 'MicroserviceAsset_ID_123',
#          'storageRequirements': 'needs to share volume with MicroserviceAsset_ID_123',
#          'limitations': 'can only work with jpg files'},
# 'containerConfiguration':
#         {'name': 'stuff_detection',
#          'command': '["sudo ./start.sh"]',
#          'args': '["-h", "test_argument"]',
#          'labels': '["label1", "label2"]',
#          'env': '["env1", "env2"]',
#          'optional1': '["optional1"]',
#          'opitonal2': '["optional1"]'},
# 'hardwareRequirements':
#            {'recommendedNumberOfGPUCores': 2,
#             'minimumNumberOfGPUCores': 1,
#             'recommendedGPURAM': 6,
#             'minimumGPURAM': 1,
#             'gpuType': 'NVidia (compute capability >= 7.0)',
#             'hpcRequired': '"True"',
#             'hpcType': 'hpcType',
#             'edgeType': 'NVIDIA Jetson AGX',
#             'recommendedRAM': 16,
#             'minimumRAM': 2,
#             'recommendedCPUs': 4,
#             'minimumCPUs': 2,
#             'requiredDiskSpace': 42},
# 'OSRequirements':
#            {'osArch': 'x86_64',
#             'osType': 'linux',
#             'osDistribution': 'ubuntu',
#             'osVersion': '20.04'},
# 'inputData':
#            {'inputData':
#                 {'DATA_KIND': 'FILE, STREAM',
#                  'DATA_DIRECTION': 'SOURCE'},
#             'dataObjects':
#                 {'DATA_KIND':
#                      ['FILE',
#                       'STREAM'
#                       ],
#                  'DATA_DIRECTION':
#                      ['SINK',
#                       'BIDIRECTIONAL'
#                       ],
#                  'DATA_FORMAT':
#                      ['application/zip',
#                       'image/jpg'
#                       ],
#                  'DATA_SOURCE_TYPE':
#                      ['MYSQL', 'KAFKA'
#                       ],
#                  'DATA_PROTOCOL':
#                      ['HTTP',
#                       'HTTPS'
#                       ],
#                  'DATA_AUTH_TYPE':
#                      ['tls_mutual',
#                       'userpass'
#                       ],
#                  'DATA_MYSQL_DIALECT':
#                      ['mariadbdialect',
#                       'sampledialect'
#                       ],
#                  'DATA_MQTT_PROTOCOL_VERSION':
#                      ['2.3.1',
#                       '2.3.2'],
#                  'DATA_KAFKA_BROKER_VERSION':
#                      ['2.7.1',
#                       '2.5'
#                       ],
#                  'DATA_S3_REGION':
#                      ['eu-central-1',
#                       'eu-central-2'],
#                  'DATA_SCHEMA':
#                      ['jpg',
#                       'png'
#                       ]}},
# 'outputData':
#         {'outputData':
#              {'DATA_KIND': 'FILE, STREAM',
#               'DATA_DIRECTION': 'SINK'},
#          'dataObjects':
#              {'DATA_KIND':
#                   ['FILE',
#                    'STREAM'
#                    ],
#               'DATA_DIRECTION':
#                   ['SINK',
#                    'BIDIRECTIONAL'
#                    ],
#               'DATA_FORMAT':
#                   ['application/zip',
#                    'image/jpg'
#                    ],
#               'DATA_SOURCE_TYPE':
#                   ['MYSQL',
#                    'KAFKA'
#                    ],
#               'DATA_PROTOCOL':
#                   ['HTTP',
#                    'HTTPS'
#                    ],
#               'DATA_AUTH_TYPE':
#                   ['tls_mutual',
#                    'userpass'],
#               'DATA_MYSQL_DIALECT':
#                   ['mariadbdialect',
#                    'sampledialect'
#                    ],
#               'DATA_MQTT_PROTOCOL_VERSION':
#                   ['2.3.1',
#                    '2.3.2'
#                    ],
#               'DATA_KAFKA_BROKER_VERSION':
#                   ['2.7.1',
#                    '2.5'
#                    ],
#               'DATA_S3_REGION':
#                   ['eu-central-1',
#                    'eu-central-2'],
#               'DATA_SCHEMA':
#                   ['jpg',
#                    'png'
#                    ]}},
#          'model':
#              {'modelTypes':
#                   ['SavedModel1 (Tensorflo1)',
#                    'SavedModel2 (Tensorflo2)'],
#              'modelRecommendedAuthTools':
#                   ['SavedModel1 (Tensorflo3)',
#                    'SavedModel2 (Tensorflo4)']},
# 'manifest': {'apiVersion': 'v1', 'kind': 'Pod', 'metadata': {'name': 'busybox-sleep'}, 'spec': {'containers': [{'name': 'busybox', 'image': 'busybox', 'args': ['sleep', '1000000']}]}}
#            }


algodt = {
'id': 'algorithm_10824912410291',
'name': 'Object Detection Algorithm for detection of faulty weld seams',
'description': 'This algorithm can be used to solve a specifc problem, and applies some fancy technologies.',
'classificationSchema': 'ML',
'type':
   ['neural network','deep learning'],
'author': 'DFKI',
'date': '06/04/2021',
'version': '1.0',
'algorithm':
    {
        'listOfMicroservices':
         ['microserviceA','microserviceB','microserviceC'],
        'abstractHostDefinition':
              {
               'microserviceA': 'microserviceA',
               'microserviceB': 'microserviceA',
               'microserviceC': 'microserviceC'
               }

     }
}

ddt = {
'id': 'deployment_10824912410291',
'name': 'Object Detection Algorithm for detection of faulty weld seams',
'author': 'DFKI',
'created_at': '06/04/2021',
'version': '1.0',
'licensor': 'Licensor 1',
'scope': 'This algorithm can be used to solve a specifc problem, and applies some fancy technologies.',
'deployment':
    {
        'host_name': 'host1',
        'deployment_id': 'depl1',
        'instance_type_id': 'ins1',
        'key_pair_id': 'key1',
        'opened_port': 8080,
        'endpoint': 'end1'
    }
}


mdt = {
'id': 'microservice_12312124',
'name': 'Object Detection for faulty parts',
'author': 'DFKI',
'date': '06/04/2021',
'version': '1.0',
'description': 'This microservices solves a certain problem using very specific methods. It supports some special input types, and allows results to be presented in chosen format.',
'classificationSchema': 'other',
'type':
    ['neural network','deep learning'],
'software':
    ['Apache Kafka','TensorFlow'],
'softwareVersion':
    ['Kafka 2.7.0','TensorFlow 2.4.1'],
'containerFormat': 'Docker',
'image': 'dockerhub://dfki/object_detection/stuff',
'deploymentFormat': 'docker run',
'deploymentData':
    {
        'apiVersion': 'v1', 'kind': 'Pod',
        'metadata':
            {'name': 'busybox-sleep'},
        'spec':
            {'containers':
                 [
                     {'name': 'busybox', 'image': 'busybox', 'args': ['sleep', '1000000']}
                 ]
            }
    },
'dependencyRequirements': 'MicroserviceAsset_ID_123',
'storageRequirements': 'needs to share volume with MicroserviceAsset_ID_123',
'limitations': 'can only work with jpg files',
'recommendedNumberOfGPUCores': 2,
'minimumNumberOfGPUCores': 1,
'recommendedGPURAM': 6,
'minimumGPURAM': 1,
'gpuType': 'NVidia (compute capability >= 7.0)',
'hpcRequired': '"True"',
'hpcType': 'hpcType',
'edgeType': 'NVIDIA Jetson AGX',
'recommendedRAM': 16,
'minimumRAM': 2,
'recommendedCPUs': 4,
'minimumCPUs': 2,
'requiredDiskSpace': 42,
'osArch': 'x86_64',
'osType': 'linux',
'osDistribution': 'ubuntu',
'osVersion': '20.04',
'inputData':
    [
        {
            'INPUT_ID': 'SAMPLE_ID',
            'DATA_KIND':
                 ['FILE','STREAM'],
             'DATA_DIRECTION':
                 ['SINK','BIDIRECTIONAL'],
             'DATA_FORMAT':
                 ['application/zip','image/jpg'],
             'DATA_SOURCE_TYPE':
                 ['MYSQL', 'KAFKA'],
             'DATA_PROTOCOL':
                 ['HTTP','HTTPS'],
             'DATA_AUTH_TYPE':
                 ['tls_mutual','userpass'],
             'DATA_MYSQL_DIALECT':
                 ['mariadbdialect','sampledialect'],
             'DATA_MQTT_PROTOCOL_VERSION':
                 ['2.3.1','2.3.2'],
             'DATA_KAFKA_BROKER_VERSION':
                 ['2.7.1','2.5'],
             'DATA_S3_REGION':
                 ['eu-central-1','eu-central-2'],
             'DATA_SCHEMA':
                 ['jpg','png' ]
        }
    ],
'outputData':
    [
        {
            'OUTPUT_ID': 'SAMPLEO_ID',
             'DATA_KIND':
                ['FILE','STREAM'],
            'DATA_DIRECTION':
                ['SINK','BIDIRECTIONAL'],
            'DATA_FORMAT':
                ['application/zip','image/jpg'],
            'DATA_SOURCE_TYPE':
                 ['MYSQL','KAFKA'],
            'DATA_PROTOCOL':
                ['HTTP','HTTPS'],
            'DATA_AUTH_TYPE':
                 ['tls_mutual','userpass'],
            'DATA_MYSQL_DIALECT':
                ['mariadbdialect','sampledialect'],
            'DATA_MQTT_PROTOCOL_VERSION':
                ['2.3.1','2.3.2'],
            'DATA_KAFKA_BROKER_VERSION':
                ['2.7.1','2.5'],
            'DATA_S3_REGION':
                ['eu-central-1','eu-central-2'],
            'DATA_SCHEMA':
                ['jpg','png']
        }
    ],
'modelTypes':
     ['SavedModel1 (Tensorflo1)','SavedModel2 (Tensorflo2)'],
'modelRecommendedAuthTools':
    ['SavedModel1 (Tensorflo3)','SavedModel2 (Tensorflo4)'],
'parameters':
    [
        {
            'name':'n1', 'type':'int','mandatory': True,
            'defaultValue':'45','description':'sample n1'
         },
        {
            'name':'n2', 'type':'bool','mandatory': False,
            'defaultValue':'45','description':'sample n2'
        }
    ],
'metric': []
}

