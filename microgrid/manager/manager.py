from chameleon.simulation.controller import Controller
from chameleon.simulation.manager import Manager
from microgrid.manager.dataset_generation import *
from microgrid.utils import *

cycle_actions = [
    CLOCK_TICK,
    SET_GRID_VOLTAGE,
    SET_SOLAR_POWER,
    SET_LOAD,
    PEAK_SHAVING,
    CONSUME_BATTERY,
    GENERATOR_SUPPLY,
    RELOAD_BATTERY,
    NIGHT_RELOAD
]

external_actions = [
    TOGGLE_ISLAND,
    TOGGLE_PEAK_SHAVING,
    TOGGLE_CLOUDY,
    REFUEL_GENERATOR,
    TOGGLE_NIGHT_RELOAD
]


def constraint():
    controller = Controller(manager, NAME)

    select = 'SELECT value FROM {} WHERE ' \
             'name LIKE "UTILITY_GRID_POWER" OR ' \
             'name LIKE "ENERGY_STORAGE_POWER" OR ' \
             'name LIKE "LOAD_DEMAND_POWER"'

    [utility_grid_power, energy_storage_power, load_demand_power] = controller.get_values(select)

    return round(utility_grid_power + energy_storage_power, 0) >= round(load_demand_power, 0)


def control_routine():
    controller = Controller(manager, NAME)
    toggle_island_hazard_prediction_dataset(controller)


manager = Manager(
    cycle_actions=cycle_actions,
    external_actions=external_actions,
    cycles=8,
    constraint=constraint,
    hazard_prediction=None,
    table=NAME,
    columns=COLUMNS,
    control=control_routine)
