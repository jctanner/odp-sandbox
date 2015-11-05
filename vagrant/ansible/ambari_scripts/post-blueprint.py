#!/usr/bin/env python

import json
import os
import requests
import socket
import sys

def check_blueprint(blueprint_name):

    ''' Check if a blueprint already exists '''

    #{u'href': u'http://master.lab.net:8080/api/v1/blueprints',
    # u'items': [{u'Blueprints': {u'blueprint_name': u'TEST002'},
    #             u'href': u'http://master.lab.net:8080/api/v1/blueprints/TEST002'},
    #            {u'Blueprints': {u'blueprint_name': u'TEST00X'},
    #             u'href': u'http://master.lab.net:8080/api/v1/blueprints/TEST00X'}]}

    found = False

    hostname = socket.gethostname()
    baseurl = "http://%s:8080/api/v1/blueprints" % (hostname)
    r = requests.get(baseurl, auth=('admin', 'admin'))
    print "# %s" % r.status_code
    jdata = json.loads(r.text)

    # The list of names is buried down in the json structure ...    
    if 'items' in jdata:
        for item in jdata['items']:
            if item.get('Blueprints', {}).get('blueprint_name', None) == blueprint_name:
                found = True
    if found:
        print "# %s already exists" % blueprint_name
    else:
        print "# %s does not exist yet" % blueprint_name
    return found


def post_blueprint(blueprint, blueprintname):

    # validate_topolgy=false seems to be very important
    # with making single node sandboxes. I keep running
    # into nonsensical 500ISEs when I try to post the 
    # host mapping afterwards, unless I set the parameter.

    hostname = socket.gethostname()
    baseurl = "http://%s:8080/api/v1/blueprints/%s?validate_topology=false" % (hostname, blueprintname)
    print "# %s" %  baseurl
    f = open(blueprint, 'rb')
    fdata = f.read()
    f.close()
    jdata = json.loads(fdata)

    if not check_blueprint(blueprintname):
        print "# POST'ing %s" % blueprint
        # Amari requires the X-Requested-By header ... 
        #   https://blog.codecentric.de/en/2014/05/lambda-cluster-provisioning/
        headers = {'X-Requested-By': 'AMBARI'}
        # POST the json ...
        r = requests.post(baseurl, auth=('admin', 'admin'), 
                          data=json.dumps(jdata), headers=headers)
        print "# %s" % r.status_code
        for x in r.text.split('\n'):
            print "# %s" % x


if __name__ == "__main__":

    assert len(sys.argv) >= 3, "Usage: <scriptname> <blueprint-file> <blueprintname>"
    assert os.path.isfile(sys.argv[1]), "Can not read %s" % sys.argv[1]

    blueprint = sys.argv[1]
    blueprintname = sys.argv[2]
    post_blueprint(blueprint, blueprintname)
