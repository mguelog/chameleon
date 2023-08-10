from microgrid.utils import *
import joblib


def action_hazard_prediction(controller, external_action):
    if external_action == TOGGLE_PEAK_SHAVING:
        return False

    if external_action == TOGGLE_ISLAND:

        select = 'SELECT value FROM {} WHERE ' \
                 'name LIKE "UTILITY_GRID_POWER"'

        [power] = controller.get_values(select)

        if power == 0:
            return True
        else:

            select = 'SELECT value FROM {} WHERE ' \
                     'name LIKE "TIME" OR ' \
                     'name LIKE "ENERGY_STORAGE_ENERGY" OR ' \
                     'name LIKE "SOLAR_ARRAY_POWER" OR ' \
                     'name LIKE "DIESEL_GENERATOR_FUEL"'

            model = joblib.load('manager/models/toggle_island_hazard_prediction_model.sav')
            values = controller.get_values(select)

            [prediction] = model.predict([values])

            return prediction == 1

    return True
