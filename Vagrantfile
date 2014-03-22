# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # Drone supports 12.04 64bit and 13.04 64bit
  config.vm.box = "phusion-open-ubuntu-12.04-amd64"
  config.vm.box_url = "https://oss-binaries.phusionpassenger.com/vagrant/boxes/ubuntu-12.04.3-amd64-vbox.box"

  # Forward keys from SSH agent rather than copypasta
  config.ssh.forward_agent = true

  # FIXME: Maybe this is enough
  config.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--memory", "1024"]
  end

  # Drone by default runs on port 80. Forward from host to guest
  config.vm.network :forwarded_port, guest: 8080, host: 8080
  config.vm.network :private_network, ip: "192.168.10.101"

  # Sync this repo into what will be $GOPATH
  #config.vm.synced_folder ".", "/opt/go/src/github.com/drone/drone"

  # system-level initial setup
  config.vm.provision "shell", inline: <<-EOF
    set -e

    # System packages
    echo "Installing Base Packages"
    export DEBIAN_FRONTEND=noninteractive
    sudo apt-get update -qq
    sudo apt-get install -qqy --force-yes python-software-properties
    sudo add-apt-repository ppa:chris-lea/node.js
    sudo apt-get update -qq
    sudo apt-get install -qqy --force-yes build-essential git python python-dev python-pip nodejs npm

    echo "Install bower"
    sudo npm config set registry http://registry.npmjs.org/
    sudo npm install -g bower

    # Docker
    echo "Install docker"
    curl -s https://get.docker.io/ubuntu/ | sudo sh
    sudo usermod -a -G docker vagrant

    # Install dependencies
    echo "Install python deps"
    sudo pip install -r /vagrant/requirements.txt

    # Cleanup
    sudo apt-get autoremove
  EOF
end
