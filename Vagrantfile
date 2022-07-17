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

            config.vm.provision "file", source: spec, destination: "/tmp/"
            config.vm.provision "file", source: "scripts/env.sh", destination: "/tmp/"

            # shell provisioning
            node.vm.provision "shell" do |shell|
                shell.path = "scripts/setup-vm.sh"
                shell.args = [spec]
                shell.reboot = "true"
            end
            nodes["items"].each do |item|
                node.vm.provision "shell", path: "scripts/#{item}.sh"
            end
        end
    end
end