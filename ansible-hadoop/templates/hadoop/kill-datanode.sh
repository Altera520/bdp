#!/bin/bash

DNPID=$("$JAVA_HOME"/bin/jps | grep -E '^[0-9]+[ ]+DataNode$' | awk '{print $1}')

if [ $? -gt 0 ]; then
  echo "ERROR: Command failed while looking for DataNode PID."
  exit 1
fi

if [ -z "$DNPID" ];
then
  echo "ERROR: Could not find a DataNode PID."
  exit 1
fi

kill -9 "$DNPID"

if [ $? -gt 0 ]; then
  echo "ERROR: Kill command failed."
  exit 1
fi