import os, sys
from typing import *
from collections import deque
from cmd import Cmd
from topology import HOME_PATH, TOPOLOGY



def ansible_play(target, act):
    cmd = f"ansible-playbook -i {HOME_PATH}/inventories/host.yml "
    cmd += f'{HOME_PATH}/{target}-{act}.yml'
    #cmd += f'{HOME_PATH}/{target}.yml --extra-vars \"act={act}\"'
    print(os.system(cmd))


def topology_sort(graph: Dict[str, List[str]],
                  cmd: str,
                  reverse: bool = False,
                  exclude: List[str] = []) -> List[str]:
    indegree = dict.fromkeys(graph.keys(), 0)
    seq = []

    for c in graph.values():
        for _ in c['child']:
            indegree[_] += 1

    q = deque([k for k, v in indegree.items() if not v])
    while q:
        p = q.popleft()
        seq.append(p)
        for c in graph[p]['child']:
            indegree[c] -= 1
            if not indegree[c]:
                q.append(c)
    seq = filter(seq, cmd, graph, exclude)
    if reverse:
        seq.reverse()
    print_seq(seq)
    return seq


def filter(seq: List[str],
           cmd: str,
           graph: Dict[str, List[str]],
           exclude: List[str]) -> List[str]:
    exclude = dict.fromkeys(exclude, 0)
    seq = [component for component in seq if component not in exclude and graph[component]['cmd'] == cmd or graph[component]['cmd'] == Cmd.ALL]
    return seq


def print_seq(seq: List[str]) -> None:
    if seq:
        base_len = max([len(_) for _ in seq])
    plan = [f"{str(i + 1).rjust(2, ' ')}. {component.ljust(base_len, ' ')}" for i, component in enumerate(seq)]
    print("======= ANSIBLE PLAN =======")
    print(" >>\n".join(plan))
    print("============================")


def act_to_cmd(act: str) -> str:
    cmd = ('run' if act == 'start' or act == 'stop' else act).upper()
    return cmd


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('illegal arguments')
        sys.exit(2)

    target = sys.argv[1]
    act = sys.argv[2]
    cmd = act_to_cmd()

    if target == 'all':
        for component in topology_sort(TOPOLOGY, cmd, act == 'stop'):
            ansible_play(component, act)
    else:
        ansible_play(target, act)