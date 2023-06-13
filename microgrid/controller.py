from chameleon.simulation.device import Device
from chameleon.simulation.buffer import Buffer
from utils import *

buffer = Buffer()

TIME = ('TIME', 1)

UTILITY_GRID_POWER = ('UTILITY_GRID_POWER', 1)
ENERGY_STORAGE_POWER = ('ENERGY_STORAGE_POWER', 1)

tick = 1
peak_shaved = 1
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


def toggle_peak_shaving(self):
    global peak_shaved
    if peak_shaved == 1:
        peak_shaved = 0
    else:
        peak_shaved = 1

    self.send(ENERGY_STORAGE_POWER, peak_shaved, ENERGY_STORAGE_ADDR)
    print('DEBUG: {} set ENERGY_STORAGE peak_shaved: {}'.format(MICROGRID_CONTROLLER, peak_shaved))

    buffer.wait()


def peak_shaving(self):
    global peak_shaved
    print('DEBUG: {} peak_shaved status: {}'.format(MICROGRID_CONTROLLER, peak_shaved))

    if peak_shaved == 1:
        utility_grid_power = self.get(UTILITY_GRID_POWER)
        demand = 0
        if utility_grid_power >= UTILITY_GRID_MAX_POWER:
            demand = 1

        self.send(ENERGY_STORAGE_POWER, demand, ENERGY_STORAGE_ADDR)
        print('DEBUG: {} demanded ENERGY_STORAGE power: {}'.format(MICROGRID_CONTROLLER, demand))

    buffer.wait()


if __name__ == '__main__':
    microgrid_controller = Device(name=MICROGRID_CONTROLLER,
                                  state=STATE,
                                  protocol=MICROGRID_CONTROLLER_PROTOCOL,
                                  transitions={
                                      CLOCK_TICK: clock_tick,
                                      TOGGLE_ISLAND: toggle_island,
                                      TOGGLE_PEAK_SHAVING: toggle_peak_shaving,
                                      PEAK_SHAVING: peak_shaving
                                  })
