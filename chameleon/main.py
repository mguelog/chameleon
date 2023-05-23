from chameleon.cli.cli import args
import glob
import subprocess


def main():
    if args.command == 'init':
        if args.overwrite:
            subprocess.run(['rm'] + glob.glob('*.sqlite'))
        try:
            subprocess.run(['python3.10', 'init.py'])
        except FileNotFoundError:
            print('Not init.py found')
    elif args.command == 'simulate':
        if args.log:
            subprocess.run(['rm', 'simulation.log'])
        try:
            subprocess.run(['python3.10', 'run.py'])
        except FileNotFoundError:
            print('Not run.py or manager.py found')


if __name__ == '__main__':
    main()
