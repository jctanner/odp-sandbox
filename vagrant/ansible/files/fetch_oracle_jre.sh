#!/bin/bash

#URL="http://download.oracle.com/otn/java/jdk/8u40-b26/jre-8u40-linux-x64.tar.gz"
#TAR="jre-8u40-linux-x64.tar.gz"
URL="http://download.oracle.com/otn-pub/java/jdk/8u66-b17/jre-8u66-linux-x64.tar.gz"
TAR="jre-8u66-linux-x64.tar.gz"

if [ ! -f $TAR ]; then

    wget --no-check-certificate \
        --no-cookies \
        --header "Cookie: oraclelicense=accept-securebackup-cookie" \
        $URL

fi

cp $TAR /var/lib/ambari-server/resources/.
