# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "512"
    vb.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ]
  end
  

  config.vm.provision "shell", inline: <<-SHELL
    add-apt-repository ppa:jonathonf/python-3.6
    apt-get -y update
    apt-get -y install python3.6 python3.6-venv
    runuser -l ubuntu -c "python3.6 -m venv ~/venv"
    runuser -l ubuntu -c "source ~/venv/bin/activate; pip install --upgrade pip; pip install -r /vagrant/requirements.txt"
  SHELL
end
