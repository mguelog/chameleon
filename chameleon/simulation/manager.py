from chameleon.simulation.buffer import Buffer
from chameleon.simulation.state import State
from chameleon.simulation.logger import Logger
from threading import Thread
import queue

buffer = Buffer()


class Manager:

    def __init__(self, cycle_actions, external_actions, cycles, table):
        self.cycle_actions = cycle_actions
        self.external_actions = external_actions
        self.cycles = cycles
        self.state = State(table)

        self.logger = Logger(self.state)
        self.queue = queue.Queue()
        self.running = True

        buffer.create()

    def cycle_loop(self, cycles):

        for i in range(cycles):

            if buffer.is_exited():
                break

            while not self.queue.empty():
                while not buffer.is_free():
                    pass

                external_action = self.queue.get()

                self.logger.log_state(external_action)
                self.logger.log_cycle(external_action)

                buffer.write(external_action)

            for cycle_action in self.cycle_actions:
                while not buffer.is_free():
                    pass

                self.logger.log_state(cycle_action)
                buffer.write(cycle_action)

            while not buffer.is_free():
                pass

            self.logger.log_cycle(None)

        self.running = False

    def external_action_input(self):
        while self.running:
            external_actions = set(input('> ').split())
            for external_action in external_actions:
                if external_action in self.external_actions:
                    self.queue.put(external_action)
                elif self.running:
                    print('Action {} not found'.format(external_action))

    def simulate(self):
        print('Simulation started')

        external_action_thread = Thread(target=self.external_action_input)
        external_action_thread.start()
        self.cycle_loop(self.cycles)

        print('\nSimulation terminated')
        print('Enter for terminate')

        external_action_thread.join()
