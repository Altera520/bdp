#!/bin/bash

function file_exists {
	FILE=$1
	if [ -e $FILE ]; then
		return 0
	else
		return 1
	fi
}

function dir_exists {
	DIR=$1
	if [ -d $DIR ]; then
		return 0
	else
		return 1
	fi
}