from chameleon.simulation.buffer import Buffer
from chameleon.simulation.state import State
from chameleon.simulation.logger import Logger
from chameleon.simulation.dataset import Dataset
from chameleon.simulation.controller import Controller
from threading import Thread
import queue


class Manager:

    def __init__(self, cycle_actions, external_command_actions, external_stealthy_actions, cycles,
                 constraint, hazard_prediction, anomaly_detection, table, columns, graphic, control):
        self.cycle_actions = cycle_actions
        self.external_command_actions = external_command_actions
        self.external_stealthy_actions = external_stealthy_actions
        self.cycles = cycles
        self.constraint = constraint
        self.hazard_prediction = hazard_prediction
        self.anomaly_detection = anomaly_detection
        self.state = State(table)
        self.graphic = graphic
        self.control = control

        self.buffer = Buffer()
        self.logger = Logger(self.state, columns)
        self.dataset = Dataset(self.state)
        self.controller = Controller(self, table)
        self.queue = queue.Queue()
        self.running = True

        self.status_actions = [self.buffer.EXIT, self.buffer.FAILURE]
        self.buffer.create()

    def run_action(self, action, collect_action):
        self.queue.put((action, collect_action))

    def action_queue(self):
        while not self.queue.empty():
            while not self.buffer.is_free():
                pass

            (external_action, collect_action) = self.queue.get()

            if external_action not in self.status_actions:
                if external_action in self.external_stealthy_actions or self.hazard_prediction is None:
                    self.buffer.write(external_action)
                else:
                    if self.hazard_prediction(self.controller, external_action):
                        self.buffer.write(external_action)
                    else:
                        return 0

            self.logger.log_state(external_action)
            self.logger.log_cycle(external_action)

            if collect_action:
                self.dataset.store_action(external_action)

            if external_action == self.buffer.FAILURE:
                self.running = False
                return -1

            if external_action == self.buffer.EXIT:
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
                while not self.buffer.is_free():
                    pass

                self.logger.log_state(cycle_action)
                self.buffer.write(cycle_action)

            while not self.buffer.is_free():
                pass

            self.logger.log_cycle(None)

            if self.graphic is not None:
                self.graphic.draw()

            if self.anomaly_detection is not None:
                self.logger.log_anomaly(self.anomaly_detection(self.controller))

            if collect_cycle:
                self.dataset.store_cycle(select)

            if self.constraint is not None and not self.constraint(self.controller):
                self.run_action(self.buffer.FAILURE, False)
                return self.action_queue()

        self.running = False

        return 0

    def external_action_input(self):
        while self.running:
            external_actions = set(input('> ').split())
            for external_action in external_actions:
                if external_action in (
                        self.status_actions + self.external_command_actions + self.external_stealthy_actions):
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
