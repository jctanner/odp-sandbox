#!/usr/bin/env python

import json
import os
import requests
import socket
import sys
import time


CLUSTER = "ODP_Sandbox"


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

    if action == 'start':
        post("systemd: Starting all services", "STARTED")
    elif action == 'stop':
        post("systemd: Stopping all services", "INSTALLED")
    elif action == 'status':
        print "Not implemented"
    else:
        print "Usage: <script> <start|stop>"
        return 1



if __name__ == "__main__":
    sys.exit(main())
