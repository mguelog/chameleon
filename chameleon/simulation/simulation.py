from mininet.net import Mininet
from mininet.cli import CLI
from minicps.mcps import MiniCPS
import sys


class Simulation(MiniCPS):
    def __init__(self, name, devices, topo, manager, cli):
        self.name = name
        self.devices = devices
        self.net = Mininet(topo=topo)
        self.manager = manager
        self.cli = cli

    def start(self):
        self.net.start()

        for device_name in self.devices:
            device = self.net.get(device_name)
            device.cmd(sys.executable + ' -u {}.py &> logs/{}.log &'.format(device_name, device_name))

        if self.manager is not None:
            self.manager.simulate()

        if self.cli or self.manager is None:
            CLI(self.net)

        self.net.stop()
