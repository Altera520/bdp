#!/bin/bash

source '/tmp/env.sh'

root_passwd()
{
    local -r PASSWD=$1
    echo $PASSWD | passwd --stdin root
}

add_user()
{
    local -r USER=$1
    local -r PASSWD=$2
    useradd -m -s /bin/bash -U $USER
    cp -pr /home/vagrant/.ssh "/home/$USER/"
    chown -R "$USER:$USER" "/home/$USER"
    echo $PASSWD | passwd --stdin $USER
    echo "%$USER ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/$USER"
}

regist_host()
{
    local -r NODES=( $(cat /tmp/node-specs.yaml | grep -E 'name|ip'  | tr ':' '\n' | grep -vE 'name|ip') )
    local -r LENGTH=${#NODES[@]}

    for (( i=0; i<${LENGTH}; i+=2 ));
    do
        echo "${NODES[$(($i+1))]} ${NODES[$i]}" >> /etc/hosts
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
               sshpass \
               git \
               glibc-langpack-ko

root_passwd $VM_PASSWORD
add_user $VM_USER $VM_PASSWORD
regist_host

# change locale
#localectl set-locale LANG=ko_KR.utf8
#localectl set-locale LANG=en_US.utf8

# change hostname
hostnamectl set-hostname $VM_HOSTNAME

# change timezone
timedatectl set-timezone Asia/Seoul
