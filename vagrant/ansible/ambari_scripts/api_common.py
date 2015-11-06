#!/usr/bin/env python

import json
import os
import requests
import shlex
import socket
import sys
import time

def poll_request(href):

    headers = {'X-Requested-By': 'AMBARI'}
    running = True
    count = 0
    while ((running) and (count < 50)):
        count += 1
        print "#%s: sleeping 5s" % count
        time.sleep(5)
        r = requests.get(href, auth=('admin', 'admin'), headers=headers)
        rdict = json.loads(r.text)
        if str(rdict['Requests']['end_time']) != "-1":
            print "# end_time: %s" % rdict['Requests']['end_time']
            running = False
        print "# end_time: %s" % rdict['Requests']['end_time']
        #import pdb; pdb.set_trace()
    

def get_services(cluster_name, output=True):

    # POST to /api/v1/clusters/<CLUSTER_NAME>
    hostname = socket.gethostname()
    headers = {'X-Requested-By': 'AMBARI'}
    baseurl = "http://%s:8080/api/v1/clusters/%s/services" % (hostname, cluster_name)
    r = requests.get(baseurl, auth=('admin', 'admin'), headers=headers)

    if output:
        print "# %s" % r.status_code
        for x in r.text.split('\n'):
            print "# %s" % x

    rdict = json.loads(r.text)
    services = rdict.get('items', {})
    return services

