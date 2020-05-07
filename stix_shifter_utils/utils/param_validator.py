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
                    old_path = value['previous']
                    old_value = get_dot_path(params_root, old_path)
                    if old_value:
                        params[key] = old_value
                        del_dot_path(params_root, old_path)
                if key in params:
                    modernize_step(value, params[key], params_root)

def get_dot_path(params, path):
    if '.' in path:
        pp = path.split('.')
        if pp[0] in params:
            return get_dot_path(params[pp[0]], '.'.join(pp[1:]))
    else:
        if path in params:
            return params[path]
        else:
            raise ValueError('Parameter not found: ' + path)

def del_dot_path(params, path):
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

    error_obj = {}
    if errors:
        error_obj['missing_params'] = errors
    if input_configs:
        if isinstance(input_configs, dict):
            error_obj['unexpected_params'] = get_inner_keys(input_configs)

    if error_obj:
        raise ValueError(error_obj)

    return validated_params


def copy_valid_configs(input_configs, expected_configs, validated_params, errors=[], current_path=''):
    if isinstance(expected_configs, dict):
        for key, value in expected_configs.items():
            key_path = current_path
            if key_path:
                key_path = key_path + '.'
            key_path = key_path + key
            if key in input_configs:
                if is_leaf(expected_configs[key]):
                    if 'min' in expected_configs[key]:
                        if not check_min(input_configs[key], expected_configs[key]['min'], expected_configs[key]['type'], key):
                            raise ValueError('\"{}: {}\" value must be more than {}'.format(key, str(input_configs[key]), str(expected_configs[key]['min'])))
                    elif 'max' in expected_configs[key]:
                        if not check_max(input_configs[key], expected_configs[key]['max'], expected_configs[key]['type'], key):
                            raise ValueError('\"{}: {}\" value must be less than {}'.format(key, str(input_configs[key]), str(expected_configs[key]['max'])))
                    elif 'regex' in expected_configs[key]:
                        if not check_regex(input_configs[key], expected_configs[key]['regex']):
                            raise ValueError('Invalid {} value \"{}\" specified'.format(key, str(input_configs[key])))

                    validated_params[key] = input_configs[key]
                    del input_configs[key]
                else:
                    if key not in validated_params:
                        validated_params[key] = dict()
                    copy_valid_configs(input_configs[key], expected_configs[key], validated_params[key], errors, key_path)
                    if not input_configs[key]:
                        del input_configs[key]
            else:
                if optional_section(expected_configs[key], key):
                    pass
                elif 'default' in expected_configs[key]:
                    validated_params[key] = value['default']
                elif ('optional' in expected_configs[key] and expected_configs[key]['optional']):
                    pass
                else:
                    errors.append(key_path)

def optional_section(item, key):
    if isinstance(item, dict):
        for key, value in item.items():
            if isinstance(value, dict):
                if 'optional' in value and value['optional'] or 'default' in value:
                    pass
                else:
                    return False
            else:
                return False
    return True

def is_leaf(config):
    if isinstance(config, dict):
        for key,value in config.items():
            if isinstance(value, dict):
                return False
    return True

def check_min(input_value, min_value, type, key):
    if type == 'number':
        if input_value >= min_value:
            return True
        else:
            return False

    if type == 'text':
        if len(input_value) >= len(min_value):
            return True
        else:
            return False
    raise ValueError('Min value property cannot be specified for type {} of field {}'.format(type, key))

def check_max(input_value, max_value, type, key):
    if type == 'number':
        if input_value <= max_value:
            return True
        else:
            return False

    if type == 'text':
        if len(input_value) <= len(max_value):
            return True
        else:
            return False

    raise ValueError('Min value property cannot be specified for type {} of field {}'.format(type, key))


def check_regex(input_value, regex_value):
    pattern = re.compile(regex_value)
    match_str = pattern.search(input_value)

    return bool(match_str)

def get_inner_keys(obj):
    keys = []
    for key, value in obj.items():
        if isinstance(value, dict):
            keys.extend(get_inner_keys(value))
        else:
            keys.append(key)
    return keys
