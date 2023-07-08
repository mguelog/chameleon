from chameleon.simulation.manager import Manager
from chameleon.simulation.buffer import Buffer
from utils import OPEN_VALVE, CHECK_TEMPERATURE, NAME

buffer = Buffer()

manager = Manager(
    cycle_actions=[
        OPEN_VALVE,
        CHECK_TEMPERATURE,
        OPEN_VALVE,
        OPEN_VALVE,
        CHECK_TEMPERATURE,
        buffer.EXIT],
    external_actions={OPEN_VALVE, CHECK_TEMPERATURE},
    cycles=1,
    table=NAME
)
