#!/bin/bash

service ambari-server stop
service ambari-agent stop

rm -rf /var/log/ambari-server/*
rm -rf /var/log/ambari-agent/*

ambari-server reset --verbose -s
ambari-server setup --verbose -s

service ambari-server start

echo "waiting for ambariserver to settle "
sleep 5
service ambari-agent start
