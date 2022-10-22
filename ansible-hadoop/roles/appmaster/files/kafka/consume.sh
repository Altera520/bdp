#!/bin/bash

DIR="$(cd "`dirname "$0"`"; pwd)"
cd $DIR

source ./kafka-env.sh

function consume {
  TOPIC=$1
  STARTING_OFFSETS=$2


  case ${STARTING_OFFSETS} in
    earliest)
    ${KAFKA_HOME}/bin/kafka-console-consumer.sh \
      --bootstrap-server ${BOOTSTRAP_SERVERS} \
      --topic ${TOPIC} \
      --from-beginning
    ;;
    latest)
    ${KAFKA_HOME}/bin/kafka-console-consumer.sh \
      --bootstrap-server ${BOOTSTRAP_SERVERS} \
      --topic ${TOPIC}
    ;;
  esac
}

TOPIC=$1
STARTING_OFFSETS=${2:-latest}

consume ${TOPIC} ${STARTING_OFFSETS}