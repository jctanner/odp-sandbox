#/bin/bash

curl -u admin:admin http://$(hostname -f):8080/api/v1/clusters
