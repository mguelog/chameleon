from chameleon.simulation.device import Device
from chameleon.simulation.buffer import Buffer
from microgrid.utils import *
import random

buffer = Buffer()

LOAD_DEMAND_POWER = ('LOAD_DEMAND_POWER', 1)

TIME = ('TIME', 1)

MIN_POWER_DEMAND = 250
BASE_POWER_DEMAND = 500
POWER_VARIATION = 25

APEX_1 = 18000
APEX_2 = 36000
APEX_3 = 50400
APEX_4 = 64800
APEX_5 = 75600
APEX_6 = 86400


def time_demand(time):
    index = 0

    if time < APEX_1:
        index = 0.5 - 0.5 * time / APEX_1
    elif time < APEX_2:
        index = 0.8 * (time - APEX_1) / (APEX_2 - APEX_1)
    elif time < APEX_3:
        index = 0.8 + 0.2 * (time - APEX_2) / (APEX_3 - APEX_2)
    elif time < APEX_4:
        index = 1 - 0.2 * (time - APEX_3) / (APEX_4 - APEX_3)
    elif time < APEX_5:
        index = 0.8 + 0.2 * (time - APEX_4) / (APEX_5 - APEX_4)
    elif time < APEX_6:
        index = 1 - 0.5 * (time - APEX_5) / (APEX_6 - APEX_5)

    return index


def set_load(self):
    time = self.get(TIME)
    power = MIN_POWER_DEMAND + time_demand(time) * BASE_POWER_DEMAND
    power = round(power + random.randint(-POWER_VARIATION, POWER_VARIATION), 2)

    self.set(LOAD_DEMAND_POWER, power)
    print('DEBUG: {} set LOAD_DEMAND_POWER: {}'.format(LOAD_DEMAND, power))

    buffer.wait()


if __name__ == '__main__':
    load_demand = Device(name=LOAD_DEMAND,
                         state=STATE,
                         protocol=LOAD_DEMAND_PROTOCOL,
                         actions={
                             SET_LOAD: set_load
                         })
