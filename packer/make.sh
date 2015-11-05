#!/bin/bash
PACKER_LOG=1 PACKER_LOG_PATH=packer.log \
    packer build --only=virtualbox-iso $@ centos7.json 
