import argparse

parser = argparse.ArgumentParser(
    prog='chameleon',
    description='Chameleon Framework'
)

subparsers = parser.add_subparsers(dest='command')

init_parser = subparsers.add_parser(
    'init',
    description='Initialize simulation state by executing init.py',
    help='initialize simulation state by executing init.py'
)
init_parser.add_argument(
    '-o', '--overwrite',
    help='overwrite current state',
    action='store_true'
)

simulate_parser = subparsers.add_parser(
    'simulate',
    description='Run system simulation by executing simulate.py',
    help='run system simulation by executing simulate.py'
)
simulate_parser.add_argument(
    '-l', '--log',
    help='create new log files',
    action='store_true'
)

args = parser.parse_args()
