from chameleon.cli.cli import args
from chameleon import STATE_LOG, CYCLE_LOG, DATASET
import glob
import subprocess
import os


def main():
    if args.command == 'init':
        if args.overwrite:
            for file in glob.glob('*.sqlite'):
                os.remove(file)

        stderr = subprocess.Popen(['python3.10', 'init.py'],
                                  stderr=subprocess.PIPE).communicate()[1]
        if stderr != b'':
            print('Not init.py found')

    elif args.command == 'simulate':
        if args.log:
            try:
                os.remove(STATE_LOG)
                os.remove(CYCLE_LOG)
            except FileNotFoundError:
                print('Not previous log files found')

        subprocess.run(['sudo', 'python3.10', 'simulate.py'])

    elif args.command == 'collect':
        if args.log:
            try:
                os.remove(STATE_LOG)
                os.remove(CYCLE_LOG)
            except FileNotFoundError:
                print('Not previous log files found')
        if args.new:
            try:
                os.remove(DATASET)
            except FileNotFoundError:
                print('Not previous data files found')

        subprocess.run(['sudo', 'python3.10', 'collect.py'])


if __name__ == '__main__':
    main()
