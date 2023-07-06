from chameleon.simulation.buffer import Buffer
from chameleon.simulation.logger import Logger
from threading import Thread
import queue

buffer = Buffer()
logger = Logger()


class Manager:

    def __init__(self, cycle_actions, external_actions, cycles, table):
        self.cycle_actions = cycle_actions
        self.external_actions = external_actions
        self.cycles = cycles
        self.table = table

        self.queue = queue.Queue()
        self.running = True

        buffer.create()

    def cycle_loop(self):

        for i in range(self.cycles):

            if buffer.is_exited():
                break

            while not self.queue.empty():
                while not buffer.is_free():
                    pass

                external_action = self.queue.get()

                logger.log_state(external_action, self.table)
                logger.log_cycle(external_action, None)
                buffer.write(external_action)

            for cycle_action in self.cycle_actions:
                while not buffer.is_free():
                    pass

                logger.log_state(cycle_action, self.table)
                buffer.write(cycle_action)

            while not buffer.is_free():
                pass

            logger.log_cycle(None, self.table)

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
        self.cycle_loop()

        print('\nSimulation terminated')
        print('Enter for terminate')

        external_action_thread.join()
