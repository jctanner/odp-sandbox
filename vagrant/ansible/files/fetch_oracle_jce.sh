#!/bin/bash

URL="http://download.oracle.com/otn-pub/java/jce/8/jce_policy-8.zip"
TAR="jce_policy-8.zip"

if [ ! -f $TAR ]; then

    wget --no-check-certificate \
        --no-cookies \
        --header "Cookie: oraclelicense=accept-securebackup-cookie" \
        $URL

fi

cp $TAR /var/lib/ambari-server/resources/.
