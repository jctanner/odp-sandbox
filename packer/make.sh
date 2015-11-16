#!/bin/bash

PACKER=$PACKER
if [ -z "$PACKER" ]; then
    PACKER="packer"
fi
#echo "PACKER=$PACKER"
#exit 1


rm -rf builds/*

PACKER_LOG=1 PACKER_LOG_PATH=packer.log \
    $PACKER build --only=virtualbox-iso $@ centos7.json 
RC=$?
if [[ $RC -ne 0 ]]; then
    echo "packer build failed"
    exit $RC
fi

vagrant box remove odpi-test-0
vagrant box add --name odpi-test-0 --provider virtualbox builds/virtualbox-centos7.box    
