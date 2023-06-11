from chameleon.simulation.device import Device
from chameleon.simulation.buffer import Buffer
from utils import *

buffer = Buffer()

if __name__ == '__main__':
    load_demand = Device(name=DIESEL_GENERATOR,
                         state=STATE,
                         protocol=DIESEL_GENERATOR_PROTOCOL,
                         transitions={})
