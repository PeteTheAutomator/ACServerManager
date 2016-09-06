#!/usr/bin/bash
# Bootstrap script for the Assetto Corsa Server Manager


yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
yum install -y ansible python-pip git policycoreutils-python

rm -rf /var/tmp/ACServerManager
git clone https://github.com/PeteTheAutomator/ACServerManager.git /var/tmp/ACServerManager
cd /var/tmp/ACServerManager/ansible

cat > ./vars.yml <<EOL
superuser_name: $NAME
superuser_email: $EMAIL
superuser_pass: $PASS
EOL

ansible-playbook -i 'localhost,' local.yml
