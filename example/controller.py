from chameleon.simulation.device import Device
from chameleon.simulation.buffer import Buffer
from utils import CONTROLLER_NAME, CONTROLLER_PROTOCOL
from utils import OPEN_VALVE
from utils import STATE
from utils import TANK_ADDR

buffer = Buffer()
LEVEL = ('LEVEL', 1)
WATER = 10


def open_valve(self):
    self.send(LEVEL, WATER, TANK_ADDR)
    print('DEBUG: controller send LEVEL: {}'.format(WATER))

    buffer.wait()


if __name__ == '__main__':
    controller = Device(name=CONTROLLER_NAME,
                        state=STATE,
                        protocol=CONTROLLER_PROTOCOL,
                        transitions={
                            OPEN_VALVE: open_valve
                        })
