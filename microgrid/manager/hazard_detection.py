from microgrid.utils import *
import joblib

toggle_island_hazard_prediction = joblib.load('manager/models/toggle_island_hazard_prediction_model.sav')
toggle_night_reload_hazard_prediction = joblib.load('manager/models/toggle_night_reload_hazard_prediction_model.sav')

islanded = False
night_reload = False


def action_hazard_prediction(controller, external_action):
    select = 'SELECT value FROM {} WHERE ' \
             'name LIKE "TIME" OR ' \
             'name LIKE "ENERGY_STORAGE_ENERGY" OR ' \
             'name LIKE "SOLAR_ARRAY_POWER" OR ' \
             'name LIKE "DIESEL_GENERATOR_FUEL"'

    if external_action == TOGGLE_PEAK_SHAVING:
        return False

    if external_action == TOGGLE_ISLAND:
        global islanded

        if islanded:
            islanded = False
            return True
        else:
            values = controller.get_values(select)
            [prediction] = toggle_island_hazard_prediction.predict([values])
            islanded = prediction == 1

            return prediction == 1

    if external_action == TOGGLE_NIGHT_RELOAD:
        global night_reload

        if night_reload:
            night_reload = False
            return True
        else:
            values = controller.get_values(select)
            [prediction] = toggle_night_reload_hazard_prediction.predict([values])
            night_reload = prediction == 1

            return prediction == 1

    return True
