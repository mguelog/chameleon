from microgrid.utils import *


def toggle_island_hazard_prediction_dataset(controller):
    controller.write('t,ese,sap,dgf,ldp,action,t1,ugp1,esp1,ese1,sap1,dgp1,dgf1,ldp1,class\n')

    select_1 = 'SELECT value FROM {} WHERE ' \
               'name LIKE "TIME" OR ' \
               'name LIKE "ENERGY_STORAGE_ENERGY" OR ' \
               'name LIKE "SOLAR_ARRAY_POWER" OR ' \
               'name LIKE "DIESEL_GENERATOR_FUEL" OR ' \
               'name LIKE "LOAD_DEMAND_POWER"'

    select_2 = 'SELECT value FROM {} WHERE ' \
               'name LIKE "TIME" OR ' \
               'name LIKE "UTILITY_GRID_POWER" OR ' \
               'name LIKE "ENERGY_STORAGE_POWER" OR ' \
               'name LIKE "ENERGY_STORAGE_ENERGY" OR ' \
               'name LIKE "SOLAR_ARRAY_POWER" OR ' \
               'name LIKE "DIESEL_GENERATOR_POWER" OR ' \
               'name LIKE "DIESEL_GENERATOR_FUEL" OR ' \
               'name LIKE "LOAD_DEMAND_POWER"'

    custom_cycle = [
        CLOCK_TICK,
        SET_SOLAR_POWER,
        SET_LOAD,
    ]

    energies = [750, 350, 180, 160, 140, 120, 100, 80, 60, 40, 20, 10, 5, 0]
    fuels = [750, 250, 75, 30, 25, 20, 15, 10, 5, 0, 22.5, 17.5, 12.5, 7.5, 2.5]

    for i in range(2):

        for energy in energies:

            for fuel in fuels:

                time = -900

                for j in range(96):
                    updates = ['UPDATE {} SET value = {} WHERE name LIKE "TIME"'.format({}, time),
                               'UPDATE {} SET value = {} WHERE name LIKE "ENERGY_STORAGE_ENERGY"'.format({}, energy),
                               'UPDATE {} SET value = {} WHERE name LIKE "DIESEL_GENERATOR_FUEL"'.format({}, fuel)]

                    controller.set_state(updates)
                    controller.run_cycles(1, True, select_1, custom_cycle)
                    controller.run_action(TOGGLE_ISLAND, True)
                    status = controller.run_cycles(1, True, select_2, None)

                    value = '0' if status == -1 else '1'
                    controller.write(value)

                    controller.run_action(TOGGLE_ISLAND, False)
                    controller.new_row()

                    time += 900

        controller.run_action(TOGGLE_CLOUDY, False)
        controller.run_cycles(1, False, None, None)


def toggle_night_reload_hazard_prediction_dataset(controller):
    controller.write('t,ese,sap,dgf,ldp,t1,ese1,dgf1,h,class\n')

    select_1 = 'SELECT value FROM {} WHERE ' \
               'name LIKE "TIME" OR ' \
               'name LIKE "ENERGY_STORAGE_ENERGY" OR ' \
               'name LIKE "SOLAR_ARRAY_POWER" OR ' \
               'name LIKE "DIESEL_GENERATOR_FUEL" OR ' \
               'name LIKE "LOAD_DEMAND_POWER"'

    select_2 = 'SELECT value FROM {} WHERE ' \
               'name LIKE "TIME" OR ' \
               'name LIKE "ENERGY_STORAGE_ENERGY" OR ' \
               'name LIKE "DIESEL_GENERATOR_FUEL"'

    select_3 = 'SELECT value FROM {} WHERE ' \
               'name LIKE "DIESEL_GENERATOR_FUEL"'

    custom_cycle = [
        CLOCK_TICK,
        SET_GRID_VOLTAGE,
        SET_SOLAR_POWER,
        SET_LOAD,
        PEAK_SHAVING,
        CONSUME_BATTERY,
        GENERATOR_SUPPLY,
        RELOAD_BATTERY
    ]

    fuels = [750, 350, 100, 50, 25, 10, 20, 5, 2.5, 0]
    energies = [1000, 750, 500, 200, 50, 0, 100, 25]

    for k in range(2):
        time = -3600

        for i in range(24):

            for fuel in fuels:

                for energy in energies:

                    updates = ['UPDATE {} SET value = {} WHERE name LIKE "TIME"'.format({}, time),
                               'UPDATE {} SET value = {} WHERE name LIKE "ENERGY_STORAGE_ENERGY"'.format({}, energy),
                               'UPDATE {} SET value = {} WHERE name LIKE "DIESEL_GENERATOR_FUEL"'.format({}, fuel)]

                    controller.set_state(updates)
                    controller.run_cycles(1, True, select_1, custom_cycle)

                    [remaining_fuel] = controller.get_values(select_3)
                    j = 0

                    while remaining_fuel > 0 and j < 24:
                        controller.run_cycles(1, False, None, custom_cycle)
                        [remaining_fuel] = controller.get_values(select_3)
                        j += 1

                    final_state = controller.get_values(select_2)
                    value = '0' if j < 24 else '1'
                    controller.write('{}, {}, {}'.format(str(final_state)[1:-1], j, value))

                    controller.new_row()

            time += 3600

        controller.run_action(TOGGLE_CLOUDY, False)
        controller.run_cycles(1, False, None, None)
