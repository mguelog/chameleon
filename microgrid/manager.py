from chameleon.simulation.manager import Manager
from chameleon.simulation.buffer import Buffer
from utils import *

buffer = Buffer()

cycle = []

manager = Manager(
    transitions={},
    simulation=cycle,
    times=1,
    table=NAME)
