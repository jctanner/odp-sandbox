# odpi-sandbox
ODPi sandbox automation

Code in this repository was heavily referenced from:
* https://github.com/geerlingguy/packer-centos-7

Quickstart
----------

````shell
cd packer
packer build centos7.json
vagrant box add --name odpi-test-0 --provider virtualbox builds/virtualbox-centos7.box
````

````shell
cd vagrant
vagrant up
````
