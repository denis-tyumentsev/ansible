#!/usr/bin/env bash

user='ansible'
uid='15777'
key='ssh-rsa ... ansible@uds-deploy.moscow.eurochem.ru'

if $(id "$user" >/dev/null 2>&1); then
  echo "Error! User $user is already exists!" && exit 1
fi

sudo useradd $user -u $uid
sudo usermod -aG wheel $user
echo 'ieNgieLohfeineenain8' | sudo passwd --stdin $user

sudo mkdir -m 700 /home/$user/.ssh && sudo sh -c "echo $key > /home/$user/.ssh/authorized_keys"

sudo chmod 600 /home/$user/.ssh/authorized_keys 
sudo chown $user:$user -R /home/$user/.ssh

