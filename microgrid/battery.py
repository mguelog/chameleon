from chameleon.simulation.device import Device
from chameleon.simulation.buffer import Buffer
from utils import *

buffer = Buffer()

ENERGY_STORAGE_POWER = ('ENERGY_STORAGE_POWER', 1)
ENERGY_STORAGE_VOLTAGE = ('ENERGY_STORAGE_VOLTAGE', 1)
ENERGY_STORAGE_CURRENT = ('ENERGY_STORAGE_CURRENT', 1)
ENERGY_STORAGE_ENERGY = ('ENERGY_STORAGE_ENERGY', 1)

LOAD_DEMAND_POWER = ('LOAD_DEMAND_POWER', 1)
SOLAR_ARRAY_POWER = ('SOLAR_ARRAY_POWER', 1)
DIESEL_GENERATOR_POWER = ('DIESEL_GENERATOR_POWER', 1)
UTILITY_GRID_POWER = ('UTILITY_GRID_POWER', 1)
TIME = ('TIME', 1)

peak_shaved = 1
islanded = 0
night_reloaded = 1

MAX_POWER = 800

NOMINAL_VOLTAGE = 5000
MIN_VOLTAGE = NOMINAL_VOLTAGE - NOMINAL_VOLTAGE * 0.3
MAX_VOLTAGE = NOMINAL_VOLTAGE + NOMINAL_VOLTAGE * 0.3
VOLTAGE_RANGE = MAX_VOLTAGE - MIN_VOLTAGE

RECHARGING_EFFICIENCY = 1


def toggle_island(self):
    buffer.delay()
    buffer.delay()

    global islanded
    islanded = float(self.receive(ENERGY_STORAGE_POWER, ENERGY_STORAGE_ADDR))
    print('DEBUG: {} receive ENERGY_STORAGE islanded: {}'.format(ENERGY_STORAGE, islanded))

    buffer.wait()


def toggle_peak_shaving(self):
    buffer.delay()

    global peak_shaved
    peak_shaved = float(self.receive(ENERGY_STORAGE_POWER, ENERGY_STORAGE_ADDR))
    print('DEBUG: {} receive ENERGY_STORAGE peak_shaved: {}'.format(ENERGY_STORAGE, peak_shaved))

    buffer.free()


def toggle_night_reload(self):
    buffer.delay()
    buffer.delay()

    global night_reloaded
    night_reloaded = float(self.receive(ENERGY_STORAGE_POWER, ENERGY_STORAGE_ADDR))
    print('DEBUG: {} receive ENERGY_STORAGE night_reloaded: {}'.format(ENERGY_STORAGE, night_reloaded))

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
        print('DEBUG: {} set ENERGY_STORAGE_CURRENT: {}'.format(ENERGY_STORAGE, current))

        self.set(ENERGY_STORAGE_POWER, power)
        print('DEBUG: {} set ENERGY_STORAGE_POWER: {}'.format(ENERGY_STORAGE, power))

        buffer.free()

    else:
        current = 0
        power = 0

        self.set(ENERGY_STORAGE_CURRENT, current)
        self.set(ENERGY_STORAGE_POWER, power)

        buffer.wait()


def peak_shaving(self):
    global peak_shaved
    print('DEBUG: {} peak_shaved status: {}'.format(ENERGY_STORAGE, peak_shaved))

    buffer.delay()

    if peak_shaved == 1:
        demand = float(self.receive(ENERGY_STORAGE_POWER, ENERGY_STORAGE_ADDR))
        print('DEBUG: {} was demanded by MICROGRID_CONTROLLER power: {}'.format(ENERGY_STORAGE, demand))

        if demand == 1:
            power = self.get(LOAD_DEMAND_POWER)
            power = round(power - UTILITY_GRID_MAX_POWER, 2)

            voltage = self.get(ENERGY_STORAGE_VOLTAGE)
            current = round((power * 1000) / voltage, 2)

            self.set(ENERGY_STORAGE_CURRENT, current)
            print('DEBUG: {} set ENERGY_STORAGE_CURRENT: {}'.format(ENERGY_STORAGE, current))

            self.set(ENERGY_STORAGE_POWER, power)
            print('DEBUG: {} set ENERGY_STORAGE_POWER: {}'.format(ENERGY_STORAGE, power))

    buffer.free()


def consume_battery(self):
    energy = self.get(ENERGY_STORAGE_ENERGY)
    power = self.get(ENERGY_STORAGE_POWER)
    solar_array_power = self.get(SOLAR_ARRAY_POWER)

    consumed_energy = (solar_array_power * RECHARGING_EFFICIENCY - power) * DELTA_TIME
    energy = round(energy + consumed_energy, 2)

    voltage = round((energy / ENERGY_STORAGE_MAX_ENERGY) * VOLTAGE_RANGE + MIN_VOLTAGE, 2)

    self.set(ENERGY_STORAGE_ENERGY, energy)
    print('DEBUG: {} set ENERGY_STORAGE_ENERGY: {}'.format(ENERGY_STORAGE, energy))

    self.set(ENERGY_STORAGE_VOLTAGE, voltage)
    print('DEBUG: {} set ENERGY_STORAGE_VOLTAGE: {}'.format(ENERGY_STORAGE, voltage))

    buffer.free()


def reload_battery(self):
    energy = self.get(ENERGY_STORAGE_ENERGY)
    power = self.get(ENERGY_STORAGE_POWER)
    diesel_generator_power = self.get(DIESEL_GENERATOR_POWER)

    diesel_generator_energy = diesel_generator_power * DELTA_TIME

    energy = round(energy + diesel_generator_energy * RECHARGING_EFFICIENCY, 2)

    if energy > ENERGY_STORAGE_MAX_ENERGY:
        energy = ENERGY_STORAGE_MAX_ENERGY

    if energy < 0:
        solar_array_power = self.get(SOLAR_ARRAY_POWER)
        reload_power = round(diesel_generator_power + solar_array_power, 2)

        energy = 0
        power = reload_power

        self.set(ENERGY_STORAGE_POWER, power)
        print('DEBUG: {} set ENERGY_STORAGE_POWER: {}'.format(ENERGY_STORAGE, power))

    voltage = round((energy / ENERGY_STORAGE_MAX_ENERGY) * VOLTAGE_RANGE + MIN_VOLTAGE, 2)
    current = round((power * 1000) / voltage, 2)

    self.set(ENERGY_STORAGE_ENERGY, energy)
    print('DEBUG: {} set ENERGY_STORAGE_ENERGY: {}'.format(ENERGY_STORAGE, energy))

    self.set(ENERGY_STORAGE_VOLTAGE, voltage)
    print('DEBUG: {} set ENERGY_STORAGE_VOLTAGE: {}'.format(ENERGY_STORAGE, voltage))

    self.set(ENERGY_STORAGE_CURRENT, current)
    print('DEBUG: {} set ENERGY_STORAGE_CURRENT: {}'.format(ENERGY_STORAGE, current))

    buffer.free()


def night_reload(self):
    buffer.delay()
    buffer.delay()
    buffer.delay()

    global islanded, night_reloaded
    print('DEBUG: {} islanded status: {}'.format(ENERGY_STORAGE, islanded))
    print('DEBUG: {} night_reloaded status: {}'.format(ENERGY_STORAGE, night_reloaded))

    if night_reloaded == 1:
        energy = self.get(ENERGY_STORAGE_ENERGY)
        power = self.get(ENERGY_STORAGE_POWER)
        utility_gird_power = self.get(UTILITY_GRID_POWER)
        load_demand_power = self.get(LOAD_DEMAND_POWER)
        reload_energy = 0

        if load_demand_power < utility_gird_power:
            reload_power = utility_gird_power - load_demand_power
            reload_energy = reload_power * DELTA_TIME

        energy = round(energy + reload_energy, 2)
        voltage = round((energy / ENERGY_STORAGE_MAX_ENERGY) * VOLTAGE_RANGE + MIN_VOLTAGE, 2)
        current = round((power * 1000) / voltage, 2)

        self.set(ENERGY_STORAGE_ENERGY, energy)
        print('DEBUG: {} set ENERGY_STORAGE_ENERGY: {}'.format(ENERGY_STORAGE, energy))

        self.set(ENERGY_STORAGE_VOLTAGE, voltage)
        print('DEBUG: {} set ENERGY_STORAGE_VOLTAGE: {}'.format(ENERGY_STORAGE, voltage))

        self.set(ENERGY_STORAGE_CURRENT, current)
        print('DEBUG: {} set ENERGY_STORAGE_CURRENT: {}'.format(ENERGY_STORAGE, current))

    buffer.free()


if __name__ == '__main__':
    battery_storage = Device(name=ENERGY_STORAGE,
                             state=STATE,
                             protocol=ENERGY_STORAGE_PROTOCOL,
                             actions={
                                 TOGGLE_ISLAND: toggle_island,
                                 TOGGLE_PEAK_SHAVING: toggle_peak_shaving,
                                 TOGGLE_NIGHT_RELOAD: toggle_night_reload,
                                 SET_LOAD: set_load,
                                 PEAK_SHAVING: peak_shaving,
                                 CONSUME_BATTERY: consume_battery,
                                 RELOAD_BATTERY: reload_battery,
                                 NIGHT_RELOAD: night_reload
                             })
