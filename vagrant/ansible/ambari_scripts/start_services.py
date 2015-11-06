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
        print x
        r = requests.put(x['href'], auth=('admin', 'admin'), 
                         data=json.dumps(payload), headers=headers)
        print "# %s" % r.status_code
        #print "# %s" % r.text

        # null text means the service is already running
        if not r.text:
            continue

        rdict = json.loads(r.text)
        #"href" : "http://sandbox.odp.org:8080/api/v1/clusters/ODP_Sandbox/requests/7"
        #import pdb; pdb.set_trace()
        print "# Polling %s startup" % x['ServiceInfo']['service_name']
        poll_request(rdict['href'])


if __name__ == "__main__":

    assert len(sys.argv) >= 1, "Usage: <scriptname> <cluster-name>"

    clustername = sys.argv[1]
    start_services(clustername)
