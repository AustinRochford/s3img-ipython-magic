Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network :forwarded_port, host: 8888, guest: 8888
  config.vm.provision :shell, path: "provision.sh"
end
