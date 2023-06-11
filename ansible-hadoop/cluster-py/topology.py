from cmd import Cmd


HOME_PATH = '/ansible/ansible-hadoop'
END = []

TOPOLOGY = {
    'zookeeper': {
        'child': [
            'kafka',
            'hadoop',
        ],
        'cmd': Cmd.ALL
    },
    'mysql': {
        'child': [
            'hadoop',
            'airflow',
        ],
        'cmd': Cmd.ALL
    },
    'hadoop': {
        'child': [
            'hive',
            'spark',
            'httpfs',
        ],
        'cmd': Cmd.ALL
    },
    'httpfs': {
        'child': END,
        'cmd': Cmd.ALL
    },
    'hive': {
        'child': [
            'spark',
        ],
        'cmd': Cmd.RUN
    },
    'spark': {
        'child': [
            'zeppelin',
            'tez',
        ],
        'cmd': Cmd.ALL
    },
    'kafka': {
        'child': [
            'kafka-connect',
        ],
        'cmd': Cmd.ALL
    },
    'kafka-connect': {
        'child': END,
        'cmd': Cmd.ALL
    },
    'airflow': {
        'child': END,
        'cmd': Cmd.ALL
    },
    'zeppelin': {
       'child': END,
       'cmd': Cmd.ALL
    },
    'appmaster': {
        'child': END,
        'cmd': Cmd.SETUP
    },
    'tez': {
        'child': END,
        'cmd': Cmd.SETUP
    },
}
