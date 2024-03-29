from chameleon.simulation.device import Device
from chameleon.simulation.buffer import Buffer
from microgrid.utils import *
import random

buffer = Buffer()

UTILITY_GRID_POWER = ('UTILITY_GRID_POWER', 1)
UTILITY_GRID_VOLTAGE = ('UTILITY_GRID_VOLTAGE', 1)
UTILITY_GRID_CURRENT = ('UTILITY_GRID_CURRENT', 1)

LOAD_DEMAND_POWER = ('LOAD_DEMAND_POWER', 1)
TIME = ('TIME', 1)
ENERGY_STORAGE_ENERGY = ('ENERGY_STORAGE_ENERGY', 1)

islanded = 0
night_reloaded = 1

NOMINAL_VOLTAGE = 45000
MIN_VOLTAGE = NOMINAL_VOLTAGE - NOMINAL_VOLTAGE * 0.04
MAX_VOLTAGE = NOMINAL_VOLTAGE + NOMINAL_VOLTAGE * 0.04


def toggle_island(self):
    buffer.delay()

    global islanded
    islanded = float(self.receive(UTILITY_GRID_POWER, UTILITY_GRID_ADDR))
    print('DEBUG: {} receive UTILITY_GRID islanded: {}'.format(UTILITY_GRID, islanded))

    buffer.wait()


def toggle_night_reload(self):
    buffer.delay()

    global night_reloaded
    night_reloaded = float(self.receive(UTILITY_GRID_POWER, UTILITY_GRID_ADDR))
    print('DEBUG: {} receive UTILITY_GRID night_reloaded: {}'.format(UTILITY_GRID, night_reloaded))

    buffer.wait()


def set_grid_voltage(self):
    voltage = round(random.uniform(MIN_VOLTAGE, MAX_VOLTAGE), 2)
    self.set(UTILITY_GRID_VOLTAGE, voltage)
    print('DEBUG: {} set UTILITY_GRID_VOLTAGE: {}'.format(UTILITY_GRID, voltage))

    buffer.free()


def set_load(self):
    global islanded
    print('DEBUG: {} islanded status: {}'.format(UTILITY_GRID, islanded))

    if islanded == 0:
        buffer.delay()

        power = self.get(LOAD_DEMAND_POWER)
        if power > UTILITY_GRID_MAX_POWER:
            power = UTILITY_GRID_MAX_POWER

        voltage = self.get(UTILITY_GRID_VOLTAGE)
        current = round((power * 1000) / voltage, 2)

        self.set(UTILITY_GRID_CURRENT, current)
        print('DEBUG: {} set UTILITY_GRID_CURRENT: {}'.format(UTILITY_GRID, current))

        self.set(UTILITY_GRID_POWER, power)
        print('DEBUG: {} set UTILITY_GRID_POWER: {}'.format(UTILITY_GRID, power))

        buffer.free()

    else:
        current = 0
        power = 0

        self.set(UTILITY_GRID_CURRENT, current)
        self.set(UTILITY_GRID_POWER, power)

        buffer.wait()


def night_reload(self):
    buffer.delay()

    global islanded, night_reloaded
    print('DEBUG: {} islanded status: {}'.format(UTILITY_GRID, islanded))
    print('DEBUG: {} night_reloaded status: {}'.format(UTILITY_GRID, night_reloaded))

    if night_reloaded == 1:
        reload = float(self.receive(UTILITY_GRID_POWER, UTILITY_GRID_ADDR))
        print('DEBUG: {} was demanded by MICROGRID_CONTROLLER reload: {}'.format(UTILITY_GRID, reload))

        if reload == 1:
            power = UTILITY_GRID_MAX_POWER
            voltage = self.get(UTILITY_GRID_VOLTAGE)
            current = round((power * 1000) / voltage, 2)

            self.set(UTILITY_GRID_CURRENT, current)
            print('DEBUG: {} set UTILITY_GRID_CURRENT: {}'.format(UTILITY_GRID, current))

            self.set(UTILITY_GRID_POWER, power)
            print('DEBUG: {} set UTILITY_GRID_POWER: {}'.format(UTILITY_GRID, power))

    buffer.wait()


if __name__ == '__main__':
    utility_grid = Device(name=UTILITY_GRID,
                          state=STATE,
                          protocol=UTILITY_GRID_PROTOCOL,
                          actions={
                              TOGGLE_ISLAND: toggle_island,
                              TOGGLE_NIGHT_RELOAD: toggle_night_reload,
                              SET_GRID_VOLTAGE: set_grid_voltage,
                              SET_LOAD: set_load,
                              NIGHT_RELOAD: night_reload
                          })
