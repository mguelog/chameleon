from minicps.devices import PLC
from chameleon.simulation.buffer import Buffer

buffer = Buffer()


class Device(PLC):

    def __init__(self, name, protocol, state, transitions):
        self.transitions = transitions
        PLC.__init__(self, name, protocol, state)

    def pre_loop(self, sleep=0):
        print('DEBUG: initializing device')

    def main_loop(self, sleep=0):
        print('DEBUG: executing transitions')

        action = buffer.read()

        while action != buffer.EXIT:

            if action not in [buffer.FREE, buffer.WAIT] and action in self.transitions:
                self.transitions[action](self)

            action = buffer.read()

        print('DEBUG: terminated executing transitions')
