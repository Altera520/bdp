import sys, os

HOME_PATH='/ansible/ansible-hadoop'

def print_usage():
    print('illegal arguments')


if __name__ == '__main__':
    # argv filter
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(2)
    
    # inventories/host.yaml
    inventory = 'host'
    
    target = sys.argv[1]
    extra_var = None if len(sys.argv) == 2 else sys.argv[2]

    # make ansible-playbook command
    # ansible-playbook -i <inventory-file> <playbook-file>
    def build_ansible_command():
        command = [
            'ansible-playbook',
            # inventory
            f'-i {HOME_PATH}/inventories/{inventory}.yml',
            # playbook
            f'{HOME_PATH}/{target}.yml',
        ]
        if extra_var:
            command.append(f'--extra-vars \"act={extra_var}\"')
        command = ' '.join(command)
        print(command)
        return command

    # execute ansible playbook
    print(os.system(build_ansible_command()))
