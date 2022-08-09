require 'yaml'

VAGRANT_API_VER = "2"
SPEC_FILE = 'node-specs.yml'

NODES = YAML.load_file(SPEC_FILE)

Vagrant.configure(VAGRANT_API_VER) do |config|
    NODES.each do |node_spec|
        config.vm.define node_spec["name"] do |node|
            node.vm.box = node_spec["box"]
            node.vm.network node_spec["network"], ip: node_spec["ip"]
            node.vbguest.installer_options = { allow_kernel_upgrade: true }

            # VM resource setting
            node.vm.provider :virtualbox do |v|
                v.name = node_spec["name"]
                v.memory = node_spec["mem"] * 1024
                v.cpus = node_spec["cpu"]
            end
            node.vm.disk :disk, size: "#{node_spec["disk"]}GB", primary: true

            # move local file to vm
            config.vm.provision "file", source: SPEC_FILE, destination: "/tmp/"
            config.vm.provision "file", source: "scripts/env.sh", destination: "/tmp/"

            # shell provisioning
            node.vm.provision "shell", path: "scripts/increase-disk.sh"
            node.vm.provision "shell" do |shell|
                shell.path = "scripts/setup-vm.sh"
                shell.args = [node_spec["name"]]
                shell.reboot = "true"
            end
            if node_spec.include?("scripts") && node_spec["scripts"].kind_of?(Array)
                node_spec["scripts"].each do |script|
                    node.vm.provision "shell", path: "scripts/#{script}.sh"
                end
            end
        end
    end
end