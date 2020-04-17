import re
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
    
    validated_params = {}
    errors = []
    copy_valid_configs(input_configs, expected_configs, validated_params, errors)

    if errors:
        raise ValueError('unexpected params: %s' % errors)
    
    if input_configs:
        raise ValueError('unexpected params: %s' % input_configs)

    return validated_params

#rename to copy config expected values
def copy_valid_configs(input_configs, expected_configs, validated_params, errors=[], current_path=''):

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
        print('current_path -->' + (current_path), is_leaf(expected_configs))
        for key, value in expected_configs.items():
            key_path = current_path
            if key_path:
                key_path = key_path + '.'
            key_path = key_path + key
            if key in input_configs:
                if is_leaf(expected_configs[key]):
                    #TODO apply validation rules: min, max, regex, etc
                    if 'min' in expected_configs[key]:
                        if not check_min(input_configs[key], expected_configs[key]['min']):
                            raise ValueError('\"{}: {}\" value must be more than {}'.format(key, str(input_configs[key]), str(expected_configs[key]['min'])))
                    elif 'max' in expected_configs[key]:
                        if not check_max(input_configs[key], expected_configs[key]['max']):
                            raise ValueError('\"{}: {}\" value must be less than {}'.format(key, str(input_configs[key]), str(expected_configs[key]['max'])))
                    elif 'regex' in expected_configs[key]:
                        if not check_regex(input_configs[key], expected_configs[key]['regex']):
                            raise ValueError('Invalid {} value \"{}\" specified'.format(key, str(input_configs[key])))

                    validated_params[key] = input_configs[key]
                    print('moved here', key_path)
                    del input_configs[key]
                else:
                    if key not in validated_params:
                        validated_params[key] = dict()
                        print('created: ', key_path)
                    copy_valid_configs(input_configs[key], expected_configs[key], validated_params[key], errors, key_path)
                    if not input_configs[key]:
                        del input_configs[key]
            else:
                if 'optional' in expected_configs[key] and not expected_configs[key]['optional']:
                    errors.append('input configuration is missing: ' + key_path)


def is_leaf(config):
    # print(str(type(config)))
    if isinstance(config, dict):
        for key,value in config.items():
            if isinstance(value, dict):
                return False
    return True

def check_min(input_value, min_value):
    if input_value >= min_value:
        return True
    else:
        return False 

def check_max(input_value, max_value):
    if input_value <= max_value:
        return True
    else:
        return False

def check_regex(input_value, regex_value):
    pattern = re.compile(regex_value)
    match_str = pattern.search(input_value)

    if match_str:
        return True
    else:
        False

if __name__ == "__main__":

    # udi_conf = {'connection': {'options': {'region': 'Labrador', 'region2': 'Nova Scotia'}}}
    # rules = {'connection': {'region': {'type': 'text', 'previous': 'connection.options.region'}, 'region2': {'type': 'text', 'previous': 'connection.options.region2'}}}
    # value = get_dot_path(udi_conf, 'connection.options.region')
    # print(value)
    # modernize_step(rules, udi_conf, udi_conf)
    # print('=================')
    # print(str(udi_conf))

    # input_params = {'connection': {'region': 'us-east'} }
    module = 'aws_cloud_watch_logs'
    config_json_path = f'stix_shifter_modules/{module}/configuration/{module}_config.json'
    
    try:
        with open(config_json_path) as mapping_file:
            expected_configs = json.load(mapping_file)
    except Exception as ex:
        raise(ex)
    # invalid original config
    # input_configs = {'configuration': {'aws_access_key_id': 'AKIA6IBDIZS3EIAR5RM5', 'aws_iam_role': 'arn:aws:iam::979326..._api_role', 'aws_secret_access_key': 'p0qAfOlxJ/zd0yqhj/D...ssoF+A0Cd'}, 'connection': {'k1': 'v1', 'region': 'us-east-1'}}
    # valid config with configuration.auth object
    # input_configs = {'configuration': {'auth': {'aws_access_key_id': 'AKIA6IBDIZS3EIAR5RM5', 'aws_iam_role': 'arn:aws:iam::979326..._api_role', 'aws_secret_access_key': 'p0qAfOlxJ/zd0yqhj/D...ssoF+A0Cd'}}, 'connection': {'k1': 'v1', 'region': 'us-east-1'}}
    # validated_params = {}
    # print('input_configs    :    '+ str(input_configs))
    # errors = []
    # validate(input_configs, expected_configs, validated_params, errors)
    # print('errors: ', str(errors))
    
    # print('validated_params : ' + str(validated_params))
    # print('input_configs out:'+ str(input_configs))

    # ptr = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\-]*[a-zA-Z0-9])\\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\\-]*[A-Za-z0-9])$"
    # # inp = "stable-tor01-vm-sa-uds.qradar.ibmcloud-dev.com"
    # inp = "127001&&"
    # check_regex(inp, ptr)