from chameleon.simulation.device import Device
from chameleon.simulation.buffer import Buffer
from utils import *

buffer = Buffer()

SOLAR_ARRAY_POWER = ('SOLAR_ARRAY_POWER', 1)

TIME = ('TIME', 1)

MAX_POWER = 250
CLOUDY_POWER = 50

max_power = MAX_POWER

RISING_SUN = 25200
FULL_SUN = 36000
FALLING_SUN = 57600
NO_SUN = 68400


def toggle_cloudy(self):
    global max_power

    if max_power == MAX_POWER:
        max_power = CLOUDY_POWER
    elif max_power == CLOUDY_POWER:
        max_power = MAX_POWER

    print('DEBUG: {} set MAX_POWER: {}'.format(SOLAR_ARRAY, max_power))

    buffer.free()


def set_solar_power(self):
    global max_power
    time = self.get(TIME)
    power = 0

    if RISING_SUN <= time < FULL_SUN:
        power = round((time - RISING_SUN) / (FULL_SUN - RISING_SUN) * max_power, 2)
    elif FULL_SUN <= time <= FALLING_SUN:
        power = max_power
    elif FALLING_SUN <= time <= NO_SUN:
        power = round((1 - (time - FALLING_SUN) / (NO_SUN - FALLING_SUN)) * max_power, 2)

    self.set(SOLAR_ARRAY_POWER, power)
    print('DEBUG: {} set SOLAR_ARRAY_POWER: {}'.format(SOLAR_ARRAY, power))

    buffer.free()


if __name__ == '__main__':
    solar_array = Device(name=SOLAR_ARRAY,
                         state=STATE,
                         protocol=SOLAR_ARRAY_PROTOCOL,
                         actions={
                             TOGGLE_CLOUDY: toggle_cloudy,
                             SET_SOLAR_POWER: set_solar_power
                         })
