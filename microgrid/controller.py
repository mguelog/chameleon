from chameleon.simulation.device import Device
from chameleon.simulation.buffer import Buffer
from utils import *

buffer = Buffer()

TIME = ('TIME', 1)
HOURS = ('HOURS', 1)

LOAD_DEMAND_POWER = ('LOAD_DEMAND_POWER', 1)
UTILITY_GRID_POWER = ('UTILITY_GRID_POWER', 1)
ENERGY_STORAGE_POWER = ('ENERGY_STORAGE_POWER', 1)
DIESEL_GENERATOR_POWER = ('DIESEL_GENERATOR_POWER', 1)
ENERGY_STORAGE_ENERGY = ('ENERGY_STORAGE_ENERGY', 1)

tick_time = SECONDS_PER_TICK
max_time = SECONDS_A_DAY
peak_shaved = 1
islanded = 0
night_reloaded = 1


def clock_tick(self):
    time = self.get(TIME)
    hours = self.get(HOURS)

    time += tick_time
    hours = round(hours + tick_time / 3600, 4)

    if time >= max_time:
        time = 0

    self.set(TIME, time)
    print('DEBUG: {} set TIME: {}'.format(MICROGRID_CONTROLLER, time))

    self.set(HOURS, hours)
    print('DEBUG: {} set HOURS: {}'.format(MICROGRID_CONTROLLER, hours))

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

    self.send(DIESEL_GENERATOR_POWER, islanded, DIESEL_GENERATOR_ADDR)
    print('DEBUG: {} set DIESEL_GENERATOR islanded: {}'.format(MICROGRID_CONTROLLER, islanded))

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


def toggle_night_reload(self):
    global night_reloaded
    if night_reloaded == 1:
        night_reloaded = 0
    else:
        night_reloaded = 1

    self.send(UTILITY_GRID_POWER, night_reloaded, UTILITY_GRID_ADDR)
    print('DEBUG: {} set UTILITY_GRID night_reloaded: {}'.format(MICROGRID_CONTROLLER, night_reloaded))

    self.send(ENERGY_STORAGE_POWER, night_reloaded, ENERGY_STORAGE_ADDR)
    print('DEBUG: {} set ENERGY_STORAGE night_reloaded: {}'.format(MICROGRID_CONTROLLER, night_reloaded))

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


def generator_supply(self):
    energy_storage_energy = self.get(ENERGY_STORAGE_ENERGY)
    demand = 0

    if energy_storage_energy < 0:
        demand = 1

    self.send(DIESEL_GENERATOR_POWER, demand, DIESEL_GENERATOR_ADDR)
    print('DEBUG: {} demanded DIESEL_GENERATOR power: {}'.format(MICROGRID_CONTROLLER, demand))

    buffer.wait()


def night_reload(self):
    global islanded, night_reloaded
    print('DEBUG: {} islanded status: {}'.format(MICROGRID_CONTROLLER, islanded))
    print('DEBUG: {} night_reloaded status: {}'.format(MICROGRID_CONTROLLER, night_reloaded))

    if night_reloaded == 1:
        time = self.get(TIME)
        energy_storage_energy = self.get(ENERGY_STORAGE_ENERGY)
        utility_grid_power = self.get(UTILITY_GRID_POWER)
        reload = 0

        if START_NIGHT_RELOAD <= time <= END_NIGHT_RELOAD and energy_storage_energy < MAX_RELOAD_ENERGY:
            if islanded == 0 and utility_grid_power < UTILITY_GRID_MAX_POWER:
                reload = 1

        self.send(UTILITY_GRID_POWER, reload, UTILITY_GRID_ADDR)
        print('DEBUG: {} demanded UTILITY_GRID reload: {}'.format(MICROGRID_CONTROLLER, reload))

    buffer.wait()


if __name__ == '__main__':
    microgrid_controller = Device(name=MICROGRID_CONTROLLER,
                                  state=STATE,
                                  protocol=MICROGRID_CONTROLLER_PROTOCOL,
                                  actions={
                                      CLOCK_TICK: clock_tick,
                                      TOGGLE_ISLAND: toggle_island,
                                      TOGGLE_PEAK_SHAVING: toggle_peak_shaving,
                                      TOGGLE_NIGHT_RELOAD: toggle_night_reload,
                                      PEAK_SHAVING: peak_shaving,
                                      GENERATOR_SUPPLY: generator_supply,
                                      NIGHT_RELOAD: night_reload
                                  })
