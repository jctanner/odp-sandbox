#!/bin/bash

mkdir -p /opt/odpi/mirror
chmod -R 777 /opt


find /opt -type d | xargs ls -al
