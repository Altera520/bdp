#!/bin/sh

NNPID=$("$JAVA_HOME"/bin/jps | grep -E '^[0-9]+[ ]+NameNode$' | awk '{print $1}')

if [ $? -gt 0 ]; then
  echo "ERROR: Command failed while looking for NameNode PID."
  exit 1
fi

if [ -z "$NNPID" ];
then
  echo "ERROR: Could not find a NameNode PID."
  exit 1
fi

kill -9 "$NNPID"

if [ $? -gt 0 ]; then
  echo "ERROR: Kill command failed."
  exit 1
fi

