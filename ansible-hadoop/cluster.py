import os
from collections import defaultdict, deque

HOME_PATH='/ansible/ansible-hadoop'
END = []
TOPOLOGY = {
    'zookeeper': ['hadoop'],
    'mysql': ['hadoop'],
    # hadoop-setup -> tez-setup, spark-setup -> hive-setup
    'hadoop': END,
    'airflow': END,
}


def play(target, act='setup', use_extra_vars=False):
    ansible_command = None
    if not use_extra_vars:
        ansible_command = f'ansible-playbook -i {HOME_PATH}/inventories/host.yml {HOME_PATH}/{target}-{act}.yml'
    else:
        ansible_command = f'ansible-playbook -i {HOME_PATH}/inventories/host.yml {HOME_PATH}/{target}.yml --extra-vars \"act={act}\"'
    print(os.system(ansible_command))


if __name__ == '__main__':
    # init hadoop cluster
    indegree = defaultdict(int)
    for parent, childs in TOPOLOGY.items():
        if parent not in indegree:
            indegree[parent] = 0
        for child in childs:
            indegree[child] += 1

    q = deque([k for k, v in indegree.items() if v == 0])
    while q:
        parent = q.popleft()
        play(parent)
        for child in TOPOLOGY[parent]:
            indegree[child] -= 1
            if indegree[child] == 0:
                q.append(child)
