from chameleon.simulation.device import Device
from chameleon.simulation.buffer import Buffer
from utils import *

buffer = Buffer()

ENERGY_STORAGE_POWER = ('ENERGY_STORAGE_POWER', 1)
ENERGY_STORAGE_VOLTAGE = ('ENERGY_STORAGE_VOLTAGE', 1)
ENERGY_STORAGE_CURRENT = ('ENERGY_STORAGE_CURRENT', 1)

LOAD_DEMAND_POWER = ('LOAD_DEMAND_POWER', 1)

peak_shaved = 1
islanded = 0

MAX_POWER = 1000


def toggle_island(self):
    buffer.delay()
    buffer.delay()

    global islanded
    islanded = float(self.receive(ENERGY_STORAGE_POWER, ENERGY_STORAGE_ADDR))
    print('DEBUG: {} receive ENERGY_STORAGE islanded: {}'.format(ENERGY_STORAGE, islanded))

    buffer.free()


def toggle_peak_shaving(self):
    buffer.delay()

    global peak_shaved
    peak_shaved = float(self.receive(ENERGY_STORAGE_POWER, ENERGY_STORAGE_ADDR))
    print('DEBUG: {} receive ENERGY_STORAGE peak_shaved: {}'.format(ENERGY_STORAGE, peak_shaved))

    buffer.free()


def set_load(self):
    global islanded
    print('DEBUG: {} islanded status: {}'.format(ENERGY_STORAGE, islanded))

    if islanded == 1:
        buffer.delay()

        power = self.get(LOAD_DEMAND_POWER)
        if power > MAX_POWER:
            power = MAX_POWER

        voltage = self.get(ENERGY_STORAGE_VOLTAGE)
        current = round((power * 1000) / voltage, 2)

        self.set(ENERGY_STORAGE_CURRENT, current)
        print('DEBUG: {} set UTILITY_GRID_CURRENT: {}'.format(ENERGY_STORAGE, current))

        self.set(ENERGY_STORAGE_POWER, power)
        print('DEBUG: {} set UTILITY_GRID_POWER: {}'.format(ENERGY_STORAGE, power))

        buffer.free()

    else:
        current = 0
        power = 0

        self.set(ENERGY_STORAGE_CURRENT, current)
        self.set(ENERGY_STORAGE_POWER, power)

        buffer.wait()


if __name__ == '__main__':
    utility_grid = Device(name=ENERGY_STORAGE,
                          state=STATE,
                          protocol=ENERGY_STORAGE_PROTOCOL,
                          transitions={
                              TOGGLE_ISLAND: toggle_island,
                              TOGGLE_PEAK_SHAVING: toggle_peak_shaving,
                              SET_LOAD: set_load,
                          })
