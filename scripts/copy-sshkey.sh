#!/bin/bash

source '/tmp/env.sh'

copy_sshkey()
{
    local -r VM_USER=$1
    local -r VM_PASSWORD=$2

    # ssh key create and then copy other VM
    local -r KEY="$HOME/.ssh/id_rsa"
    if [ ! -f "${KEY}.pub" ]; then
        echo -e 'y' | ssh-keygen -t rsa -f $KEY -q -N ""    
    fi
    NODES=( $(cat /tmp/node-specs.yml | grep name | awk '{print $3}') )
    #NODES=( $(cat /tmp/node-specs.yaml | grep name | awk '{print $3}' | grep -v $HOSTNAME) )
    for NODE in "${NODES[@]}"
    do
        sshpass -p "$VM_PASSWORD" ssh-copy-id -i "${KEY}.pub" "${VM_USER}@${NODE}" -o stricthostkeychecking=no
    done
}

#export -f copy_sshkey
#su $VM_USER -c "copy_sshkey $VM_USER $VM_PASSWORD"
copy_sshkey root $VM_PASSWORD
