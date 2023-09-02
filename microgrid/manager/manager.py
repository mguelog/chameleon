from chameleon.simulation.controller import Controller
from chameleon.simulation.manager import Manager
from chameleon.simulation.graphic import Graphic
from microgrid.manager.dataset_generation import *
from microgrid.manager.action_test import *
from microgrid.manager.hazard_detection import *
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

external_command_actions = [
    TOGGLE_ISLAND,
    TOGGLE_PEAK_SHAVING,
    TOGGLE_NIGHT_RELOAD,
    REFUEL_GENERATOR
]

external_stealthy_actions = [
    TOGGLE_CLOUDY,
    TOGGLE_LOAD_PEAK
]


def constraint(controller):
    select = 'SELECT value FROM {} WHERE ' \
             'name LIKE "UTILITY_GRID_POWER" OR ' \
             'name LIKE "ENERGY_STORAGE_POWER" OR ' \
             'name LIKE "LOAD_DEMAND_POWER"'

    [utility_grid_power, energy_storage_power, load_demand_power] = controller.get_values(select)

    return round(utility_grid_power + energy_storage_power, 0) >= round(load_demand_power, 0)


def control_routine():
    controller = Controller(manager, NAME)
    toggle_island_test(controller)


graphic = Graphic('Microgrid', HOURS_COLUMN,
                  [LOAD_DEMAND_POWER_COLUMN, ENERGY_STORAGE_ENERGY_COLUMN, ENERGY_STORAGE_POWER_COLUMN,
                   UTILITY_GRID_POWER_COLUMN, SOLAR_ARRAY_POWER_COLUMN, DIESEL_GENERATOR_FUEL_COLUMN])

manager = Manager(
    cycle_actions=cycle_actions,
    external_command_actions=external_command_actions,
    external_stealthy_actions=external_stealthy_actions,
    cycles=1440,
    constraint=constraint,
    hazard_prediction=action_hazard_prediction,
    anomaly_detection=anomaly_detection,
    table=NAME,
    columns=COLUMNS,
    graphic=graphic,
    control=control_routine)
