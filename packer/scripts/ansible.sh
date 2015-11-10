#!/bin/bash -eux

# Install EPEL repository.
yum -y install epel-release

# Install Ansible.
yum -y install ansible python-setuptools

# Run Ansible [defered to packer's ansible-local provisioner]
#cd /opt/ansible ; ansible-playbook -c local -e "packer=True" -v sandbox.yml
touch /var/log/ansible.log
chmod 777 /var/log/ansible.log
