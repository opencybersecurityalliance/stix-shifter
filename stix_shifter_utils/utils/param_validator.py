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

    modernize_step(configs, params, params)

    # if isinstance(params, dict):
    #     if "options" in params.keys():
    #         options = params.get('options')
    #         if isinstance(options, dict):
    #             for options_key, options_value in options.items():
    #                 params[options_key] = options_value
    #             params.pop("options")

    # return params

def modernize_step(configs, params, params_root):
    if isinstance(configs, dict):
        for key, value in configs.items():
            if isinstance(value, dict):
                if 'previous' in value:
                    # insert old value
                    old_path = value['previous'] #connection.options.log_group_names
                    old_value = get_dot_path(params_root, old_path)#  <= replace to handle dots = connection.options.log_group_names, it can fail on any of 3 steps
                    if old_value:
                        params[key] = old_value
                        del_dot_path(params_root, old_path)
                    # del params_root[old_path]#  <= replace to handle dots = connection.options.log_group_names, it can fail on any of 3 steps
                    # delete old value
                # check that params[key] exists
                if key in params:
                    modernize_step(value, params[key], params_root)

def get_dot_path(params, path):
    # print(str(params), path)
    if '.' in path:
        pp = path.split('.')
        if pp[0] in params:
            return get_dot_path(params[pp[0]], '.'.join(pp[1:]))
    else:
        return params[path]

def del_dot_path(params, path):
    # print(str(params), path)
    if '.' in path:
        pp = path.split('.')
        if pp[0] in params:
            del_dot_path(params[pp[0]], '.'.join(pp[1:]))
            if len(params[pp[0]]) == 0:
                del params[pp[0]]
    else:
        del params[path]

def param_validator(module, connection, configuration):
    valid = False

    config_json_path = f'stix_shifter_modules/{module}/configuration/{module}_config.json'
    
    try:
        with open(config_json_path) as mapping_file:
            configs = json.load(mapping_file)
    except Exception as ex:
        raise(ex)
    
    # if isinstance(configs, dict):
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
    0. rework param_validator to a 1 call validation for configuration and connection (recurtion, options may contain only objects from the root level but everything is optional)
    1. all the keys(required) from json are present in udi config_json_path (implemented)
    2. no extra params are provided, except options
        |
         --->   on step 1
                during validation MOVE from udi_conf_dict to udi_conf_validated_dict
                make sure udi_conf_dict has no extra params 

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


if __name__ == "__main__":
    print('hello')

    udi_conf = {'connection': {'options': {'region': 'Labrador', 'region2': 'Nova Scotia'}}}
    rules = {'connection': {'region': {'type': 'text', 'previous': 'connection.options.region'}, 'region2': {'type': 'text', 'previous': 'connection.options.region2'}}}
    # value = get_dot_path(udi_conf, 'connection.options.region')
    # print(value)
    modernize_step(rules, udi_conf, udi_conf)
    print('=================')
    print(str(udi_conf))
    
     
