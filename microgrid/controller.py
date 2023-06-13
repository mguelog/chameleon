from chameleon.simulation.device import Device
from chameleon.simulation.buffer import Buffer
from utils import *

buffer = Buffer()

TIME = ('TIME', 1)

UTILITY_GRID_POWER = ('UTILITY_GRID_POWER', 1)
ENERGY_STORAGE_POWER = ('ENERGY_STORAGE_POWER', 1)

tick = 1
islanded = 0


def clock_tick(self):
    time = self.get(TIME)
    time += tick
    self.set(TIME, time)
    print('DEBUG: {} set TIME: {}'.format(MICROGRID_CONTROLLER, time))

    buffer.free()


def toggle_island(self):
    global islanded
    if islanded == 1:
        islanded = 0
    else:
        islanded = 1

    self.send(UTILITY_GRID_POWER, islanded, UTILITY_GRID_ADDR)
    print('DEBUG: {} set UTILITY_GRID islanded: {}'.format(MICROGRID_CONTROLLER, islanded))

    self.send(ENERGY_STORAGE_POWER, islanded, ENERGY_STORAGE_ADDR)
    print('DEBUG: {} set ENERGY_STORAGE islanded: {}'.format(MICROGRID_CONTROLLER, islanded))

    buffer.wait()


if __name__ == '__main__':
    microgrid_controller = Device(name=MICROGRID_CONTROLLER,
                                  state=STATE,
                                  protocol=MICROGRID_CONTROLLER_PROTOCOL,
                                  transitions={
                                      CLOCK_TICK: clock_tick,
                                      TOGGLE_ISLAND: toggle_island,
                                  })
