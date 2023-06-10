from chameleon.simulation.logger import Logger
import time

logger = Logger()


class Buffer:
    BUFFER = '.buffer'
    FREE = 'free'
    WAIT = 'wait'
    EXIT = 'exit'
    SLEEP = 0.2

    def write(self, action, table):
        logger.log_state(action, table)

        with open(self.BUFFER, 'w') as file:
            file.write(action)

    def free(self):
        self.delay()

        with open(self.BUFFER, 'w') as file:
            file.write(self.FREE)

    def wait(self):
        self.delay()

        with open(self.BUFFER, 'w') as file:
            file.write(self.WAIT)

    def create(self):
        self.free()

    def read(self):
        self.delay()

        with open(self.BUFFER, 'r') as file:
            return file.readline()

    def delay(self):
        time.sleep(self.SLEEP)
