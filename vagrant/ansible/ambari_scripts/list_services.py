#!/usr/bin/env python

import json
import os
import requests
import shlex
import socket
import sys
 
from api_common import get_services

if __name__ == "__main__":

    assert len(sys.argv) >= 1, "Usage: <scriptname> <cluster-name>"

    clustername = sys.argv[1]
    get_services(clustername)
