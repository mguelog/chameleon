from chameleon.simulation.init import Init
from utils import PATH, SCHEMA, INIT_SCHEMA

init = Init(
    path=PATH,
    schema=SCHEMA,
    init_schema=INIT_SCHEMA
)

if __name__ == '__main__':
    init.create()
