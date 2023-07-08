from chameleon.simulation.simulation import Simulation
from utils import CONTROLLER_NAME, TANK_NAME
from manager import manager
from topo import topo

simulation = Simulation(
    name='tank_cps',
    devices=[CONTROLLER_NAME, TANK_NAME],
    topo=topo,
    manager=manager,
    cli=False,
    wireshark=False)

if __name__ == '__main__':
    simulation.start()
