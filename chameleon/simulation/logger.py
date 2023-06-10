from chameleon import STATE_LOG
import sqlite3
import fnmatch
import os


def get_first(tuple):
    return tuple[0]


class Logger:
    select = 'SELECT value FROM {}'

    def __init__(self):
        for file in os.listdir('.'):
            if fnmatch.fnmatch(file, '*.sqlite'):
                connection = sqlite3.connect(file)
                self.cursor = connection.cursor()
                break

    def log_state(self, action, table):
        self.cursor.execute(self.select.format(table))
        state = list(map(get_first, self.cursor.fetchall()))

        with open(STATE_LOG, 'a') as file:
            file.write(str(state) + '\n' + action + '\t')
