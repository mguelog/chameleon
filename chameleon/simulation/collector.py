from chameleon.simulation.state import State
from chameleon.simulation.dataset import Dataset


class Collector:

    def __init__(self, manager, table):
        self.state = State(table)
        self.dataset = Dataset(table)
        self.manager = manager

    def set_state(self, updates):
        self.state.set_state(updates)

    def get_values(self, select):
        return self.state.get_values(select)

    def run_cycles(self, cycles, collect_cycle, select):
        self.manager.cycle_loop(cycles, collect_cycle, select)

    def run_action(self, action, collect_action):
        self.manager.run_action(action, collect_action)

    def check_constrain(self, constrain, expected_value):
        self.state.check_constrain(constrain, expected_value)

    def write(self, data):
        self.dataset.store_data(data)

    def new_row(self):
        self.dataset.new_line()
