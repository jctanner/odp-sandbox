# odpi-sandbox
ODPi sandbox automation

Code in this repository was heavily referenced from:
* https://github.com/geerlingguy/packer-centos-7
* http://www.tecmint.com/multiple-centos-installations-using-kickstart/
* https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Installation_Guide/sect-kickstart-syntax.html


Quickstart
----------

````shell
cd packer
# add --debug to step through each phase
packer build centos7.json
vagrant box add --name odpi-test-0 --provider virtualbox builds/virtualbox-centos7.box
````

````shell
cd vagrant
vagrant up
````
