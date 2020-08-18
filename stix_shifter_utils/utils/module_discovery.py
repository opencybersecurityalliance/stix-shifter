import os
from importlib import import_module
from pathlib import Path


def process_dialects(cli_module, options):
    module, cli_dialects = __split_module_dialects(cli_module)
    if 'dialects' not in options or options['dialects'] is None:
        options['dialects'] = []
    options_dialects = options['dialects']
    dialects = list(set(cli_dialects+options_dialects))
    return module, dialects


def __split_module_dialects(module_dialects):
    module = None
    dialects = []
    if ':' in module_dialects:
        dialects = module_dialects.split(':')
        module = dialects.pop(0)
    else:
        module = module_dialects
        dialects = []
    return module, dialects


def dialect_list(module):
    modules = import_module('stix_shifter_modules')
    if '__file__' in dir(modules):
        modules_path = Path(modules.__file__).parent
    else:
        modules_path = modules.__path__._path[0]
    dialects_path = os.path.join(modules_path, f'{module}/stix_translation/json')
    ENDING = '_from_stix_map.json'
    dialects = []
    if os.path.isdir(dialects_path):
        files = [name for name in os.listdir(dialects_path) if (os.path.isfile(os.path.join(dialects_path, name)) and
                 (name.endswith(ENDING)))]
        dialects = list(map(lambda f: f[:-len(ENDING)], files))
    if not dialects:
        dialects = ['default']
    return dialects
