from microgrid.manager.hazard_detection import *
from microgrid.utils import *
import random


def toggle_island_hazard_prediction_f_score(controller):
    select_1 = 'SELECT value FROM {} WHERE ' \
               'name LIKE "TIME" OR ' \
               'name LIKE "UTILITY_GRID_POWER" OR ' \
               'name LIKE "ENERGY_STORAGE_ENERGY" OR ' \
               'name LIKE "SOLAR_ARRAY_POWER" OR ' \
               'name LIKE "DIESEL_GENERATOR_FUEL"'

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
        SET_SOLAR_POWER,
        SET_LOAD,
    ]

    true_positives = 0
    false_positives = 0
    false_negatives = 0

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

        controller.run_cycles(1, True, select_1, custom_cycle)
        controller.run_action(TOGGLE_ISLAND, True)

        prediction = 'safe' if action_hazard_prediction(controller, TOGGLE_ISLAND) else 'failure'
        actual = 'safe' if controller.run_cycles(1, True, select_2, None) == 0 else 'failure'

        controller.write(' Prediction: ' + prediction + ', Actual: ' + actual)

        if prediction == 'failure' and actual == 'failure':
            controller.write(', \ttrue positive')
            true_positives += 1
        elif prediction == 'failure' and actual == 'safe':
            controller.write(', \tfalse positive')
            false_positives += 1
        elif prediction == 'safe' and actual == 'failure':
            controller.write(', \tfalse negative')
            false_negatives += 1

        controller.run_action(TOGGLE_ISLAND, False)
        controller.run_cycles(1, False, None, None)
        controller.new_row()

    controller.write('True positives: {}\n'.format(true_positives))
    controller.write('False positives: {}\n'.format(false_positives))
    controller.write('False negatives: {}\n'.format(false_negatives))

    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)

    controller.write('Precision: {}\n'.format(precision))
    controller.write('Recall: {}\n'.format(recall))

    f_score = (2 * precision * recall) / (precision + recall)

    controller.write('F-score: {}'.format(f_score))
