from chameleon.simulation.device import Device
from chameleon.simulation.buffer import Buffer
from utils import *
import random

buffer = Buffer()

LOAD_DEMAND_POWER = ('LOAD_DEMAND_POWER', 1)

MAX_POWER_INCREASE = 50


def set_load(self):
    power = self.get(LOAD_DEMAND_POWER)
    power_increase = random.uniform(-MAX_POWER_INCREASE, MAX_POWER_INCREASE)

    if power + power_increase < 350:
        power = round(power - power_increase, 2)
    elif power + power_increase > 650:
        power = round(power - power_increase, 2)
    else:
        power = round(power + power_increase, 2)

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
