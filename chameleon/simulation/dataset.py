from chameleon import DATASET


class Dataset:

    def __init__(self, state):
        self.state = state

    def store_action(self, action):
        with open(DATASET, 'a') as file:
            file.write(action + ',')

    def store_cycle(self, select):
        state = self.state.get_values(select)

        if state is not None:
            with open(DATASET, 'a') as file:
                file.write(str(state)[1:-1] + ',')

    def store_data(self, data):
        with open(DATASET, 'a') as file:
            file.write(data)

    def new_line(self):
        with open(DATASET, 'a') as file:
            file.write('\n')
