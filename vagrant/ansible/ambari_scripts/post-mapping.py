#!/usr/bin/env python

import json
import os
import requests
import shlex
import socket
import sys
import pprint

def constructInventory():
    data = {}
    data['_meta'] = {}
    data['_meta']['hostvars'] = {}


    data['all'] = {}
    data['all']['hosts'] = []

    data['nodes'] = {}
    data['nodes']['hosts'] = []


    f = open('/etc/hosts', 'rb')
    fdata = f.read()
    f.close()
    flines = [x.strip() for x in fdata.split('\n') if x.strip()]
    flines = [x for x in flines if not x.startswith('#')]

    for x in flines:
        if x.startswith('127.0.0.1') or 'localhost' in x:
            continue

        parts = shlex.split(x)

        thisfqdn = parts[1]
        thishostname = thisfqdn.split('.')[0]
        thisip = parts[0]
        thiskey = "/vagrant/.vagrant/machines/%s/virtualbox/private_key" % thishostname

        data['all']['hosts'].append(thisfqdn)
        data['_meta']['hostvars'][thisfqdn] = {}
        data['_meta']['hostvars'][thisfqdn]['ansible_ssh_private_key_file'] = thiskey
        data['_meta']['hostvars'][thisfqdn]['hostname_short'] = thishostname
        data['_meta']['hostvars'][thisfqdn]['hostname_long'] = thishostname
        data['_meta']['hostvars'][thisfqdn]['ip_address'] = thisip

        data['nodes']['hosts'].append(thisfqdn)

    return data


def check_cluster(cluster_name):
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

    if r.status_code == 404:
        return False
    else:
        return True

def construct_and_post_payload(blueprint_name, cluster_name):

    # http://www.pythian.com/blog/ambari-blueprints-and-one-touch-hadoop-clusters/
    '''
    {
      "blueprint":"hadoop-benchmark",
      "host_groups: [
        { 
          "name":"master",
          "hosts":[{"fqdn":"host-1"}]
        },
        {
          "name":"slaves",
          "hosts":[ 
            {"fqdn":"host-2"},
            {"fqdn":"host-3"}  
          ]
      ]
    }
    '''

    # https://blog.codecentric.de/en/2014/05/lambda-cluster-provisioning/
    '''
	{ "blueprint":"blueprint-c1",
	  "host-groups":[
		{ "name":"host_group_1",
		  "hosts":[
			{ "fqdn":"one.cluster",
			  "ip":"192.168.0.101" }, ... ] }, ... ] }
    '''

    inventory = constructInventory()
    hosts = inventory['nodes']['hosts']

    # Create the first group
    group1 = {'name': 'host_group_1',
              'hosts': [] }

    # Create the mapping structure for the POST
    data = {'blueprint': blueprint_name,
            'host_groups': [group1] }

    # Add each host to group1
    for host in hosts:
        host_dict = {'fqdn': host,
                     'ip': inventory['_meta']['hostvars'][host]['ip_address']}            
        data['host_groups'][0]['hosts'].append(host_dict)

    #print data
    #pprint.pprint(data)
	print json.dumps(data, indent=True)
    #sys.exit(1)


    # POST to /api/v1/clusters/<CLUSTER_NAME>
    hostname = socket.gethostname()
    headers = {'X-Requested-By': 'AMBARI'}
    baseurl = "http://%s:8080/api/v1/clusters/%s" % (hostname, cluster_name)
    print "# POST --> %s" % baseurl
    r = requests.post(baseurl, auth=('admin', 'admin'), 
                        data=json.dumps(data), headers=headers)

    print "# %s" % r.status_code
    for x in r.text.split('\n'):
        print "# %s" % x


def validate_hosts_registered():
    
    inventory = constructInventory()
    hosts = inventory['nodes']['hosts']

    for x in hosts:
        hostname = socket.gethostname()
        headers = {'X-Requested-By': 'AMBARI'}
        baseurl = "http://%s:8080/api/v1/hosts/%s" % (hostname, x)
        print "# POST --> %s" % baseurl
        r = requests.get(baseurl, auth=('admin', 'admin'), headers=headers)

        if r.status_code != 200:
            print "%s is not registered, failing!"
            sys.exit(1)
        else:
            print "# host: %s is registered" % x

def post_mapping(blueprint_name, cluster_name, checkhosts=True, checkcluster=False):

    if checkhosts:
        validate_hosts_registered()

    if checkcluster:
        if not check_cluster(cluster_name):
            construct_and_post_payload(blueprint_name, cluster_name)
    else:
        construct_and_post_payload(blueprint_name, cluster_name)


if __name__ == "__main__":

    assert len(sys.argv) >= 2, "Usage: <scriptname> <blueprint-name> <cluster-name>"

    blueprint = sys.argv[1]
    clustername = sys.argv[2]
    post_mapping(blueprint, clustername)
