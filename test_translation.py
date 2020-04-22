# import stix_shifter_utils.utils.module_discovery
import os
from stix_shifter.stix_transmission import stix_transmission
import importlib

def module_list():
    modules_path = 'stix_shifter_modules'
    dirs = []
    if os.path.isdir(modules_path):
        dirs = [ name for name in os.listdir(modules_path) if (os.path.isdir(os.path.join(modules_path, name)) and (not name.startswith('__')) )]
    return dirs

def main():
    # modules = module_list().sort()
    modules = ['aws_cloud_watch_logs']
    connection = {'c': 'c'}
    configuration = {'c': 'c'}
    # print(f'modules: {modules}')
    for module in modules:
        transmission = stix_transmission.StixTransmission(module, connection, configuration)
        result = transmission.ping()

        # datamapper_module = importlib.import_module(
        #             "stix_shifter_modules." + module + ".stix_translation")
        # # print((os.path.dirname(datamapper_module.__file__)))
        print(f'result: {result}')

if __name__ == '__main__':
    main()