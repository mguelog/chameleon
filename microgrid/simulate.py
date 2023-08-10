from chameleon.simulation.simulation import Simulation
from utils import MICROGRID_CONTROLLER, UTILITY_GRID, ENERGY_STORAGE, LOAD_DEMAND, DIESEL_GENERATOR, SOLAR_ARRAY
from microgrid.manager.manager import manager
from topo import topo

simulation = Simulation(
    name='microgrid',
    devices=[MICROGRID_CONTROLLER, UTILITY_GRID, ENERGY_STORAGE, LOAD_DEMAND, DIESEL_GENERATOR, SOLAR_ARRAY],
    devices_directory='components',
    topo=topo,
    manager=manager,
    cli=False,
    wireshark=False)

if __name__ == '__main__':
    simulation.start()
