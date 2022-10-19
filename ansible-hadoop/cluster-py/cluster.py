import os, sys
from collections import defaultdict, deque
import copy
from topology import HOME_PATH, NEED_EXTRA_VARS, TOPOLOGY, SETUP_FILTER_LIST, EXEC_FILTER_LIST

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


def print_usage():
    print('illegal arguments')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(2)

    target = sys.argv[1]
    act = sys.argv[2]

    func = {
        'setup': lambda _: topology_play(lambda seq: seq.popleft(), 'setup', filter(TOPOLOGY, SETUP_FILTER_LIST)),
        'start': lambda _: topology_play(lambda seq: seq.popleft(), 'start', filter(TOPOLOGY, EXEC_FILTER_LIST)),
        'stop': lambda _: topology_play(lambda seq: seq.pop(), 'stop', filter(TOPOLOGY, EXEC_FILTER_LIST)),
    }
    
    if target == 'all':
        func[act]()
    else:
        play(target, act)
