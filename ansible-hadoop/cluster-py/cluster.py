import argparse
import os
import sys
from collections import deque
from typing import *

from topology import HOME_PATH, TOPOLOGY_FOR_EXEC, TOPOLOGY_FOR_SETUP


def ansible_play(target, act):
    cmd = [
        f"ansible-playbook -i {HOME_PATH}/inventories/host.yml",
        f"{HOME_PATH}/{target}-{act}.yml",
    ]
    cmd = " ".join(cmd)
    print(os.system(cmd))


def topology_sort(graph: Dict[str, List[str]]) -> List[str]:
    indegree = dict.fromkeys(graph.keys(), 0)
    seq = []

    for components in graph.values():
        for component in components:
            indegree[component] += 1

    q = deque([k for k, v in indegree.items() if not v])
    while q:
        component = q.popleft()
        seq.append(component)
        for child_component in graph[component]:
            indegree[child_component] -= 1
            if not indegree[child_component]:
                q.append(child_component)
    return seq


def print_plan(topology_list: List[str]) -> None:
    if topology_list:
        base_len = max([len(_) for _ in seq])
    plan = [f"{str(i + 1).rjust(2, ' ')}. {component.ljust(base_len, ' ')}" for i, component in enumerate(topology_list)]
    print("======= ANSIBLE PLAN =======")
    print(" >>\n".join(plan))
    print("============================")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parser')
    parser.add_argument('--target', type=str, required=True)
    parser.add_argument('--act', type=str, required=True)
    args = parser.parse_args()

    act = args.act.lower()
    allow_acts = [
        'setup',
        'start',
        'stop',
        'config',
        'link',
    ]
    assert act in allow_acts

    if args.target == 'all':
        TOPOLOGY = TOPOLOGY_FOR_SETUP if args.act == 'setup' else TOPOLOGY_FOR_EXEC
        topology_list = topology_sort(TOPOLOGY)

        # stop인 경우 topology를 역순으로 변경
        if act == 'stop':
            topology_list.reverse()

        print_plan(topology_list)
        for component in topology_list:
            ansible_play(component, act)
    else:
        ansible_play(target, act)
