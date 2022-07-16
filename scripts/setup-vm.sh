#!/bin/bash

source /vagrant/scrupts/env.sh

function add_user {
    USER=$1
    PASSWD=$2

    useradd -m -s /bin/bash -U $USER
    cp -pr /home/vagrant/.ssh "/home/$USER/"
    chown -R "$USER:$USER" "/home/$USER"
    echo $PASSWD | passwd --stdin $USER
    echo "%$USER ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/$USER"
}

function make_hosts
{
    SPEC_FILE=$1
    NODES=(`cat "/tmp/$SPEC_FILE" | grep -e name -e ip | tr ':' '\n' | grep -v name | grep -v ip`)
    i=-1
    for node in "${NODES[@]}"
    do
        i=$((i+1))
        if ! ((i % 2)); then
            continue
        fi
        echo "${NODES[$i]} ${NODES[$(($i - 1))]}" >> /etc/hosts
    done
    rm "/tmp/$SPEC_FILE"
}


# =======================================================================

# step1. update package & install
sudo dnf -y update
sudo dnf -y install epel-release wget net-tools lsof vim

# step2. add user
add_user $VM_USER $VM_PASSWORD

# step3. edit /etc/hosts
SPEC_FILE=$1
make_hosts $SPEC_FILE

localectl set-locale LANG=en_US.UTF-8