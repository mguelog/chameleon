from chameleon.simulation.device import Device
from chameleon.simulation.buffer import Buffer
from utils import *

buffer = Buffer()

if __name__ == '__main__':
    microgrid_controller = Device(name=MICROGRID_CONTROLLER,
                                  state=STATE,
                                  protocol=MICROGRID_CONTROLLER_PROTOCOL,
                                  transitions={})
