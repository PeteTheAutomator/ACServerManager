#!/usr/bin/bash
# Bootstrap script for the Assetto Corsa Server Manager

sudo sed -i 's/^Defaults\s\+requiretty/Defaults    !requiretty/' /etc/sudoers
sudo yum install -y python-setuptools python-devel policycoreutils-python openssl-devel git gcc
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
