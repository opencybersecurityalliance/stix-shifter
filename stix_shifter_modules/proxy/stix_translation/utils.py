import json


def unwrap_connection_options(options):
    destination_params = options.get('destination')
    if type(destination_params) == str:
        if len(destination_params):
            destination_params = json.loads(destination_params)
        else:
            destination_params = {}
    return destination_params['connection'], destination_params['configuration']
