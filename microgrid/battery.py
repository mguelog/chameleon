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

peak_shaved = 1
islanded = 0

MAX_POWER = 1000

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
    power = self.get(ENERGY_STORAGE_POWER)
    energy = self.get(ENERGY_STORAGE_ENERGY)

    energy = round(energy - power * TICK_TIME, 2)

    voltage = round((energy / ENERGY_STORAGE_MAX_ENERGY) * VOLTAGE_RANGE + MIN_VOLTAGE, 2)

    self.set(ENERGY_STORAGE_ENERGY, energy)
    print('DEBUG: {} set ENERGY_STORAGE_ENERGY: {}'.format(ENERGY_STORAGE, energy))

    self.set(ENERGY_STORAGE_VOLTAGE, voltage)
    print('DEBUG: {} set ENERGY_STORAGE_VOLTAGE: {}'.format(ENERGY_STORAGE, voltage))

    buffer.free()


def reload_battery(self):
    energy = self.get(ENERGY_STORAGE_ENERGY)
    power = self.get(ENERGY_STORAGE_POWER)
    solar_power = self.get(SOLAR_ARRAY_POWER)

    solar_energy = solar_power * TICK_TIME
    energy = round(energy + solar_energy * RECHARGING_EFFICIENCY, 2)

    if energy > ENERGY_STORAGE_MAX_ENERGY:
        energy = ENERGY_STORAGE_MAX_ENERGY

    if energy < 0:
        energy = 0

        if power >= solar_power:
            power = solar_power
        else:
            energy = (solar_energy - power) * TICK_TIME

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


if __name__ == '__main__':
    battery_storage = Device(name=ENERGY_STORAGE,
                             state=STATE,
                             protocol=ENERGY_STORAGE_PROTOCOL,
                             actions={
                                 TOGGLE_ISLAND: toggle_island,
                                 TOGGLE_PEAK_SHAVING: toggle_peak_shaving,
                                 SET_LOAD: set_load,
                                 PEAK_SHAVING: peak_shaving,
                                 CONSUME_BATTERY: consume_battery,
                                 RELOAD_BATTERY: reload_battery
                             })
