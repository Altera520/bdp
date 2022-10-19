import os, sys
from collections import defaultdict, deque
import copy

HOME_PATH='/ansible/ansible-hadoop'
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
        'httpfs'
    ],
    'httpfs': END,
    'hive': [
        'spark'
    ],
    'spark': END,
    'kafka': [
        'kafka-confluent', 
        'kafka-connect'
    ],
    'kafka-confluent': END,
    'kafka-connect': END,
    'airflow': END,
    'appmaster': END
}
NEED_EXTRA_VARS = [
    'zookeeper',
    'mysql',
]
SETUP_FILTER_LIST = [
    'kafka-connect'
]
EXEC_FILTER_LIST = [
    'appmaster',
    'kafka-confluent',
]


def play(target, act):
    # ansible-playbook -i <inventory-file> <playbook-file>
    ansible_command = f"ansible-playbook -i {HOME_PATH}/inventories/host.yml "
    if target not in NEED_EXTRA_VARS:
        ansible_command += f'{HOME_PATH}/{target}-{act}.yml'
    else:
        ansible_command += f'{HOME_PATH}/{target}.yml --extra-vars \"act={act}\"'
    print(os.system(ansible_command))


def topology_sort(topology):
    indegree = defaultdict(int)
    for parent, childs in topology.items():
        if parent not in indegree:
            indegree[parent] = 0
        for child in childs:
            indegree[child] += 1

    dq = deque([k for k, v in indegree.items() if v == 0])
    seq = deque([])
    while dq:
        parent = dq.popleft()
        seq.append(parent)
        for child in topology[parent]:
            indegree[child] -= 1
            if indegree[child] == 0:
                dq.append(child)
    return seq
    

def topology_play(func, act, topology):
    seq = topology_sort(topology)
    while seq:
        play(func(seq), act)


def filter(topology, filter_list):
    topology = copy.deepcopy(TOPOLOGY)
    for target in filter_list:
        del topology[target]
    return topology
    

def cluster_setup():
    topology_play(lambda seq: seq.popleft(), 'setup', filter(TOPOLOGY, SETUP_FILTER_LIST))


def cluster_start():
    topology_play(lambda seq: seq.popleft(), 'start', filter(TOPOLOGY, EXEC_FILTER_LIST))


def cluster_stop():
    topology_play(lambda seq: seq.pop(), 'stop', filter(TOPOLOGY, EXEC_FILTER_LIST))


def print_usage():
    print('illegal arguments')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(2)

    target = sys.argv[1]
    act = sys.argv[2]
    if target == 'all':
        func = {
            'setup': cluster_setup,
            'start': cluster_start,
            'stop': cluster_stop,
        }[act]()
    else:
        play(target, act)
