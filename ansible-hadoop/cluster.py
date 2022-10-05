import sys, os
from collections import defaultdict, deque

HOME_PATH='/ansible/ansible-hadoop'

COMPONENT = {
    'airflow': True,
    'python': False,
    'mysql': True,
    'hadoop': True,
    'superset': True,
    'hive': True,
    'scala': False,
    'java': False,
    'kafka': True,
    'zookeeper': True,
    'spark': True,
    'tez': False
}

STACK = {
    'airflow': ['python', 'mysql'],
    'hadoop': ['java', 'zookeeper'],
    'mysql': [],
    'superset': ['python', 'mysql'],
    'hive': ['hadoop', 'mysql', 'zookeeper', 'tez'],
    'kafka': ['java', 'zookeeper'],
    'zookeeper': ['java'],
    'spark': ['scala', 'hive', 'hadoop'],
    'hue': ['hive', 'hadoop']
}

def gen_topology_indegree():
    indegree = defaultdict(int)
    for stack, childs in STACK.items():
        if indegree[stack] == 0:
            indegree[stack] = 0
        for child in childs:
            indegree[child] += 1
    return indegree


def ansible_command(act, target):
    return f'ansible-playbook -i {HOME_PATH}/inventories/host.yml {HOME_PATH}/{target}-{act}.yml'


def setup_cluster(indegree):
    q = deque()
    for target, v in indegree.items():
        if v == 0:
            q.append(target)
    while q:
        target = q.popleft()
        if COMPONENT[target]:
            print(os.system(ansible_command('setup', target)))
        for child in STACK[target]:
            indegree[child] -= 1
            if indegree[child] == 0:
                q.append(child)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('need one argument: setup | start | stop')
        sys.exit(2)
    

    print(os.system(build_ansible_command()))
    

    gen_topology_indegree
    pass