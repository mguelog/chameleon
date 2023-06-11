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
MICROGRID_CONTROLLER = 'controller'
UTILITY_GRID = 'grid'
ENERGY_STORAGE = 'battery'
LOAD_DEMAND = 'load'
DIESEL_GENERATOR = 'generator'
SOLAR_ARRAY = 'solar'

# protocol
MICROGRID_CONTROLLER_MAC = '00:00:00:00:00:01'
MICROGRID_CONTROLLER_ADDR = '10.0.0.1'
MICROGRID_CONTROLLER_TAGS = (
    ('TIME', 1, 'UINT'),)
MICROGRID_CONTROLLER_SERVER = {
    'address': MICROGRID_CONTROLLER_ADDR,
    'tags': MICROGRID_CONTROLLER_TAGS
}
MICROGRID_CONTROLLER_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': MICROGRID_CONTROLLER_SERVER
}

UTILITY_GRID_MAC = '00:00:00:00:00:02'
UTILITY_GRID_ADDR = '10.0.0.2'
UTILITY_GRID_TAGS = (
    ('UTILITY_GRID_POWER', 1, 'REAL'),
    ('UTILITY_GRID_VOLTAGE', 1, 'REAL'),
    ('UTILITY_GRID_CURRENT', 1, 'REAL'))
UTILITY_GRID_SERVER = {
    'address': UTILITY_GRID_ADDR,
    'tags': UTILITY_GRID_TAGS
}
UTILITY_GRID_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': UTILITY_GRID_SERVER
}

ENERGY_STORAGE_MAC = '00:00:00:00:00:03'
ENERGY_STORAGE_ADDR = '10.0.0.3'
ENERGY_STORAGE_TAGS = (
    ('ENERGY_STORAGE_POWER', 1, 'REAL'),
    ('ENERGY_STORAGE_VOLTAGE', 1, 'REAL'),
    ('ENERGY_STORAGE_CURRENT', 1, 'REAL'))
ENERGY_STORAGE_SERVER = {
    'address': ENERGY_STORAGE_ADDR,
    'tags': ENERGY_STORAGE_TAGS
}
ENERGY_STORAGE_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': ENERGY_STORAGE_SERVER
}

LOAD_DEMAND_MAC = '00:00:00:00:00:04'
LOAD_DEMAND_ADDR = '10.0.0.4'
LOAD_DEMAND_TAGS = (
    ('LOAD_DEMAND_POWER', 1, 'REAL'),)
LOAD_DEMAND_SERVER = {
    'address': LOAD_DEMAND_ADDR,
    'tags': LOAD_DEMAND_TAGS
}
LOAD_DEMAND_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': LOAD_DEMAND_SERVER
}

DIESEL_GENERATOR_MAC = '00:00:00:00:00:05'
DIESEL_GENERATOR_ADDR = '10.0.0.5'
DIESEL_GENERATOR_TAGS = (
)
DIESEL_GENERATOR_SERVER = {
    'address': DIESEL_GENERATOR_ADDR,
    'tags': DIESEL_GENERATOR_TAGS
}
DIESEL_GENERATOR_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': DIESEL_GENERATOR_SERVER
}

SOLAR_ARRAY_MAC = '00:00:00:00:00:06'
SOLAR_ARRAY_ADDR = '10.0.0.6'
SOLAR_ARRAY_TAGS = (
)
SOLAR_ARRAY_SERVER = {
    'address': SOLAR_ARRAY_ADDR,
    'tags': SOLAR_ARRAY_TAGS
}
SOLAR_ARRAY_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': SOLAR_ARRAY_SERVER
}

NETMASK = '/24'

# state
PATH = 'microgrid_db.sqlite'
NAME = 'microgrid_table'

STATE = {
    'name': NAME,
    'path': PATH
}

SCHEMA = """
CREATE TABLE microgrid_table (
    pid               INTEGER NOT NULL,
    name              TEXT NOT NULL,
    value             FLOAT NOT NULL,
    PRIMARY KEY (name, pid)
);
"""
INIT_SCHEMA = """
    INSERT INTO microgrid_table VALUES (1, 'TIME', 0);
    INSERT INTO microgrid_table VALUES (1, 'UTILITY_GRID_POWER', 0);
    INSERT INTO microgrid_table VALUES (1, 'UTILITY_GRID_VOLTAGE', 45000);
    INSERT INTO microgrid_table VALUES (1, 'UTILITY_GRID_CURRENT', 0);
    INSERT INTO microgrid_table VALUES (1, 'ENERGY_STORAGE_POWER', 0);
    INSERT INTO microgrid_table VALUES (1, 'ENERGY_STORAGE_VOLTAGE', 20000);
    INSERT INTO microgrid_table VALUES (1, 'ENERGY_STORAGE_CURRENT', 0);
    INSERT INTO microgrid_table VALUES (1, 'LOAD_DEMAND_POWER', 500);
"""
