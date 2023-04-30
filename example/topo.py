from mininet.topo import Topo
from utils import CONTROLLER_NAME, TANK_NAME
from utils import CONTROLLER_MAC, TANK_MAC
from utils import CONTROLLER_ADDR, TANK_ADDR, NETMASK


class TankTopo(Topo):
    def build(self):
        switch = self.addSwitch('s1')

        controller = self.addHost(
            name=CONTROLLER_NAME,
            ip=CONTROLLER_ADDR + NETMASK,
            mac=CONTROLLER_MAC)
        self.addLink(controller, switch)

        tank = self.addHost(
            name=TANK_NAME,
            ip=TANK_ADDR + NETMASK,
            mac=TANK_MAC)
        self.addLink(tank, switch)


topo = TankTopo()
