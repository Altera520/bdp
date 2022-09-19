#!/bin/bash

VM_COUNT=$(vagrant global-status | grep virtualbox | wc -l)

NETWORK='1'

expect -c "
spawn env VAGRANT_EXPERIMENTAL=disks vagrant up
expect \"bridge to\"
send \"${NETWORK}\n\"
"