from chameleon.simulation.device import Device
from chameleon.simulation.buffer import Buffer
from utils import *

buffer = Buffer()

DIESEL_GENERATOR_POWER = ('DIESEL_GENERATOR_POWER', 1)

islanded = 0

MIN_POWER = 300
MAX_POWER = 800


def toggle_island(self):
    buffer.delay()
    buffer.delay()
    buffer.delay()

    global islanded
    islanded = float(self.receive(DIESEL_GENERATOR_POWER, DIESEL_GENERATOR_ADDR))
    print('DEBUG: {} receive DIESEL_GENERATOR islanded: {}'.format(DIESEL_GENERATOR, islanded))

    buffer.free()


def generator_supply(self):
    global islanded
    buffer.delay()

    demand = float(self.receive(DIESEL_GENERATOR_POWER, DIESEL_GENERATOR_ADDR))
    print('DEBUG: {} was demanded by MICROGRID_CONTROLLER power: {}'.format(DIESEL_GENERATOR, demand))

    power = 0
    if demand == 1:
        print('DEBUG: {} islanded status: {}'.format(DIESEL_GENERATOR, islanded))

        if islanded == 0:
            power = MIN_POWER
        else:
            power = MAX_POWER

    self.set(DIESEL_GENERATOR_POWER, power)
    print('DEBUG: {} set DIESEL_GENERATOR_POWER: {}'.format(DIESEL_GENERATOR, power))

    buffer.free()


if __name__ == '__main__':
    diesel_generator = Device(name=DIESEL_GENERATOR,
                              state=STATE,
                              protocol=DIESEL_GENERATOR_PROTOCOL,
                              actions={
                                  TOGGLE_ISLAND: toggle_island,
                                  GENERATOR_SUPPLY: generator_supply
                              })
