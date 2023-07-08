from chameleon.cli.cli import args
from chameleon import STATE_LOG, CYCLE_LOG
import glob
import subprocess


def main():
    if args.command == 'init':
        if args.overwrite:
            subprocess.run(['sudo', 'rm'] + glob.glob('*.sqlite'))

        try:
            subprocess.run(['python3.10', 'init.py'])
        except FileNotFoundError:
            print('Not init.py found')
    elif args.command == 'simulate':
        if args.log:
            subprocess.run(['sudo', 'rm', STATE_LOG, CYCLE_LOG])

        try:
            subprocess.run(['sudo', 'python3.10', 'simulate.py'])
        except FileNotFoundError:
            print('Not simulate.py found')


if __name__ == '__main__':
    main()
