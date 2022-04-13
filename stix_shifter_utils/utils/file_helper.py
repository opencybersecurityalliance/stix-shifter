import json
import traceback
import os
from pathlib import Path
from stix_shifter_utils.utils.logger import set_logger

logger = set_logger(__name__)
__path_searchable = ['stix_shifter_modules', 'modules']
__default_search_path = ['stix_translation', 'json']


def read_json(filepath, options, search_path=__default_search_path):
    # Read JSON file that is either passed in with the options or internally contained in the module
    # logger.debug('call: read_json: ' + json.dumps(options, indent=4))
    # filepath may be:
    #  'to_stix_map.json' -> 'to_stix_map' mapping data if present otherwise contents of 'module'/stix_translation/json/to_stix_map.json
    #  'to_stix_map' -> 'to_stix_map' mapping data if present otherwise contents of 'module'/stix_translation/json/to_stix_map.json
    #  '/full/path/somefile.json' -> 'somefile' mapping data if present otherwise contents of /full/path/somefile.json
    file_name = Path(filepath).name
    file_key = file_name
    trim_str = '.json'
    if file_key.endswith(trim_str):
        file_key = file_key[:-len(trim_str)]
    if 'mapping' in options and file_key in options['mapping']:
        logger.debug('returning options_mapping for: ' + filepath)
        return options['mapping'][file_key]

    if os.path.isfile(filepath):
        file_path = filepath
        logger.debug('returning full_path for: ' + filepath)
    else:
        if not file_name.endswith(trim_str):
            file_name = file_name + trim_str
        json_path = get_json_path(search_path)
        file_path = os.path.join(json_path, file_name)
        logger.debug('returning in_module_path for: ' + filepath + '->' + file_path)
    with open(file_path, 'r') as f:
        return json.load(f)


def get_json_path(search_path=__default_search_path, depth=3):
    caller_file_path = traceback.extract_stack()[-depth].filename
    path = caller_file_path.split(os.sep)
    if not path[0]:
        path[0] = os.path.sep
    path_item_id = 0
    for path_item in path:
        for path_searchable_item in __path_searchable:
            if path_item == path_searchable_item:
                path = path[:path_item_id+2]
                for p in search_path:
                    path.append(p)
                return os.path.join(*path)
        path_item_id += 1
    return get_json_path(search_path, depth+2)
