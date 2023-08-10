from chameleon.simulation.manager import Manager
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

manager = Manager(
    cycle_actions=cycle_actions,
    external_actions=external_actions,
    cycles=8,
    constraint=None,
    hazard_prediction=None,
    table=NAME,
    columns=COLUMNS,
    control=None)
