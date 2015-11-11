#!/bin/bash

URLS="http://download.oracle.com/otn-pub/java/jce/8/jce_policy-8.zip"
URLS="$URLS http://download.oracle.com/otn-pub/java/jdk/8u66-b17/jdk-8u66-linux-x64.tar.gz"
URLS="$URLS http://download.oracle.com/otn-pub/java/jdk/8u66-b17/jre-8u66-linux-x64.tar.gz"

for URL in $URLS; do
    echo $URL
    TAR=$(basename $URL)
    echo $TAR

    if [ ! -f $TAR ]; then

        wget --no-check-certificate \
            --no-cookies \
            --header "Cookie: oraclelicense=accept-securebackup-cookie" \
            $URL

    fi

done

