from chameleon.simulation.device import Device
from chameleon.simulation.buffer import Buffer
from utils import *

buffer = Buffer()

ENERGY_STORAGE_POWER = ('ENERGY_STORAGE_POWER', 1)

islanded = 0


def toggle_island(self):
    buffer.delay()
    buffer.delay()

    global islanded
    islanded = float(self.receive(ENERGY_STORAGE_POWER, ENERGY_STORAGE_ADDR))
    print('DEBUG: {} receive ENERGY_STORAGE islanded: {}'.format(ENERGY_STORAGE, islanded))

    buffer.free()


if __name__ == '__main__':
    utility_grid = Device(name=ENERGY_STORAGE,
                          state=STATE,
                          protocol=ENERGY_STORAGE_PROTOCOL,
                          transitions={
                              TOGGLE_ISLAND: toggle_island,
                          })
