#!/bin/bash

source '/tmp/env.sh'

function add_user 
{
    local -r USER=$1
    local -r PASSWD=$2
    useradd -m -s /bin/bash -U $USER
    cp -pr /home/vagrant/.ssh "/home/$USER/"
    chown -R "$USER:$USER" "/home/$USER"
    echo $PASSWD | passwd --stdin $USER
    echo "%$USER ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/$USER"
}

function regist_host
{
    local -r NODES=( $(cat /tmp/node-specs.yaml | grep -E 'name|ip'  | tr ':' '\n' | grep -vE 'name|ip') )
    local -r LENGTH=${#NODES[@]}

    for (( i=0; i<${LENGTH}; i+=2 ));
    do
        echo "${NODES[$i]} ${NODES[$(($i+1))]}" >> /etc/hosts
    done
}


# =======================================================================

VM_HOSTNAME=$1

dnf -y update
dnf -y install epel-release \
               wget \
               net-tools \
               lsof \
               vim \
               curl \
               sshpass

add_user $VM_USER $VM_PASSWORD
regist_host

# change locale
localectl set-locale LANG=en_US.UTF-8

# change hostname
hostnamectl set-hostname $VM_HOSTNAME

# change timezone
timedatectl set-timezone Asia/Seoul
