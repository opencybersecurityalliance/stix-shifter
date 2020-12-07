import re
import json
from jsonmerge import merge
import importlib
from os import path
import copy

def get_merged_config(module):
    ss_modules_path = importlib.import_module('stix_shifter_modules')
    if isinstance(ss_modules_path.__path__, list):
        base_path = ss_modules_path.__path__[0]
    else:
        base_path = ss_modules_path.__path__._path[0]
    module_config_path = path.join(base_path, module, 'configuration', 'config.json')
    base_config_path = path.join(base_path, 'config.json')
    with open(module_config_path) as mapping_file:
        module_configs = json.load(mapping_file)
    if path.isfile(base_config_path):
        with open(base_config_path) as mapping_file:
            base_configs = json.load(mapping_file)
        module_configs = merge(base_configs, module_configs)
    return module_configs


def modernize_objects(module, params):
    expected_configs = get_merged_config(module)
    modernize_step(expected_configs, params, params)
    return params


def modernize_step(configs, params, params_root):
    if isinstance(configs, dict):
        for key, value in configs.items():
            if isinstance(value, dict):
                if 'previous' in value:
                    old_path = value['previous']
                    old_present, old_value = get_dot_path(params_root, old_path)
                    if key not in params:
                        if old_present:
                            params[key] = old_value
                    if old_present:
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
            return True, params[path]
    return False, None


def del_dot_path(params, path):
    if '.' in path:
        pp = path.split('.')
        if pp[0] in params:
            del_dot_path(params[pp[0]], '.'.join(pp[1:]))
            if len(params[pp[0]]) == 0:
                del params[pp[0]]
    else:
        del params[path]


def param_validator(module, input_configs, start_point=None):
    input_configs = copy.deepcopy(input_configs)
    expected_configs = get_merged_config(module)
    if start_point:
        start_points = start_point.split('.')
        for item in start_points:
            expected_configs = expected_configs[item]
    validated_params = {}
    errors = []
    copy_valid_configs(input_configs, expected_configs, validated_params, errors)

    error_obj = {}
    if errors:
        error_obj['missing_params'] = errors
    if input_configs:
        if isinstance(input_configs, dict):
            error_obj['unexpected_params'] = input_configs

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
                    if input_configs[key]:
                        if 'min' in expected_configs[key]:
                            if not check_min(input_configs[key], expected_configs[key]['min'],
                                             expected_configs[key]['type'], key):
                                raise ValueError('\"{}: {}\" value must be more than {}'.format(key, str(input_configs[key]),
                                                 str(expected_configs[key]['min'])))
                        if 'max' in expected_configs[key]:
                            if not check_max(input_configs[key], expected_configs[key]['max'],
                                             expected_configs[key]['type'], key):
                                raise ValueError('\"{}: {}\" value must be less than {}'.format(key, str(input_configs[key]),
                                                 str(expected_configs[key]['max'])))
                        if 'regex' in expected_configs[key]:
                            if not check_regex(input_configs[key], expected_configs[key]['regex']):
                                raise ValueError('Invalid {} value \"{}\" specified'.format(key, str(input_configs[key])))
                        
                        if expected_configs[key]['type'] == 'number':
                            if not check_number(input_configs[key]):
                                raise ValueError('{} "{}" type must be a number'.format(key, input_configs[key]))

                    input_value = input_configs[key]
                    if input_value is not None or ('nullable' in expected_configs[key] and expected_configs[key]['nullable']):
                        validated_params[key] = input_value
                        del input_configs[key]
                    elif 'default' in expected_configs[key]:
                        validated_params[key] = expected_configs[key]['default']
                        del input_configs[key]
                    elif ('optional' in expected_configs[key] and expected_configs[key]['optional']):
                        del input_configs[key]
                else:
                    if key not in validated_params:
                        validated_params[key] = dict()
                    copy_valid_configs(input_configs[key], expected_configs[key], validated_params[key], errors, key_path)
                    if not input_configs[key]:
                        del input_configs[key]
            else:
                if optional_section(expected_configs[key], key):
                    if default_section(expected_configs[key], key):
                        if key not in validated_params:
                            validated_params[key] = dict()
                        copy_valid_configs(dict(), expected_configs[key], validated_params[key], errors, key_path)
                    else:
                        pass
                elif 'default' in expected_configs[key]:
                    validated_params[key] = value['default']
                elif ('optional' in expected_configs[key] and expected_configs[key]['optional']):
                    pass
                elif key_path != 'connection.type':
                    errors.append(key_path)


def optional_section(item, key):
    if isinstance(item, dict):
        for key, value in item.items():
            if isinstance(value, dict):
                if 'optional' in value and value['optional'] or 'default' in value:
                    pass
                else:
                    return False
            elif key == 'type' and value == 'fields':
                pass
            else:
                return False
    return True


def default_section(item, key):
    if isinstance(item, dict):
        for key, value in item.items():
            if isinstance(value, dict):
                return 'default' in value
    return False


def is_leaf(config):
    if isinstance(config, dict):
        if 'type' in config and config['type'] == 'json':
            return True
        for key, value in config.items():
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
        if len(input_value) >= min_value:
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
        if len(input_value) <= max_value:
            return True
        else:
            return False

    raise ValueError('Min value property cannot be specified for type {} of field {}'.format(type, key))


def check_regex(input_value, regex_value):
    pattern = re.compile(regex_value)
    match_str = pattern.search(input_value)
    return bool(match_str)

def check_number(input_value):
    return isinstance(input_value, int)