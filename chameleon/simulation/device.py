from minicps.devices import PLC
from chameleon.simulation.buffer import Buffer


class Device(PLC):

    def __init__(self, name, protocol, state, actions):
        self.actions = actions
        self.buffer = Buffer()
        PLC.__init__(self, name, protocol, state)

    def pre_loop(self, sleep=0):
        print('DEBUG: initializing device')

    def main_loop(self, sleep=0):
        print('DEBUG: executing actions')

        action = self.buffer.read()

        while not self.buffer.is_exited():

            if action in self.actions:
                self.actions[action](self)

            action = self.buffer.read()

        print('DEBUG: terminated executing actions')
