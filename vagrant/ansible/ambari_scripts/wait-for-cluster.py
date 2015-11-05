#!/usr/bin/env python

import json
import os
import requests
import shlex
import socket
import sys
import time


def isclusterbusy(cluster_name):
    '''
    [root@sandbox ~]# curl -u admin:admin http://$(hostname -f):8080/api/v1/clusters/ODP_Sandbox2
    {
      "status" : 404,
      "message" : "The requested resource doesn't exist: Cluster not found, clusterName=ODP_Sandbox2"
    }    
    '''
    found = False
    hostname = socket.gethostname()
    baseurl = "http://%s:8080/api/v1/clusters/%s" % (hostname, cluster_name)
    r = requests.get(baseurl, auth=('admin', 'admin'))
    print "# %s" % r.status_code
    data = json.loads(r.text)
    state = data.get("Clusters", {}).get("provisioning_state", None)

    # "provisioning_state" : "INSTALLED"

    print "# state: %s" % state
    if not state or state == "INIT" or state != "INSTALLED":
        return True
    else:
        return False


def wait_till_finished(cluster_name):

    busy = True
    while busy:
        busy = isclusterbusy(cluster_name)
        time.sleep(10)


if __name__ == "__main__":

    assert len(sys.argv) >= 1, "Usage: <scriptname> <blueprint-name> <cluster-name>"

    clustername = sys.argv[1]
    wait_till_finished(clustername)
