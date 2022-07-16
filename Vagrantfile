VAGRANT_API_VER = "2"

require 'yaml'
spec = 'node-specs.yaml'
nodes = YAML.load_file(spec)

Vagrant.configure(VAGRANT_API_VER) do |config|
    nodes.each do |nodes|
        config.vm.define nodes["name"] do |node|
            node.vm.box = nodes["box"]
            node.vm.network nodes["network"], ip: nodes["ip"]
            node.vbguest.installer_options = { allow_kernel_upgrade: true }

            # VM resource setting
            node.vm.provider :virtualbox do |v|
                v.name = nodes["name"]
                v.memory = nodes["mem"]
                v.cpus = nodes["cpu"]
            end

            config.vm.provision "file" do |file|
                file.source = spec
                file.destination = "/tmp/"
            end

            # shell
            node.vm.provision "shell" do |shell|
                shell.path = "scripts/setup-vm.sh"
                shell.args = [spec]
                shell.reboot = "true"
            end
        end
    end
end