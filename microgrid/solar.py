from chameleon.simulation.device import Device
from chameleon.simulation.buffer import Buffer
from utils import *

buffer = Buffer()

SOLAR_ARRAY_POWER = ('SOLAR_ARRAY_POWER', 1)

TIME = ('TIME', 1)

MAX_POWER = 50
RISING_SUN = 25200
FULL_SUN = 36000
FALLING_SUN = 57600
NO_SUN = 68400


def set_solar_power(self):
    time = self.get(TIME)
    power = 0

    if RISING_SUN <= time < FULL_SUN:
        power = round((time - RISING_SUN) / (FULL_SUN - RISING_SUN) * MAX_POWER, 2)
    elif FULL_SUN <= time <= FALLING_SUN:
        power = MAX_POWER
    elif FALLING_SUN <= time <= NO_SUN:
        power = round((1 - (time - FALLING_SUN) / (NO_SUN - FALLING_SUN)) * MAX_POWER, 2)

    self.set(SOLAR_ARRAY_POWER, power)
    print('DEBUG: {} set SOLAR_ARRAY_POWER: {}'.format(SOLAR_ARRAY, power))

    buffer.free()


if __name__ == '__main__':
    solar_array = Device(name=SOLAR_ARRAY,
                         state=STATE,
                         protocol=SOLAR_ARRAY_PROTOCOL,
                         actions={
                             SET_SOLAR_POWER: set_solar_power
                         })
