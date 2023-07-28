from chameleon import DATASET
import sqlite3
import fnmatch
import os


def get_first(tpl):
    return tpl[0]


class State:

    def __init__(self, table):
        self.table = table
        for file in os.listdir('.'):
            if fnmatch.fnmatch(file, '*.sqlite'):
                self.connection = sqlite3.connect(file)
                self.cursor = self.connection.cursor()
                break

    def get_values(self, select):
        self.cursor.execute(select.format(self.table))
        return list(map(get_first, self.cursor.fetchall()))

    def set_state(self, updates):
        for update in updates:
            self.cursor.execute(update.format(self.table))
            self.connection.commit()

    def check_constrain(self, constrain, expected_value):
        state = self.get_values(constrain.format(self.table))

        with open(DATASET, 'a') as file:
            if state == [expected_value]:
                file.write('0,')
            else:
                file.write('1,')
