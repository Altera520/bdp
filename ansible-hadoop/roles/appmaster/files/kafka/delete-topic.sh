#!/bin/bash

DIR="$(cd "`dirname "$0"`"; pwd)"
cd $DIR

source ./kafka-env.sh

function delete_topic {
  TOPIC=$1
  PARTITION_COUNT=$2
  REPLICA_FACTOR=$3

  ${KAFKA_HOME}/bin/kafka-topics.sh \
    --bootstrap-server ${BOOTSTRAP_SERVERS} \
    --delete \
    --topic ${TOPIC}
}

delete_topic $1
