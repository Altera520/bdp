#!/bin/bash

increase_disk()
{
    local -r BLOCK=$1
    local -r PARTITION=$2

    # change partition table
    echo -e "resizepart\n${PARTITION}\nYes\n100%" | parted $BLOCK ---pretend-input-tty

    # extend logical group
    xfs_growfs "${BLOCK}${PARTITION}"
}

increase_disk /dev/sda 1