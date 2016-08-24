#!/usr/bin/bash
# Bootstrap script for the Assetto Corsa Server Manager

sudo yum install -y python-setuptools python-dev policycoreutils-python openssl-devel git gcc
sudo easy_install pip
sudo pip install ansible

git clone https://github.com/PeteTheAutomator/ACServerManager.git
cd ACServerManager/ansible

cat > ./vars.yml <<EOL
superuser_name: $NAME
superuser_email: $EMAIL
superuser_pass: $PASS
EOL

ansible-playbook -i 'localhost,' local.yml
