# Installing vagrant keys
# source: https://gun.io/blog/building-vagrant-machines-with-packer/

id vagrant
RC=$?
if [[ $RC -ne 0 ]]; then
    useradd vagrant
fi

echo "vagrant:vagrant" | chpasswd

mkdir -p /home/vagrant/.ssh
chmod 700 /home/vagrant/.ssh

cd /home/vagrant/.ssh

which wget
RC=$?
if [[ $RC -ne 0 ]]; then
    yum -y install wget
fi

wget --no-check-certificate 'https://raw.github.com/mitchellh/vagrant/master/keys/vagrant.pub' -O authorized_keys
chmod 600 /home/vagrant/.ssh/authorized_keys
chown -R vagrant:vagrant /home/vagrant
