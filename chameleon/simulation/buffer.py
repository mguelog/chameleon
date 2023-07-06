import time


def short_delay():
    time.sleep(0.05)


class Buffer:
    BUFFER = '.buffer'
    FREE = 'free'
    WAIT = 'wait'
    EXIT = 'exit'
    SLEEP = 0.2

    def write(self, action):
        with open(self.BUFFER, 'w') as file:
            file.write(action)

    def free(self):
        short_delay()

        with open(self.BUFFER, 'w') as file:
            file.write(self.FREE)

    def wait(self):
        short_delay()

        if self.read() != self.FREE:
            with open(self.BUFFER, 'w') as file:
                file.write(self.WAIT)

    def create(self):
        self.free()

    def read(self):
        short_delay()

        with open(self.BUFFER, 'r') as file:
            return file.readline()

    def is_free(self):
        return self.read() == self.FREE

    def delay(self):
        time.sleep(self.SLEEP)
