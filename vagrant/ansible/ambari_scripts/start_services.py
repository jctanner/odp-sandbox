#!/usr/bin/env python

# http://hortonworks.com/community/forums/topic/automatically-starting-services/

import json
import os
import requests
import shlex
import socket
import sys
import time
 
from api_common import get_services
from api_common import poll_request
   

def start_services(cluster_name):

    services = get_services(cluster_name, output=False)

    headers = {'X-Requested-By': 'AMBARI'}
    payload = {"ServiceInfo": {"state" : "STARTED"}} 
    for x in services:

        # {"RequestInfo": {"context" :"Start YARN via REST"}, "Body": {"ServiceInfo": {"state": "STARTED"}}}

        thispayload = {'RequestInfo': {'context': 'Start %s from API' % x['ServiceInfo']['service_name']},
                       'Body': payload}

        print "# Starting: %s" % x
        r = requests.put(x['href'], auth=('admin', 'admin'), 
                         data=json.dumps(thispayload), headers=headers)
        print "# PUT: %s" % r.status_code
        #print "# %s" % r.text
        #import pdb; pdb.set_trace()

        # 200 == the service is already started
        # 201 == the service will be started
        # 202 == ???
        if (int(r.status_code) != 200) \
            and (int(r.status_code) != 201) \
            and (int(r.status_code) != 202):

            print "# Failure starting %s: %s" % (x, r.status_code)
            print r.text
            sys.exit(1)

        # Poll the startup task if the rc was 201
        if (int(r.status_code) == 201) or (int(r.status_code) == 202):
            print "# Polling startup for %s" % x
    
            #import pdb; pdb.set_trace()
            # null text means the service is already running
            #if not r.text:
            #    print "r.text was null, skipping this service"
            #    continue

            rdict = json.loads(r.text)
            #"href" : "http://sandbox.odp.org:8080/api/v1/clusters/ODP_Sandbox/requests/7"
            #import pdb; pdb.set_trace()
            print "# Polling %s startup" % x['ServiceInfo']['service_name']
            #import pdb; pdb.set_trace()
            print rdict
            if 'href' in rdict:
                poll_request(rdict['href'], name=x)


if __name__ == "__main__":

    assert len(sys.argv) >= 1, "Usage: <scriptname> <cluster-name>"

    clustername = sys.argv[1]
    start_services(clustername)
