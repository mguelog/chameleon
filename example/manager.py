from chameleon.simulation.manager import Manager
from utils import OPEN_VALVE, CHECK_TEMPERATURE, NAME

manager = Manager(
    cycle_actions=[
        OPEN_VALVE,
        CHECK_TEMPERATURE],
    external_command_actions=[
        OPEN_VALVE,
        CHECK_TEMPERATURE],
    external_stealthy_actions=[],
    cycles=10,
    constraint=None,
    hazard_prediction=None,
    anomaly_detection=None,
    table=NAME,
    columns='a,lvl,tmp',
    graphic=None,
    control=None
)
