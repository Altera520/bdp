#!/bin/bash

DIR="$(cd "`dirname "$0"`"; pwd)"
cd $DIR

source ./kafka-env.sh

function reassign {
  JSON_FILE=${1}

  ${KAFKA_HOME}/bin/kafka-reassign-partitions.sh \
    --bootstrap-server ${BOOTSTRAP_SERVERS} \
    --reassignment-json-file ${JSON_FILE} \
    --execute
}

JSON_FILE=${1:-reassign.json}

reassign $JSON_FILE