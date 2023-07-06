from chameleon import STATE_LOG, CYCLE_LOG
import sqlite3
import fnmatch
import os


def get_first(tpl):
    return tpl[0]


select_all = 'SELECT value FROM {}'


class Logger:

    def __init__(self):
        for file in os.listdir('.'):
            if fnmatch.fnmatch(file, '*.sqlite'):
                self.connection = sqlite3.connect(file)
                self.cursor = self.connection.cursor()
                break

    def get_values(self, select, table):
        if table is not None:
            self.cursor.execute(select.format(table))
            return list(map(get_first, self.cursor.fetchall()))
        else:
            return None

    def log_state(self, action, table):
        state = self.get_values(select_all, table)

        if state is not None:
            with open(STATE_LOG, 'a') as file:
                file.write(str(state) + '\n' + action + '\t')

    def log_cycle(self, action, table):
        if action is not None:
            with open(CYCLE_LOG, 'a') as file:
                file.write(action + '\n')
        else:
            state = self.get_values(select_all, table)

            if state is not None:
                with open(CYCLE_LOG, 'a') as file:
                    file.write(str(state) + '\n')
