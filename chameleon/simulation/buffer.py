import time


def short_delay():
    time.sleep(0.01)


class Buffer:
    BUFFER = '.buffer'
    FREE = 'free'
    WAIT = 'wait'
    EXIT = 'exit'
    FAILURE = 'failure'
    SLEEP = 0.3

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
        return self.read() in (self.FREE, self.EXIT)

    def is_exited(self):
        return self.read() == self.EXIT

    def delay(self):
        time.sleep(self.SLEEP)
