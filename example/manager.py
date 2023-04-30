from chameleon.simulation.manager import Manager
from chameleon.simulation.buffer import Buffer
from utils import OPEN_VALVE, CHECK_TEMPERATURE

buffer = Buffer()

manager = Manager(
    transitions={OPEN_VALVE, CHECK_TEMPERATURE},
    simulation=[
        OPEN_VALVE,
        CHECK_TEMPERATURE,
        OPEN_VALVE,
        OPEN_VALVE,
        CHECK_TEMPERATURE,
        buffer.EXIT
    ]
)
