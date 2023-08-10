from chameleon.simulation.control import Control
from utils import MICROGRID_CONTROLLER, UTILITY_GRID, ENERGY_STORAGE, LOAD_DEMAND, DIESEL_GENERATOR, SOLAR_ARRAY
from microgrid.manager.manager import manager
from topo import topo

control = Control(
    name='microgrid',
    devices=[MICROGRID_CONTROLLER, UTILITY_GRID, ENERGY_STORAGE, LOAD_DEMAND, DIESEL_GENERATOR, SOLAR_ARRAY],
    devices_directory='components',
    topo=topo,
    manager=manager)

if __name__ == '__main__':
    control.start()
