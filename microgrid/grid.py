from chameleon.simulation.device import Device
from chameleon.simulation.buffer import Buffer
from utils import *
import random

buffer = Buffer()

UTILITY_GRID_POWER = ('UTILITY_GRID_POWER', 1)
UTILITY_GRID_VOLTAGE = ('UTILITY_GRID_VOLTAGE', 1)

islanded = 0

NOMINAL_VOLTAGE = 45000
MIN_VOLTAGE = NOMINAL_VOLTAGE - NOMINAL_VOLTAGE * 0.04
MAX_VOLTAGE = NOMINAL_VOLTAGE + NOMINAL_VOLTAGE * 0.04


def toggle_island(self):
    buffer.delay()

    global islanded
    islanded = float(self.receive(UTILITY_GRID_POWER, UTILITY_GRID_ADDR))
    print('DEBUG: {} receive ENERGY_STORAGE islanded: {}'.format(UTILITY_GRID, islanded))

    buffer.wait()


def set_grid_voltage(self):
    voltage = round(random.uniform(MIN_VOLTAGE, MAX_VOLTAGE), 2)
    self.set(UTILITY_GRID_VOLTAGE, voltage)
    print('DEBUG: {} set UTILITY_GRID_VOLTAGE: {}'.format(UTILITY_GRID, voltage))

    buffer.free()


if __name__ == '__main__':
    utility_grid = Device(name=UTILITY_GRID,
                          state=STATE,
                          protocol=UTILITY_GRID_PROTOCOL,
                          transitions={
                              TOGGLE_ISLAND: toggle_island,
                              SET_GRID_VOLTAGE: set_grid_voltage,
                          })
