#!/bin/sh

SNNPID=$("$JAVA_HOME"/bin/jps | grep -E '^[0-9]+[ ]+SecondaryNameNode$' | awk '{print $1}')

if [ $? -gt 0 ]; then
  echo "ERROR: Command failed while looking for SecondaryNameNode PID."
  exit 1
fi

if [ -z "$SNNPID" ];
then
  echo "ERROR: Could not find a SecondaryNameNode PID."
  exit 1
fi

kill -9 "$SNNPID"

if [ $? -gt 0 ]; then
  echo "ERROR: Kill command failed."
  exit 1
fi

