from microgrid.utils import *
import random


def toggle_island_test(controller):
    controller.write('h,t,ugp,ugv,ugc,esp,esv,esc,ese,sap,dgp,dgf,ldp,a,class\n')

    for i in range(1000):
        time = random.randint(0, SECONDS_A_DAY - 1)
        energy = random.randint(0, 25)
        fuel = random.randint(0, 25)

        updates = ['UPDATE {} SET value = {} WHERE name LIKE "TIME"'.format({}, time),
                   'UPDATE {} SET value = {} WHERE name LIKE "ENERGY_STORAGE_ENERGY"'.format({}, energy),
                   'UPDATE {} SET value = {} WHERE name LIKE "DIESEL_GENERATOR_FUEL"'.format({}, fuel)]

        controller.set_state(updates)

        if random.randint(0, 1) == 1:
            controller.run_action(TOGGLE_CLOUDY, False)

        controller.run_cycles(1, True, None, None)
        controller.run_action(TOGGLE_ISLAND, True)

        actual = 1 if controller.run_cycles(1, False, None, None) == 0 else 0
        controller.write('{}'.format(actual))

        controller.run_action(TOGGLE_ISLAND, False)
        controller.run_cycles(1, False, None, None)
        controller.new_row()


def toggle_night_reload_test(controller):
    controller.write('h,t,ugp,ugv,ugc,esp,esv,esc,ese,sap,dgp,dgf,ldp,a,class\n')

    for i in range(1000):
        time = random.randint(0, SECONDS_A_DAY - 1)
        energy = random.randint(0, 50)
        fuel = random.randint(0, 100)

        updates = ['UPDATE {} SET value = {} WHERE name LIKE "TIME"'.format({}, time),
                   'UPDATE {} SET value = {} WHERE name LIKE "ENERGY_STORAGE_ENERGY"'.format({}, energy),
                   'UPDATE {} SET value = {} WHERE name LIKE "DIESEL_GENERATOR_FUEL"'.format({}, fuel)]

        controller.set_state(updates)

        if random.randint(0, 1) == 1:
            controller.run_action(TOGGLE_CLOUDY, False)

        controller.run_cycles(1, True, None, None)
        controller.run_action(TOGGLE_NIGHT_RELOAD, True)

        status = controller.run_cycles(12, False, None, None)

        actual = '0' if status == -1 else '1'
        controller.write('{}'.format(actual))

        controller.run_action(TOGGLE_NIGHT_RELOAD, False)
        controller.new_row()
