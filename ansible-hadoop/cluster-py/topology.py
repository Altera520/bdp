#!/usr/bin/env python

HOME_PATH = '/ansible/ansible-hadoop'
END = []

TOPOLOGY = {
    'zookeeper': [
        'kafka', 
        'hadoop'
    ],
    'mysql': [
        'hadoop', 
        'airflow'
    ],
    # hadoop-setup -> tez-setup, spark-setup -> hive-setup
    'hadoop': [
        'hive', 
        'spark', 
        'httpfs',
        'zeppelin',
    ],
    'httpfs': END,
    'hive': [
        'spark'
    ],
    'spark': [
        'zeppelin',
    ],
    'kafka': [
        'kafka-connect',
    ],
    'kafka-connect': END,
    'airflow': END,
    'zeppelin': END,
    'appmaster': END
}

NEED_EXTRA_VARS = [
    'zookeeper',
    'mysql',
]

SETUP_FILTER_LIST = [
    
]

EXEC_FILTER_LIST = [
    'appmaster',
]