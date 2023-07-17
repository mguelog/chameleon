from chameleon.cli.cli import args
from chameleon import STATE_LOG, CYCLE_LOG
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
        if args.new:
            subprocess.run(['sudo', 'rm', STATE_LOG, CYCLE_LOG])

        try:
            subprocess.run(['sudo', 'python3.10', 'simulate.py'])
        except FileNotFoundError:
            print('Not simulate.py found')


if __name__ == '__main__':
    main()
