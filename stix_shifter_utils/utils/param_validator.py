import json

def param_validator(module, connection, configuration):
    validate = False
    updated_object = {}
    config_json_path = f'stix_shifter_modules/{module}/configuration/{module}_config.json'
    
    try:
        with open(config_json_path) as mapping_file:
            configs = json.load(mapping_file)
    except Exception as ex:
        raise(ex)
    
    expected_connection = configs.get("connection")
    expected_configuration = configs.get("configuration")

    validate, updated_object = connection_validator(connection, expected_connection)
    validate = configuration_validator(configuration, expected_configuration)
    
    return validate, updated_object

def connection_validator(connection, expected_connection):
    validate = False
    updated_connection = {}
    if isinstance(connection, dict):
        for key, value in connection.items():
            # TODO: data type match
            if key in expected_connection.keys():
                validate = True
            elif key == "options":
                if isinstance(value, dict):
                    for options_key, options_value in value.items():
                        if options_key in expected_connection.keys():
                            updated_connection[options_key] = options_value
                            validate = True
                        else:
                            raise Exception("Parameter validation failed: Invalid parameter \"{}\" passed in the options property".format(options_key))
                else:
                    raise Exception("Parameter validation failed: Invalid parameter passed in 'options'")
            else:
                raise Exception("Parameter validation failed: Invalid parameter \"{}\" passed in the query".format(key))

    return validate, updated_connection

def configuration_validator(configuration, expected_configuration):
    validate = False
    
    auth_object = configuration.get('auth')
    expected_auth_object = expected_configuration.get('auth')
    if auth_object:
        if isinstance(auth_object, dict):
            for key, value in auth_object.items():
                # TODO: data type match
                if key in expected_auth_object.keys():
                    validate = True
                else:
                    validate = False
                    raise Exception("Parameter validation failed: Invalid parameter \"{}\" passed in the query".format(key))
    else:
        raise Exception("Invalid configuration object: auth object not found")
    
    return validate
