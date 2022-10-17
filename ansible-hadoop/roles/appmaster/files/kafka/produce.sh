#!/bin/bash

DIR="$(cd "`dirname "$0"`"; pwd)"
cd $DIR

source ./kafka-env.sh

function produce {
  TOPIC=$1

  ${KAFKA_HOME}/bin/kafka-console-producer.sh \
    --broker-list ${BOOTSTRAP_SERVERS} \
    --topic ${TOPIC}
}

produce $1
