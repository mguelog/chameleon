from minicps.utils import build_debug_logger

# log
test_logger = build_debug_logger(
    name=__name__,
    bytes_per_file=10000,
    rotating_files=2,
    lformat='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    ldir='logs/',
    suffix='')

# names
CONTROLLER_NAME = 'controller'
TANK_NAME = 'tank'

# protocol
CONTROLLER_MAC = '00:00:00:00:00:01'
CONTROLLER_TAGS = ()
CONTROLLER_ADDR = '10.0.0.1'
CONTROLLER_SERVER = {
    'address': CONTROLLER_ADDR,
    'tags': CONTROLLER_TAGS
}
CONTROLLER_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': CONTROLLER_SERVER
}

TANK_MAC = '00:00:00:00:00:02'
TANK_ADDR = '10.0.0.2'
TANK_TAGS = (
    ('LEVEL', 1, 'INT'),
    ('TEMPERATURE_SENSOR', 1, 'INT'))
TANK_SERVER = {
    'address': TANK_ADDR,
    'tags': TANK_TAGS
}
TANK_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': TANK_SERVER
}

NETMASK = '/24'

# state
PATH = 'tank_db.sqlite'
NAME = 'tank_table'

STATE = {
    'name': NAME,
    'path': PATH
}

SCHEMA = """
CREATE TABLE tank_table (
    pid               INTEGER NOT NULL,
    name              TEXT NOT NULL,
    value             INTEGER NOT NULL,
    PRIMARY KEY (name, pid)
);
"""
INIT_SCHEMA = """
    INSERT INTO tank_table VALUES (1, 'LEVEL', 100);
    INSERT INTO tank_table VALUES (1, 'TEMPERATURE_SENSOR', 25);
"""

# transitions
OPEN_VALVE = 'open_valve'
CHECK_TEMPERATURE = 'check_temperature'
