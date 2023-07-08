from chameleon.simulation.device import Device
from chameleon.simulation.buffer import Buffer
from utils import TANK_NAME, TANK_PROTOCOL
from utils import OPEN_VALVE, CHECK_TEMPERATURE
from utils import STATE
from utils import TANK_ADDR
import random

buffer = Buffer()
LEVEL = ('LEVEL', 1)
TEMPERATURE = ('TEMPERATURE_SENSOR', 1)


def open_valve(self):
    buffer.delay()

    water = int(self.receive(LEVEL, TANK_ADDR))
    print('DEBUG: tank receive LEVEL: {}'.format(water))

    level = self.get(LEVEL) + water
    self.set(LEVEL, level)
    print('DEBUG: tank set LEVEL: {}'.format(level))

    buffer.free()


def check_temperature(self):
    temperature = random.randint(-5, 30)

    self.set(TEMPERATURE, temperature)
    print('DEBUG: tank read TEMPERATURE: {}'.format(temperature))
    buffer.free()


if __name__ == '__main__':
    tank = Device(name=TANK_NAME,
                  state=STATE,
                  protocol=TANK_PROTOCOL,
                  actions={
                      OPEN_VALVE: open_valve,
                      CHECK_TEMPERATURE: check_temperature
                  })
