from minicps.devices import PLC
from chameleon.simulation.buffer import Buffer

buffer = Buffer()


class Device(PLC):

    def __init__(self, name, protocol, state, actions):
        self.actions = actions
        PLC.__init__(self, name, protocol, state)

    def pre_loop(self, sleep=0):
        print('DEBUG: initializing device')

    def main_loop(self, sleep=0):
        print('DEBUG: executing transitions')

        action = buffer.read()

        while not buffer.is_exited():

            if action not in [buffer.FREE, buffer.WAIT] and action in self.actions:
                self.actions[action](self)

            action = buffer.read()

        print('DEBUG: terminated executing transitions')
