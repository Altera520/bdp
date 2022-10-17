#!/bin/bash

DIR="$(cd "`dirname "$0"`"; pwd)"
cd $DIR

source ./kafka-env.sh

function describe {
  TOPIC=$1   

  case $TOPIC in
    all)
    ${KAFKA_HOME}/bin/kafka-topics.sh \
     --describe \
     --bootstrap-server ${BOOTSTRAP_SERVERS}
    ;;
    *)
    ${KAFKA_HOME}/bin/kafka-topics.sh \
     --describe \
     --bootstrap-server ${BOOTSTRAP_SERVERS} \
     --topic ${TOPIC}
    ;;
  esac
}

describe $1