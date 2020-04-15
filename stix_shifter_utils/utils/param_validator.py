import json

def modernize_objects(module, params):

    config_json_path = f'stix_shifter_modules/{module}/configuration/{module}_config.json'
    
    try:
        with open(config_json_path) as mapping_file:
            configs = json.load(mapping_file)
    except Exception as ex:
        raise(ex)
    expected_connection = configs.get("connection")
    # for key, value in expected_connection.items():
    #     if key 

    if isinstance(params, dict):
        if "options" in params.keys():
            options = params.get('options')
            if isinstance(options, dict):
                for options_key, options_value in options.items():
                    params[options_key] = options_value
                params.pop("options")

    return params

def param_validator(module, connection, configuration):
    valid = False

    config_json_path = f'stix_shifter_modules/{module}/configuration/{module}_config.json'
    
    try:
        with open(config_json_path) as mapping_file:
            configs = json.load(mapping_file)
    except Exception as ex:
        raise(ex)
    
    if isinstance(configs, dict):
        for key, value in configs.items():
            if key == 'connection':
                expected_connection = configs.get("connection")
                valid = validate(connection, expected_connection)
            elif key == 'configuration':
                expected_configuration = configs.get("configuration")["auth"]
                valid = validate(configuration["auth"], expected_configuration)

    return valid

def validate(params, expected_params):
    valid = False

    if isinstance(params, dict):
        for key, value in expected_params.items():
            if key in params.keys():
                valid = True
            elif value.get('optional'):
                continue
            else:
                raise Exception("Parameter validation failed: parameter \"{}\" not found".format(key))
    else:
        raise Exception("Parameter validation failed: Invalid parameter object \"{}\" passed in the query".format(params))
    
    return valid

# def validate(params, expected_params):
#     valid = False

#     if isinstance(params, dict):
#         for key, value in params.items():
#             print('KEY' + str(key))
#             print('VALUE' + str(value))
#             # TODO: data type match
#             if isinstance(value, dict):
#                 print('VALUE2' + str(value))
#                 valid = validate(value, expected_params)
#             elif key in expected_params.keys():
#                 valid = True
#             elif expected_params.get(key)['optional']:
#                 continue
#             else:
#                 raise Exception("Parameter validation failed: Invalid parameter \"{}\" passed in the query".format(key))
#     else:
#         raise Exception("Parameter validation failed: Invalid parameter object \"{}\" passed in the query".format(params))
    
#     return valid
