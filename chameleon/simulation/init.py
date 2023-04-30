from minicps.states import SQLiteState
from sqlite3 import OperationalError


class Init:
    def __init__(self, path, schema, init_schema):
        self.path = path
        self.schema = schema
        self.init_schema = init_schema

    def create(self):
        try:
            SQLiteState._create(self.path, self.schema)
            SQLiteState._init(self.path, self.init_schema)
            print('{} successfully created'.format(self.path))
        except OperationalError:
            print('{} already exists'.format(self.path))
