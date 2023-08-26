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
    controller.write('t,esp,ese,sap,dgf,ldp,action,t1,ugp1,esp1,ese1,dgf1,ldp1,class\n')

    select_1 = 'SELECT value FROM {} WHERE ' \
               'name LIKE "TIME" OR ' \
               'name LIKE "ENERGY_STORAGE_POWER" OR ' \
               'name LIKE "ENERGY_STORAGE_ENERGY" OR ' \
               'name LIKE "SOLAR_ARRAY_POWER" OR ' \
               'name LIKE "DIESEL_GENERATOR_FUEL" OR ' \
               'name LIKE "LOAD_DEMAND_POWER"'

    select_2 = 'SELECT value FROM {} WHERE ' \
               'name LIKE "TIME" OR ' \
               'name LIKE "UTILITY_GRID_POWER" OR ' \
               'name LIKE "ENERGY_STORAGE_POWER" OR ' \
               'name LIKE "ENERGY_STORAGE_ENERGY" OR ' \
               'name LIKE "DIESEL_GENERATOR_FUEL" OR ' \
               'name LIKE "LOAD_DEMAND_POWER"'

    custom_cycle = [
        CLOCK_TICK,
        SET_GRID_VOLTAGE,
        SET_SOLAR_POWER,
        SET_LOAD,
        PEAK_SHAVING
    ]

    fuels = [750, 350, 100, 50, 40, 30, 20, 10, 5, 0]
    energies = [1000, 750, 500, 250, 150, 100, 50, 25, 0]

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
                    controller.run_action(TOGGLE_NIGHT_RELOAD, True)

                    status = controller.run_cycles(12, False, None, None)

                    final_state = controller.get_values(select_2)
                    actual = '0' if status == -1 else '1'
                    controller.write('{}, {}'.format(str(final_state)[1:-1], actual))

                    controller.run_action(TOGGLE_NIGHT_RELOAD, False)
                    controller.new_row()

            time += 3600

        controller.run_action(TOGGLE_CLOUDY, False)


def anomaly_detection_dataset(controller, stealthy_action):
    controller.write('h,t,ugp,ugv,ugc,esp,esv,esc,ese,sap,dgp,dgf,ldp,class\n')

    fuels = [1000, 750, 500, 250, 100, 50]
    energies = [1000, 750, 500, 250, 100, 50]

    anomaly = 1

    if stealthy_action is not None:
        controller.run_action(stealthy_action, False)
        anomaly = 0

    for i in range(3):

        if 0 < i <= 2:
            controller.run_action(TOGGLE_ISLAND, False)

        if i == 2:
            controller.run_action(TOGGLE_NIGHT_RELOAD, False)

        for j in range(2):
            time = -900

            for k in range(48):

                for fuel in fuels:

                    for energy in energies:
                        updates = ['UPDATE {} SET value = {} WHERE name LIKE "TIME"'.format({}, time),
                                   'UPDATE {} SET value = {} WHERE name LIKE "ENERGY_STORAGE_ENERGY"'.format({},
                                                                                                             energy),
                                   'UPDATE {} SET value = {} WHERE name LIKE "DIESEL_GENERATOR_FUEL"'.format({}, fuel)]

                        controller.set_state(updates)
                        controller.run_cycles(1, True, None, None)

                        controller.write('{}'.format(anomaly))
                        controller.new_row()

                time += 1800

            controller.run_action(TOGGLE_CLOUDY, False)
