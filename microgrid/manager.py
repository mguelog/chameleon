from chameleon.simulation.manager import Manager
from chameleon.simulation.buffer import Buffer
from utils import *

buffer = Buffer()

cycle = []

manager = Manager(
    cycle_actions=cycle,
    external_actions={},
    cycles=1,
    table=NAME)
