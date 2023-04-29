from chameleon.simulation.buffer import Buffer

buffer = Buffer()


class Manager:

    def __init__(self, transitions, simulation):
        self.transitions = transitions
        self.simulation = simulation
        buffer.create()

    def simulate(self):
        print('Simulation started')

        i = 0
        action = buffer.read()

        while i < len(self.simulation) and action != buffer.EXIT:

            if action == buffer.FREE:
                buffer.write(self.simulation[i])
                i += 1

            action = buffer.read()

        print('Simulation terminated')
