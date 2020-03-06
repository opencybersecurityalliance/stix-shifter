import os

def process_dialects(cli_module, options):
    module, cli_dialects = split_module_dialects(cli_module)
    if 'dialects' not in options:
        options['dialect'] = []
    options_dialects = options['dialect']
    
    dialects = list(set(cli_dialects+options_dialects))
    if len(dialects)>1 and 'default' in dialects:
        dialects.remove('default')
    options['dialect'] = dialects
    return module, dialects

def split_module_dialects(module_dialects):
    module = None
    dialects = []
    if ':' in module_dialects:
        dialects = module_dialects.split(':')
        module = dialects.pop(0)
    else:
        module = module_dialects
        dialects = dialect_list(module)
    return module, dialects

def module_list():
    modules_path = 'stix_shifter_modules'
    dirs = [ name for name in os.listdir(modules_path) if (os.path.isdir(os.path.join(modules_path, name)) and (not name.startswith('__')) )]
    return dirs

def dialect_list(module):
    dialects_path = f'stix_shifter_modules/{module}/stix_translation/json'
    ENDING = '_from_stix_map.json'
    dialects = []
    if os.path.isdir(dialects_path):
        files = [ name for name in os.listdir(dialects_path) if (os.path.isfile(os.path.join(dialects_path, name)) and (name.endswith(ENDING)) )]
        dialects = list(map(lambda f: f[:-len(ENDING)], files))
    if not dialects:
        dialects = ['default']
    return dialects