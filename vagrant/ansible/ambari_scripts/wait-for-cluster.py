#!/usr/bin/env python

import json
import os
import requests
import shlex
import socket
import sys
import time

from api_common import get_services
from api_common import get_services_and_components


def isclusterbusy(cluster_name):
    '''
    [root@sandbox ~]# curl -u admin:admin http://$(hostname -f):8080/api/v1/clusters/ODP_Sandbox2
    {
      "status" : 404,
      "message" : "The requested resource doesn't exist: Cluster not found, clusterName=ODP_Sandbox2"
    }    
    '''
    found = False
    installing = False
    starting = False

    hostname = socket.gethostname()
    baseurl = "http://%s:8080/api/v1/clusters/%s" % (hostname, cluster_name)
    r = requests.get(baseurl, auth=('admin', 'admin'))
    print "# %s" % r.status_code
    data = json.loads(r.text)
    state = data.get("Clusters", {}).get("provisioning_state", None)

    # "provisioning_state" : "INSTALLED"

    # Check the services and components
    svcdata = get_services_and_components(cluster_name)
    #import pdb; pdb.set_trace()

    errors = 0
    for k,v in svcdata.iteritems():
        if v['state'] == 'INSTALL_FAILED':
            print "# %s installation failed" % k
            errors += 1
        elif v['state'] == 'INSTALLING':
            installing = True
        elif v['state'] == 'STARTING':
            starting = True
        print "# %s: %s" % (k, v['state'])

        for k2,v2 in v['components'].iteritems():
            if v2['state'] == 'INSTALL_FAILED':
                print "# %s installation failed" % k2
                errors += 1
            elif v2['state'] == 'INSTALLING':
                installing = True
            elif v2['state'] == 'STARTING':
                starting = True
            print "#\t%s: %s" % (k2, v2['state'])

    if errors > 0:
        sys.exit(errors)

    print "# state: %s" % state
    if (not state) or (state == "INIT") or (state != "INSTALLED") or installing or starting:
        # BUSY ...
        return True
    else:
        # NOT BUSY ...
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
