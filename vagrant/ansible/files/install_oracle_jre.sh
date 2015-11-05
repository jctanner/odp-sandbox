#!/bin/bash

URL="http://download.oracle.com/otn-pub/java/jdk/8u65-b17/jre-8u65-linux-x64.rpm"
RPM="jre-8u65-linux-x64.rpm"

if [ ! -f $RPM ]; then

    wget --no-check-certificate \
        --no-cookies \
        --header "Cookie: oraclelicense=accept-securebackup-cookie" \
        $URL

fi

yum -y install $RPM
