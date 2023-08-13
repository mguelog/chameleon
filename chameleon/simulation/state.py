import sqlite3
import fnmatch
import os


def get_first(tpl):
    return tpl[0]


select_all = 'SELECT value FROM {}'


class State:

    def __init__(self, table):
        self.table = table
        for file in os.listdir('.'):
            if fnmatch.fnmatch(file, '*.sqlite'):
                self.connection = sqlite3.connect(file)
                self.cursor = self.connection.cursor()
                break

    def get_values(self, select):
        if select is not None:
            self.cursor.execute(select.format(self.table))
            return list(map(get_first, self.cursor.fetchall()))
        else:
            self.cursor.execute(select_all.format(self.table))
            return list(map(get_first, self.cursor.fetchall()))

    def set_state(self, updates):
        for update in updates:
            self.cursor.execute(update.format(self.table))
            self.connection.commit()
