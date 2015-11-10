#!/bin/bash -eux

# Install EPEL repository.
yum -y install epel-release

# Install Ansible.
yum -y install ansible python-setuptools

# Run Ansible
cd /opt/ansible ; ansible-playbook -c local -e "packer=True" -v sandbox.yml
