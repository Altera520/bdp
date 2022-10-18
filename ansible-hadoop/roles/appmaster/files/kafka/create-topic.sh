#!/bin/bash

DIR="$(cd "`dirname "$0"`"; pwd)"
cd $DIR

source ./kafka-env.sh

function create_topic {
  TOPIC=$1
  PARTITION_COUNT=$2
  REPLICA_FACTOR=$3

  ${KAFKA_HOME}/bin/kafka-topics.sh \
    --bootstrap-server ${BOOTSTRAP_SERVERS} \
    --create \
    --topic ${TOPIC} \
    --partitions ${PARTITION_COUNT} \
    --replication-factor ${REPLICA_FACTOR}
}

TOPIC=$1
PARTITION_COUNT=$2
REPLICA_FACTOR=${3:-$DEFAULT_REPLICA_FACTOR}

create_topic $TOPIC $PARTITION_COUNT $REPLICA_FACTOR
