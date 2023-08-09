from chameleon import STATE_LOG, CYCLE_LOG
import os.path

select_all = 'SELECT value FROM {}'


class Logger:

    def __init__(self, state, columns):
        self.state = state

        if not os.path.isfile(CYCLE_LOG):
            with open(CYCLE_LOG, 'a') as file:
                file.write(columns + '\n')

    def log_state(self, action):
        values = self.state.get_values(select_all)

        if values is not None:
            with open(STATE_LOG, 'a') as file:
                file.write(str(values) + '\n' + action + '\t')

    def log_cycle(self, action):
        if action is not None:
            with open(CYCLE_LOG, 'a') as file:
                file.write(action + '\n')
        else:
            values = self.state.get_values(select_all)

            if values is not None:
                with open(CYCLE_LOG, 'a') as file:
                    file.write(',' + str(values)[1:-1] + '\n')
