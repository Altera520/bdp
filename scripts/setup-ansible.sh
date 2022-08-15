#!/bin/bash

source '/tmp/env.sh'

setup_ansible()
{
    local -r VM_USER=$1
    local -r ANSIBLE_HOME=${2:-/ansible}

    # install ansible
    echo "ANSIBLE_HOME=$ANSIBLE_HOME" >> ~/.bash_profile
    source ~/.bash_profile

    mkdir -p $ANSIBLE_HOME
    cd $ANSIBLE_HOME
    python -m virtualenv venv
    echo "source $(pwd)/venv/bin/activate" > .env
    source venv/bin/activate
    pip install ansible

    # git init
    # git remote add origin https://github.com/Altera520/BDP.git
    # # sparse checkout enable
    # git config core.sparsecheckout true
    # echo 'ansible-hadoop/*' >> .git/info/sparse-checkout
    # git pull origin main
}

#export -f setup_ansible
#su $VM_USER -c "setup_ansible $VM_USER $GIT_BDP_REPO"

setup_ansible root /ansible
