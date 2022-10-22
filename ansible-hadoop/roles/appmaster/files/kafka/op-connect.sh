#!/bin/bash

DIR="$(cd "`dirname "$0"`"; pwd)"
cd $DIR

source ./kafka-env.sh

function op_kafka_connect {
    command=$1
    connector_name=$2

    case ${command} in
      start)
        connector_config=$3
        curl -X POST ${KAFKA_CONNECTOR_URL}/connectors \
        -H 'Content-Type: application/json' \
        -d @"${HOME}/kafka/connector/${connector_config}" | jq '.'
      ;;
      stop)
        curl -X DELETE ${KAFKA_CONNECTOR_URL}/connectors/${connector_name}
      ;;
      pause)
        curl -X PUT ${KAFKA_CONNECTOR_URL}/connectors/${connector_name}/pause
      ;;
      resume)
        curl -X P UT ${KAFKA_CONNECTOR_URL}/connectors/${connector_name}/resume
      ;;
      status)
        curl -X GET ${KAFKA_CONNECTOR_URL}/connectors/${connector_name}/status | jq '.'
      ;;
      select-config)
        curl -X GET ${KAFKA_CONNECTOR_URL}/connectors/${connector_name}/config | jq '.'
      ;;
      update-config)
        curl -X PUT ${KAFKA_CONNECTOR_URL}/connectors/${connector_name}/config
      ;;
      validate-config)
        curl -X PUT ${KAFKA_CONNECTOR_URL}/connectors/${connector_name}/config/validate
      ;;
      select-connector)
        curl -X GET ${KAFKA_CONNECTOR_URL}/connectors/${connector_name} | jq '.'
      ;;
      select-connectors)
        curl -X GET ${KAFKA_CONNECTOR_URL}/connectors | jq '.'
      ;;
      select-connect)
        curl -X GET ${KAFKA_CONNECTOR_URL}/ | jq '.'
      ;;
      select-plugins)
        curl -X GET ${KAFKA_CONNECTOR_URL}/connector-plugins | jq '.'
      ;;
      select-topics)
        curl -X GET ${KAFKA_CONNECTOR_URL}/connectors/${connector_name}/topics | jq '.'
      ;;
    esac
}

op_kafka_connect $@