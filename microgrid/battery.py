from chameleon.simulation.device import Device
from chameleon.simulation.buffer import Buffer
from utils import *

buffer = Buffer()

if __name__ == '__main__':
    utility_grid = Device(name=ENERGY_STORAGE,
                          state=STATE,
                          protocol=ENERGY_STORAGE_PROTOCOL,
                          transitions={})
