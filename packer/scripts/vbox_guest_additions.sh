#!/bin/bash
# https://github.com/gwagner/packer-centos/blob/master/provisioners/install-virtualbox-guest-additions.sh

# Only run this script if the machine is hosted by virtualbox
VTYPE=$(virt-what | head -n1)
if [[ "$VTYPE" -ne "virtualbox" ]]; then
	exit 0
fi

# Mount the disk image
cd /tmp
mkdir /tmp/isomount
mount -t iso9660 -o loop /home/vagrant/VBoxGuest*.iso /tmp/isomount

# Install the drivers
/tmp/isomount/VBoxLinuxAdditions.run

# Cleanup
umount isomount
rm -rf isomount /root/VBoxGuestAdditions.iso
