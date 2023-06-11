from chameleon.simulation.device import Device
from chameleon.simulation.buffer import Buffer
from utils import *

buffer = Buffer()

if __name__ == '__main__':
    load_demand = Device(name=LOAD_DEMAND,
                         state=STATE,
                         protocol=LOAD_DEMAND_PROTOCOL,
                         transitions={})
