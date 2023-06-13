from chameleon.simulation.device import Device
from chameleon.simulation.buffer import Buffer
from utils import *

buffer = Buffer()

TIME = ('TIME', 1)

tick = 1


def clock_tick(self):
    time = self.get(TIME)
    time += tick
    self.set(TIME, time)
    print('DEBUG: {} set TIME: {}'.format(MICROGRID_CONTROLLER, time))

    buffer.free()


if __name__ == '__main__':
    microgrid_controller = Device(name=MICROGRID_CONTROLLER,
                                  state=STATE,
                                  protocol=MICROGRID_CONTROLLER_PROTOCOL,
                                  transitions={
                                      CLOCK_TICK: clock_tick
                                  })
