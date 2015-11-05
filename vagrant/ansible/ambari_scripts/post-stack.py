#!/usr/bin/env python

import json
import os
import requests
import shlex
import socket
import sys
 

def post_stack(cluster_name, stack_name):

    data = {'ServiceInfo': {'service_name': stack_name } }

    # POST to /api/v1/clusters/<CLUSTER_NAME>
    hostname = socket.gethostname()
    headers = {'X-Requested-By': 'FOOBAR'}
    baseurl = "http://%s:8080/api/v1/clusters/%s/services" % (hostname, cluster_name)
    print "# POST --> %s" % baseurl
    r = requests.post(baseurl, auth=('admin', 'admin'), data=json.dumps(data), headers=headers)

    print "# %s" % r.status_code
    for x in r.text.split('\n'):
        print "# %s" % x


if __name__ == "__main__":

    assert len(sys.argv) >= 2, "Usage: <scriptname> <cluster-name> <stack-name>"

    clustername = sys.argv[1]
    stackname = sys.argv[2]
    post_stack(clustername, stackname)
