#!/usr/bin/bash
# Bootstrap script for the Assetto Corsa Server Manager

yum install -y python-setuptools python-devel policycoreutils-python openssl-devel git gcc libffi-devel
easy_install pip
pip install ansible

rm -rf /var/tmp/ACServerManager
git clone https://github.com/PeteTheAutomator/ACServerManager.git /var/tmp/ACServerManager
cd /var/tmp/ACServerManager/ansible
git pull

cat > ./vars.yml <<EOL
superuser_name: $NAME
superuser_email: $EMAIL
superuser_pass: $PASS
EOL

ansible-playbook -i 'localhost,' local.yml
