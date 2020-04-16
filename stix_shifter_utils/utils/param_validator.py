import json

def modernize_objects(module, params):

    config_json_path = f'stix_shifter_modules/{module}/configuration/{module}_config.json'
    
    try:
        with open(config_json_path) as mapping_file:
            configs = json.load(mapping_file)
    except Exception as ex:
        raise(ex)

    modernize_step(configs, params, params)

    return params

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

def param_validator(module, input_configs):

    config_json_path = f'stix_shifter_modules/{module}/configuration/{module}_config.json'
    
    try:
        with open(config_json_path) as mapping_file:
            expected_configs = json.load(mapping_file)
    except Exception as ex:
        raise(ex)
    
    # if isinstance(expected_configs, dict):
    #     if expected_configs['connection']:
    #         return_obj = {}
    #         validate(connection, expected_configs['connection'], return_obj)
    #         print(str(return_obj))
    #         if connection:
    #             for k in connection.keys():
    #                 print('Invalid param: ' + str(k))
    #     if expected_configs['configuration']:
    #          validate(configuration, expected_configs['configuration'], return_obj)
    #          if configuration:
    #             for k in configuration.keys():
    #                 print('Invalid param: ' + str(k))
    #          print(str(return_obj))
    validated_params = {}
    validate(input_configs, expected_configs, validated_params)


def validate(input_configs, expected_configs, validated_params):

    # 0. rework param_validator to a 1 call validation for configuration and connection (recurtion, options may contain only objects from the root level but everything is optional)
    # 1. all the keys(required) from json are present in udi config_json_path (implemented)
    # 2. no extra params are provided, except options
    #     |
    #      --->   on step 1
    #             during validation MOVE from udi_conf_dict to udi_conf_validated_dict
    #             make sure udi_conf_dict has no extra params 

    # udi_conf_dict = {} 
    # udi_conf_validated_dict = {}

    if isinstance(expected_configs, dict):
        for key, value in expected_configs.items():
            if key in input_configs:
                if isinstance(value, dict):
                    validate(input_configs[key], value, validated_params)
                
                if key in input_configs:
                    validated_params[key] = input_configs[key]
                    del input_configs[key]
                

if __name__ == "__main__":

    udi_conf = {'connection': {'options': {'region': 'Labrador', 'region2': 'Nova Scotia'}}}
    rules = {'connection': {'region': {'type': 'text', 'previous': 'connection.options.region'}, 'region2': {'type': 'text', 'previous': 'connection.options.region2'}}}
    # value = get_dot_path(udi_conf, 'connection.options.region')
    # print(value)
    # modernize_step(rules, udi_conf, udi_conf)
    # print('=================')
    # print(str(udi_conf))

    input_params = {'connection': {'region': 'us-east'} }
    module = 'aws_cloud_watch_logs'
    config_json_path = f'stix_shifter_modules/{module}/configuration/{module}_config.json'
    
    try:
        with open(config_json_path) as mapping_file:
            expected_configs = json.load(mapping_file)
    except Exception as ex:
        raise(ex)
    input_configs = {'configuration': {'aws_access_key_id': 'AKIA6IBDIZS3EIAR5RM5', 'aws_iam_role': 'arn:aws:iam::979326..._api_role', 'aws_secret_access_key': 'p0qAfOlxJ/zd0yqhj/D...ssoF+A0Cd'}, 'connection': {'k1': 'v1', 'region': 'us-east-1'}}
    validated_params = {}
    validate(input_configs, expected_configs, validated_params)