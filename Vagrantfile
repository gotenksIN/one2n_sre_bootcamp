Vagrant.configure("2") do |config|
  config.vm.box = "debian/trixie64"

  config.vm.provider "libvirt" do |lv|
    lv.memory = "2048"
    lv.cpus = 2
  end

  config.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"

  config.vm.provision "shell", path: "vagrant/provision.sh", privileged: true
end
