from chameleon.simulation.collection import Collection
from utils import MICROGRID_CONTROLLER, UTILITY_GRID, ENERGY_STORAGE, LOAD_DEMAND, DIESEL_GENERATOR, SOLAR_ARRAY
from manager import manager
from topo import topo

collection = Collection(
    name='microgrid',
    devices=[MICROGRID_CONTROLLER, UTILITY_GRID, ENERGY_STORAGE, LOAD_DEMAND, DIESEL_GENERATOR, SOLAR_ARRAY],
    topo=topo,
    manager=manager)

if __name__ == '__main__':
    collection.start()
