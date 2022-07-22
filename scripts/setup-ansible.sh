#!/bin/bash

source '/tmp/env.sh'

function setup_ansible
{
    local -r VM_USER=$1

    # install ansible
    mkdir -p "/home/$VM_USER/ansible"
    cd "/home/$VM_USER/ansible"
    python -m virtualenv venv
    echo "source $(pwd)/venv/bin/activate" > .env
    echo -e 'Y' | cd $(pwd)
    pip install ansible
}

setup_ansible $VM_USER