#!/bin/bash
INVENTORY=inventories/host.yml

# component priority first to last, first component is highest
COMPONENTS="
zookeeper
kafka
mariadb
airflow
hadoop
hive
"

cluster_setup()
{    
    local -r ACT=setup
    for COMPONENT in "${COMPONENTS[@]}"
    do
        ansible-playbook -i $INVENTORY $COMPONENT --extra-vars "'${ACT}'"
    done
}

cluster_start()
{
    
}

cluster_stop()
{
    
}

case $1 in
    'setup')
        cluster_setup
    ;;
    'start')
        cluster_start
    ;;
    'stop')
        cluster_stop
    ;;
esac
