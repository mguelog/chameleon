from chameleon.simulation.buffer import Buffer

buffer = Buffer()


class Manager:

    def __init__(self, transitions, simulation, times, table):
        self.transitions = transitions
        self.simulation = simulation
        self.times = times
        self.table = table

        buffer.create()

    def simulate(self):
        print('Simulation started')

        for i in range(self.times):

            j = 0
            action = buffer.read()

            while j < len(self.simulation) and action != buffer.EXIT:

                if action == buffer.FREE:
                    buffer.write(self.simulation[j], self.table)
                    j += 1

                action = buffer.read()

        print('Simulation terminated')
