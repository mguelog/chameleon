from mininet.net import Mininet
from mininet.cli import CLI
import sys


class Simulation:
    def __init__(self, name, devices, topo, manager, cli, wireshark):
        self.name = name
        self.devices = devices
        self.net = Mininet(topo=topo)
        self.manager = manager
        self.cli = cli
        self.wireshark = wireshark

    def start(self):
        self.net.start()

        for device_name in self.devices:
            device = self.net.get(device_name)
            device.cmd(sys.executable + ' -u {}.py &> logs/{}.log &'.format(device_name, device_name))

        self.net.pingAll()

        if self.wireshark:
            CLI.do_sh(self.net, line=['wireshark &> logs/wireshark.log &'])
        elif self.cli or self.manager is None:
            CLI(self.net)

        if self.manager is not None:
            self.manager.simulate()

        self.net.stop()
