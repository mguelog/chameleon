from mininet.topo import Topo
from utils import *


class MicrogridTopo(Topo):
    def build(self):
        switch = self.addSwitch('s1')

        microgrid_controller = self.addHost(
            name=MICROGRID_CONTROLLER,
            ip=MICROGRID_CONTROLLER_ADDR + NETMASK,
            mac=MICROGRID_CONTROLLER_MAC)
        self.addLink(microgrid_controller, switch)

        utility_grid = self.addHost(
            name=UTILITY_GRID,
            ip=UTILITY_GRID_ADDR + NETMASK,
            mac=UTILITY_GRID_MAC)
        self.addLink(utility_grid, switch)

        energy_storage = self.addHost(
            name=ENERGY_STORAGE,
            ip=ENERGY_STORAGE_ADDR + NETMASK,
            mac=ENERGY_STORAGE_MAC)
        self.addLink(energy_storage, switch)

        load_demand = self.addHost(
            name=LOAD_DEMAND,
            ip=LOAD_DEMAND_ADDR + NETMASK,
            mac=LOAD_DEMAND_MAC)
        self.addLink(load_demand, switch)

        diesel_generator = self.addHost(
            name=DIESEL_GENERATOR,
            ip=DIESEL_GENERATOR_ADDR + NETMASK,
            mac=DIESEL_GENERATOR_MAC)
        self.addLink(diesel_generator, switch)

        solar_array = self.addHost(
            name=SOLAR_ARRAY,
            ip=SOLAR_ARRAY_ADDR + NETMASK,
            mac=SOLAR_ARRAY_MAC)
        self.addLink(solar_array, switch)


topo = MicrogridTopo()
