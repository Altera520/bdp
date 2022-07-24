import sys, os

HOME_PATH='/ansible/ansible-hadoop'

def print_usage():
    print('illegal arguments')

if __name__ == '__main__':
    # argv filter
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(2)
    
    inventory = 'host' 
    component, operation = tuple(sys.argv[1:])

    # make ansible-playbook command
    # ansible-playbook -i <inventory-file> <playbook-file>
    cmd = ' '.join([
        'ansible-playbook',
        # inventory
        f'-i {HOME_PATH}/inventories/{inventory}.yaml',
        # playbook
        f'{HOME_PATH}/playbooks/{component}/{operation}.yaml',
    ])

    # execute ansible playbook
    print(os.system(cmd))
