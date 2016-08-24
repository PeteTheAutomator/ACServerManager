#!/usr/bin/bash
# Bootstrap script for the Assetto Corsa Server Manager

SU_NAME=$1
SU_EMAIL=$2
SU_PASS=$3

sudo yum install -y python-setuptools python-dev openssl-devel git gcc
sudo easy_install pip
sudo pip install ansible

git clone https://github.com/PeteTheAutomator/ACServerManager.git
cd ACServerManager/ansible

cat > ./vars.yml <<EOL
superuser_name: $SU_NAME
superuser_email: $SU_EMAIL
superuser_pass: $SU_PASS
EOL

ansible-playbook -i 'localhost,' local.yml
