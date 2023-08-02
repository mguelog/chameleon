from chameleon.simulation.buffer import Buffer
from chameleon.simulation.state import State
from chameleon.simulation.logger import Logger
from chameleon.simulation.dataset import Dataset
from threading import Thread
import queue

buffer = Buffer()


class Manager:

    def __init__(self, cycle_actions, external_actions, cycles, constraint, control, table):
        self.cycle_actions = cycle_actions
        self.external_actions = external_actions
        self.cycles = cycles
        self.constraint = constraint
        self.control = control
        self.state = State(table)

        self.logger = Logger(self.state)
        self.dataset = Dataset(self.state)
        self.queue = queue.Queue()
        self.running = True

        buffer.create()

    def cycle_loop(self, cycles, collect_cycle, select, custom_cycle):

        self.running = True

        for i in range(cycles):

            if buffer.is_exited():
                break

            while not self.queue.empty():
                while not buffer.is_free():
                    pass

                (external_action, collect_action) = self.queue.get()

                self.logger.log_state(external_action)
                self.logger.log_cycle(external_action)

                if collect_action:
                    self.dataset.store_action(external_action)

                buffer.write(external_action)

                if external_action == buffer.EXIT or external_action == buffer.FAILURE:
                    self.running = False
                    break

            if not self.running:
                break

            cycle_actions = self.cycle_actions

            if custom_cycle is not None:
                cycle_actions = custom_cycle

            for cycle_action in cycle_actions:
                while not buffer.is_free():
                    pass

                self.logger.log_state(cycle_action)
                buffer.write(cycle_action)

            while not buffer.is_free():
                pass

            self.logger.log_cycle(None)

            if collect_cycle:
                self.dataset.store_cycle(select)

            if self.constraint is not None and not self.constraint():
                print('System failure by constraint violation')
                self.queue.put((buffer.FAILURE, False))

        self.running = False

    def run_action(self, action, collect_action):
        self.queue.put((action, collect_action))

    def external_action_input(self):
        while self.running:
            external_actions = set(input('> ').split())
            for external_action in external_actions:
                if external_action in self.external_actions:
                    self.queue.put((external_action, False))
                elif external_action == buffer.EXIT:
                    self.queue.put((buffer.EXIT, False))
                elif self.running:
                    print('Action {} not found'.format(external_action))

    def simulate(self):
        print('Simulation started')

        external_action_thread = Thread(target=self.external_action_input)
        external_action_thread.start()
        self.cycle_loop(self.cycles, False, None, None)

        print('\nSimulation terminated')
        print('Enter for terminate')

        external_action_thread.join()

    def control(self):
        print('Dataset generation started')

        if self.control is not None:
            self.control()

        print('Dataset generation terminated')
