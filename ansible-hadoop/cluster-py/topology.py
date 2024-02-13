HOME_PATH = '/ansible/ansible-hadoop'
END = []

TOPOLOGY_FOR_EXEC = {
    'zookeeper': [
        'kafka',
        'hadoop',
    ],
    'mysql': [
        'hadoop',
        'airflow',
    ],
    'hadoop': [
        'hive',
        'spark',
        'httpfs',
    ],
    'httpfs': END,
    'hive': [
        'spark',
    ],
    'spark': [
        'zeppelin',
    ],
    'kafka': [
        'kafka-connect'
    ],
    'kafka-connect': END,
    'airflow': END,
    'zeppelin': END,
}

TOPOLOGY_FOR_SETUP = {
    'zookeeper': [
        'kafka',
        'hadoop',
    ],
    'mysql': [
        'hadoop',
        'airflow',
    ],
    'hadoop': [
        'hive',
        'spark',
        'httpfs',
    ],
    'httpfs': END,
    'hive': [
        'spark',
    ],
    'spark': [
        'tez',
        'zeppelin',
    ],
    'kafka': [
        'kafka-connect'
    ],
    'kafka-connect': END,
    'airflow': END,
    'tez': END,
    'appmaster': END,
    'zeppelin': END,
}
