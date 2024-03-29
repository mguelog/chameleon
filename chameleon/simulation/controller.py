from chameleon.simulation.state import State
from chameleon.simulation.dataset import Dataset


class Controller:

    def __init__(self, manager, table):
        self.state = State(table)
        self.dataset = Dataset(self.state)
        self.manager = manager

    def set_state(self, updates):
        self.state.set_state(updates)

    def get_values(self, select):
        return self.state.get_values(select)

    def run_cycles(self, cycles, collect_cycle, select, custom_cycle):
        return self.manager.cycle_loop(cycles, collect_cycle, select, custom_cycle)

    def run_action(self, action, collect_action):
        self.manager.run_action(action, collect_action)

    def write(self, data):
        self.dataset.store_data(data)

    def new_row(self):
        self.dataset.new_line()
