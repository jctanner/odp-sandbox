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
        #print rdict
        if str(rdict['Requests']['end_time']) != "-1":
            print "# end_time: %s" % rdict['Requests']['end_time']
            running = False
        print "# end_time: %s" % rdict['Requests']['end_time']
        #import pdb; pdb.set_trace()
    

def get_services_and_components(cluster_name):

    svcdict = {}

    # POST to /api/v1/clusters/<CLUSTER_NAME>
    hostname = socket.gethostname()
    headers = {'X-Requested-By': 'AMBARI'}
    baseurl = "http://%s:8080/api/v1/clusters/%s/services" % (hostname, cluster_name)
    r = requests.get(baseurl, auth=('admin', 'admin'), headers=headers)

    data = json.loads(r.text)
    #print data
    for x in data['items']:

        #"ServiceInfo" : {
        #  "cluster_name" : "ODP_Sandbox",
        #  "maintenance_state" : "OFF",
        #  "service_name" : "ZOOKEEPER",
        #  "state" : "INSTALL_FAILED"
        #},

        svc = requests.get(x['href'], auth=('admin', 'admin'), headers=headers)
        svcdata = json.loads(svc.text)
        svcname = svcdata['ServiceInfo']['service_name']
        svcstate = svcdata['ServiceInfo']['state']
        svcdict[svcname] = {}
        svcdict[svcname]['components'] = {}
        svcdict[svcname]['state'] = svcstate

        # Iterate through the components
        for xc in svcdata['components']:

            #  "ServiceComponentInfo" : {
            #    "category" : "MASTER",
            #    "cluster_name" : "ODP_Sandbox",
            #    "component_name" : "METRICS_COLLECTOR",
            #    "installed_count" : 0,
            #    "service_name" : "AMBARI_METRICS",
            #    "started_count" : 0,
            #    "state" : "STARTED",
            #    "total_count" : 1
            #  },

            #print xc
            comp = requests.get(xc['href'], auth=('admin', 'admin'), headers=headers)
            compdata = json.loads(comp.text)
            #print comp.text
            compname = compdata['ServiceComponentInfo']['component_name']
            compstate = compdata['ServiceComponentInfo']['state']
            svcdict[svcname]['components'][compname] = {}
            svcdict[svcname]['components'][compname]['state'] = compstate


    return svcdict


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

