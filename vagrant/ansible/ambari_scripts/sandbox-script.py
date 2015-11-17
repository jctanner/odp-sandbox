#!/usr/bin/env python

# systemctl restart ambari-server ; systemctl restart ambari-agent ; ./sandbox-script.py start

import json
import os
import requests
import socket
import sys
import time


CLUSTER = "ODP_Sandbox"

def get_services_and_components():

    # Return a dictionary of services and components

    svcdict = {}

    # POST to /api/v1/clusters/<CLUSTER_NAME>
    hostname = socket.gethostname()
    headers = {'X-Requested-By': 'AMBARI'}
    baseurl = "http://%s:8080/api/v1/clusters/%s/services" % (hostname, CLUSTER)
    r = requests.get(baseurl, auth=('admin', 'admin'), headers=headers)
    #import pdb; pdb.set_trace()

    data = json.loads(r.text)

    if not data:
        print r.status_code
        import pdb; pdb.set_trace()

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

    return svcdata


def get_cluster_status():

    # Iterate services and generate a synthetic aggregate state

    states = []
    try:
        svcdata = get_services_and_components()
    except:
        svcdata = {}
    
    for k,v in svcdata.iteritems():
        thisstate = None
        if type(v) == dict:
            if 'state' in v:
                if v['state'] == 'UNKNOWN':
                    thisstate = "stopped"
                elif v['state'] == 'INSTALLED':
                    thisstate = "stopped"
                elif v['state'] == 'STARTING':
                    thisstate = "started"
                elif v['state'] == 'STARTED':
                    thisstate = "started"
                states.append(thisstate)

    print "# states: %s" % states

    state = 'stopped'
    if states:
        if 'stopped' in states and not 'started' in states:
            state = 'stopped'
        elif 'started' in states and not 'stopped' in states:
            state = 'started'
    return state


def wait_for_ambari():

    # poll port 8080 until it is listening

    counter = 0
    maxcount = 100
    interval = 2
    running = False

    print "# Polling ambari port ..."
    while (not running) or (counter < maxcount):
        print "# Opening socket ..."
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8080))
        print " Result: %s" % result
        if result == 0:
            running = True
            break
        else:
            print "# sleeping %ss" % interval
            counter += 1
            time.sleep(interval)

    print "# Ambari port is open"

    # Now wait for the API to be available ...
    hostname = socket.gethostname()
    headers = {'X-Requested-By': 'AMBARI'}
    baseurl = "http://%s:8080/api/v1/clusters/%s" % (hostname, CLUSTER)
    counter = 0
    running = False

    print "# Polling ambari API ..."
    while (not running) or (counter < maxcount):
        r = requests.get(baseurl, auth=('admin', 'admin'), headers=headers)
        if r.status_code in [200, 201, 202]:
            running = True
            break        
        else:
            print "# %s" % r.status_code
            print "# sleeping %ss" % interval
            counter += 1
            time.sleep(interval)

    print "Waiting for services to exit 'UNKNOWN' state"
    counter = 0
    unknowns = None

    while (not unknowns) or (counter < maxcount):
        unknowns = 0
        svcdata = get_services_and_components()
        if not svcdata:
            unknowns = -1
            print "# no services returned yet"
        else:
            #import pdb; pdb.set_trace()
            for k,v in svcdata.iteritems():
                if type(v) == dict:
                    if 'state' in v:
                        if v['state'] == 'UNKNOWN':
                            unknowns += 1
            print "# total unknown states: %s" % unknowns
        if unknowns == 0:
            break
        else:
            print "# sleeping"
            counter += 1
            time.sleep(interval)        


def post(message,state):

    # message: the human readable description that would show up in the UI
    # state: INSTALLED or STARTED

    hostname = socket.gethostname()
    headers = {'X-Requested-By': 'AMBARI'}
    baseurl = "http://%s:8080/api/v1/clusters/%s/services" % (hostname, CLUSTER)

    # X-Requested-By is an ambari requirement
    headers = {'X-Requested-By': 'AMBARI'}
    payload = {"ServiceInfo": {"state" : "%s" % state.upper()}} 
    thispayload = {'RequestInfo': {'context': message},
                   'Body': payload}

    r = requests.put(baseurl, auth=('admin', 'admin'), 
                     data=json.dumps(thispayload), headers=headers)
    print "# PUT: %s" % r.status_code

    # 200 == the service is already started
    # 201 == the service will be started
    # 202 == ???
    if (int(r.status_code) != 200) \
        and (int(r.status_code) != 201) \
        and (int(r.status_code) != 202):

        print "# Failure: %s" % (r.status_code)
        print r.text
        sys.exit(1)

    # Poll the startup task if the rc was 201
    if (int(r.status_code) == 201) or (int(r.status_code) == 202):
        rdict = json.loads(r.text)
        print rdict
        if 'href' in rdict:
            poll_request(rdict['href'])


def poll_request(href):

    # Sleep until a task is finished or a timeout is exceeded

    headers = {'X-Requested-By': 'AMBARI'}
    running = True
    count = 0
    while ((running) and (count < 100)):
        count += 1
        print "# %s: sleeping 5s" % (count)
        time.sleep(5)
        r = requests.get(href, auth=('admin', 'admin'), headers=headers)
        rdict = json.loads(r.text)
        #print rdict
        if str(rdict['Requests']['end_time']) != "-1":
            print "# end_time: %s" % (rdict['Requests']['end_time'])
            running = False
        print "# end_time: %s" % (rdict['Requests']['end_time'])
        #import pdb; pdb.set_trace()



def main():

    action = sys.argv[1]

    state = get_cluster_status()

    if action == 'start':
        if state == 'stopped':
            print "STARTING sandbox"
            wait_for_ambari()
            post("systemd: Starting all services", "STARTED")
        else:
            print "sandbox already started"
    elif action == 'stop':
        if state == 'started':
            print "STOPPING sandbox"
            post("systemd: Stopping all services", "INSTALLED")
        else:
            print "sandbox already stopped"
    elif action == 'status':
        print "Not implemented"
    else:
        print "Usage: <script> <start|stop>"
        return 1



if __name__ == "__main__":
    sys.exit(main())
