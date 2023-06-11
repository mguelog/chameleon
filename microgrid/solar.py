from chameleon.simulation.device import Device
from chameleon.simulation.buffer import Buffer
from utils import *

buffer = Buffer()

if __name__ == '__main__':
    load_demand = Device(name=SOLAR_ARRAY,
                         state=STATE,
                         protocol=SOLAR_ARRAY_PROTOCOL,
                         transitions={})
