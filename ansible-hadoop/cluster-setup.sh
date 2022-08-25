#!/bin/bash

INVENTORY=inventories/host.yml
ACT=setup

# component priority first to last, first component is highest
COMPONENTS="
zookeeper
kafka
mariadb
airflow
hadoop
hive
"

for COMPONENT in "${COMPONENTS[@]}"
do
    ansible-playbook -i $INVENTORY $COMPONENT --extra-vars "'${ACT}'"
done