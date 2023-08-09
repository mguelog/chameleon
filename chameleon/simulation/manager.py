from chameleon.simulation.buffer import Buffer
from chameleon.simulation.state import State
from chameleon.simulation.logger import Logger
from chameleon.simulation.dataset import Dataset
from threading import Thread
import queue

buffer = Buffer()


class Manager:

    def __init__(self, cycle_actions, external_actions, cycles, constraint, hazard_prediction, table, columns, control):
        self.cycle_actions = cycle_actions
        self.external_actions = external_actions
        self.cycles = cycles
        self.constraint = constraint
        self.hazard_prediction = hazard_prediction
        self.state = State(table)
        self.control = control

        self.logger = Logger(self.state, columns)
        self.dataset = Dataset(self.state)
        self.queue = queue.Queue()
        self.running = True

        buffer.create()

    def run_action(self, action, collect_action):
        self.queue.put((action, collect_action))

    def action_queue(self):
        while not self.queue.empty():
            while not buffer.is_free():
                pass

            (external_action, collect_action) = self.queue.get()

            if external_action not in [buffer.FAILURE, buffer.EXIT]:
                if self.hazard_prediction is None:
                    buffer.write(external_action)
                else:
                    if self.hazard_prediction(external_action):
                        buffer.write(external_action)
                    else:
                        return 0

            self.logger.log_state(external_action)
            self.logger.log_cycle(external_action)

            if collect_action:
                self.dataset.store_action(external_action)

            if external_action == buffer.FAILURE:
                self.running = False
                return -1

            if external_action == buffer.EXIT:
                self.running = False
                return 1

        return 0

    def cycle_loop(self, cycles, collect_cycle, select, custom_cycle):

        self.running = True

        for i in range(cycles):

            exit_status = self.action_queue()
            if exit_status != 0:
                return exit_status

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
                self.run_action(buffer.FAILURE, False)
                return self.action_queue()

        self.running = False

        return 0

    def external_action_input(self):
        while self.running:
            external_actions = set(input('> ').split())
            for external_action in external_actions:
                if external_action in self.external_actions or external_action == buffer.EXIT:
                    self.run_action(external_action, False)
                elif self.running:
                    print('Action {} not found'.format(external_action))

    def simulate(self):
        print('\nSimulation started')

        external_action_thread = Thread(target=self.external_action_input)
        external_action_thread.start()
        exit_status = self.cycle_loop(self.cycles, False, None, None)

        if exit_status == 0:
            print('\nSimulation terminated')
        if exit_status == 1:
            print('\nSimulation exited')
        elif exit_status == -1:
            print('\nSimulation terminated by system failure')

        print('Enter for terminate')

        external_action_thread.join()
