import time


class Buffer:
    BUFFER = '.buffer'
    FREE = 'free'
    WAIT = 'wait'
    EXIT = 'exit'
    SLEEP = 0.05

    def write(self, action):
        with open(self.BUFFER, 'w') as file:
            file.write(action)

    def free(self):
        self.delay()
        self.write(self.FREE)

    def wait(self):
        self.delay()
        self.write(self.WAIT)

    def create(self):
        self.free()

    def read(self):
        self.delay()
        with open(self.BUFFER, 'r') as file:
            return file.readline()

    def delay(self):
        time.sleep(self.SLEEP)
