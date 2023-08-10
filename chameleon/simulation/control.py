from mininet.net import Mininet
import sys


class Control:

    def __init__(self, name, devices, devices_directory, topo, manager):
        self.name = name
        self.devices = devices
        self.devices_directory = devices_directory,
        self.net = Mininet(topo=topo)
        self.manager = manager

    def start(self):
        self.net.start()

        for device_name in self.devices:
            device = self.net.get(device_name)
            device.cmd(sys.executable + ' -u {}/{}.py &> logs/{}.log &'.format(self.devices_directory,
                                                                               device_name, device_name))

            self.net.pingAll()

            if self.manager is not None:
                self.manager.control()

            self.net.stop()
