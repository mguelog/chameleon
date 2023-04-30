import argparse

parser = argparse.ArgumentParser(
    prog='chameleon',
    description='Chameleon Framework'
)

subparsers = parser.add_subparsers(dest='command')

init_parser = subparsers.add_parser(
    'init',
    description='Initialize simulation state',
    help='initialize simulation state'
)
init_parser.add_argument(
    '-o', '--overwrite',
    help='overwrite current state',
    action='store_true'
)

args = parser.parse_args()
