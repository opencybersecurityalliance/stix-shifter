from setuptools import find_packages
# To use a consistent encoding
from codecs import open
import sys
import shutil
import subprocess
import json
import io
import os
from jsonmerge import merge
import tempfile
import importlib

here = os.path.abspath(os.path.dirname(__file__))
SKIP_ME = 'SKIP.ME'

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

TMP_MAPPING_DIR = 'tmp_mapping'
MODULES_DIR = 'stix_shifter_modules'
if os.path.isdir(TMP_MAPPING_DIR):
    shutil.rmtree(TMP_MAPPING_DIR)

os.mkdir(TMP_MAPPING_DIR)

for module in [o for o in os.listdir(MODULES_DIR) if (os.path.isdir(os.path.join(MODULES_DIR,o)) and not o.startswith('_'))]:
    if not os.path.isfile(os.path.join(MODULES_DIR, module, 'SKIP.ME')):
        print(module + '..')
        connector_module = importlib.import_module("stix_shifter_modules." + module + ".entry_point")
        entry_point = connector_module.EntryPoint()
        mapping = entry_point.get_mapping()
        with open(os.path.join(TMP_MAPPING_DIR, module+'.json'), 'w') as f:
            json.dump(mapping, f, sort_keys=False, indent=4)

def fill_connectors(projects, modules_path):
    modules = [name for name in os.listdir(modules_path)
               if (os.path.isdir(os.path.join(modules_path, name)) and (not name.startswith('__')))]
    for module in modules:
        if not os.path.isfile(os.path.join(modules_path, module, SKIP_ME)):
            projects['stix_shifter_modules_' + module] = ['stix_shifter_modules/' + module]

# The mode determines how the stix-shifter is packaged
# 1 = Include everything in 1 whl package
# 3 - 3 whl packages respectively for stix-shifter, stix-shifter-utils and stix-shifter-modules
# N - stix-shifter, stix-shifter-utils, and each connector is packaged separately
# <module name> - package only the specified connector

mode = 'N'
if 'MODE' in os.environ:
    mode = os.environ['MODE']

# DO NOT remove spaces around the equal sign at the line below
version = '1.0.0'
if 'VERSION' in os.environ:
    version = os.environ['VERSION']

if mode == '1':
    projects = {
        "stix_shifter": [
            'stix_shifter_utils',
            'stix_shifter',
            'stix_shifter_modules'
            ]
    }
elif mode == '3':
    projects = {
        "stix_shifter_utils": ["stix_shifter_utils"],
        "stix_shifter": ["stix_shifter"],
        "stix_shifter_modules": ["stix_shifter_modules"],
    }
elif mode == 'N':
    projects = {
        "stix_shifter_utils": ["stix_shifter_utils"],
        "stix_shifter": ["stix_shifter"],
    }
    fill_connectors(projects, "stix_shifter_modules")
else:
    module_path = 'stix_shifter_modules/' + mode
    if os.path.isdir(module_path):
        projects = {
            "stix_shifter_modules_" + mode: [module_path]
        }
    else:
        print('Unexpected value in MODE environment variable: %s' % mode)
        print('Allowed values: 1|3|N|module_name')
        exit(1)

for project_name in projects.keys():
    cleanup_file_list = []
    temp_dir = None
    module_dir = None

    src_folders = projects[project_name]
    print('processing project_name %s' % project_name)

    # Prepare packages
    packages_include = []
    for src_folder in src_folders:
        packages_include.append(src_folder.replace('/', '.'))
        packages_include.append(src_folder.replace('/', '.') + '.*')
    print('packages_include: %s' % packages_include)
    packages = find_packages(include=packages_include)
    print('packages: %s' % packages)

    # Prepare requires list
    install_requires = set()
    requirements_files = []
    for src_folder in src_folders:
        for r, d, f in os.walk(src_folder):
            for file in f:
                if 'requirements.txt' == file and not os.path.isfile(os.path.join(r, SKIP_ME)):
                    requirements_files.append(os.path.join(r, file))
    print('requirements_files: %s' % requirements_files)
    for requirements_file in requirements_files:
        with open(requirements_file) as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]
        lines = list(filter(lambda s: (not s.startswith('#')) and len(s) > 0, lines))
        install_requires.update(lines)
    install_requires = list(install_requires)
    print('install_requires: %s' % install_requires)

    # Prepare entry points
    entry_points = {}
    entry_points_items = []
    for src_folder in src_folders:
        entry_point_path = os.path.join(src_folder, 'scripts', src_folder+'.py')
        if os.path.exists(entry_point_path):
            entry_points_items.append('%s=%s.scripts.%s:main' % (project_name.replace('_', '-'), project_name, project_name))
    if len(entry_points_items) > 0:
        entry_points = {  # Optional
            'console_scripts': entry_points_items
            }
    print('entry_points: %s' % entry_points)

    # Prepare setup params
    params = {
        'name': project_name,  # Required
        'version': version,  # Required
        'description': 'Tools and interface to translate STIX formatted results and queries to different data source '
                       + 'formats and to set up appropriate connection strings for invoking and triggering actions '
                       + 'in openwhisk',  # Required
        'long_description': long_description,  # Optional
        'long_description_content_type': 'text/markdown',
                                         # Optional (see note above)
        'url': 'https://github.com/opencybersecurityalliance/stix-shifter',  # Optional
        'author': 'ibm',
        'author_email': '',  # Optional
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'classifiers': [  # Optional
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3.6',
        ],
        'keywords': 'datasource stix translate transform transmit',  # Optional
        'packages': packages,  # Required
        'install_requires': install_requires,
        'include_package_data': True,
        'entry_points': entry_points,  # Optional
        'project_urls': {  # Optional
            'Source': 'https://github.com/opencybersecurityalliance/stix-shifter',
        },
    }

    # Prepare MANIFEST.in, include json files
    shutil.rmtree('MANIFEST.in', ignore_errors=True)
    shutil.copyfile('build_templates/MANIFEST.in', 'MANIFEST.in')
    json_include_lines = []

    for json_search_path in src_folders:
        connector_name = ''
        json_search_path_split = json_search_path.split(os.sep)
        if len(json_search_path_split) > 1:
            connector_name = json_search_path_split[1]
        module_dir = json_search_path
        configuration_path = os.path.join(module_dir, 'configuration')
        if os.path.isdir(configuration_path):
            conf_path = os.path.join(module_dir, 'conf')
            shutil.rmtree(conf_path, ignore_errors=True)
            os.mkdir(conf_path)
            for r, d, f in os.walk(configuration_path):
                for file in f:
                    configuration_file_path = os.path.join(r, file)
                    with open(configuration_file_path) as json_file:
                        module_data = json.load(json_file)
                    base_data = None
                    data = dict()
                    base_path = os.path.join(r, '..', '..', file)
                    if os.path.isfile(base_path):
                        with open(base_path) as json_file:
                            base_data = json.load(json_file)
                        data = base_data
                    data = merge(module_data, data)
                    if file == 'config.json':
                        with open(os.path.join(TMP_MAPPING_DIR, connector_name+ '.json')) as f:
                            mapping = json.load(f)
                            data['connection']['options']['mapping']['default'] = mapping
                    json_file_path = os.path.join(r, '..', 'conf', file)
                    with open(json_file_path, 'w') as json_file:
                        json_file.write(json.dumps(data, indent=4, sort_keys=False))
            temp_dir = tempfile.TemporaryDirectory()
            shutil.move(configuration_path, temp_dir.name)
            os.rename(conf_path, configuration_path)
            cleanup_file_list.append(configuration_path)

        for r, d, f in os.walk(module_dir):
            r_split = r.split(os.sep)
            if not (len(r_split) >= 3 and ('tests' == r_split[2])):
                for file in f:
                    if '.json' in file:
                        json_include_lines.append('include ' + os.path.join(r, file) + ' \n')
    with open('MANIFEST.in', 'a') as out_file:
        out_file.writelines(json_include_lines)

    # Run setup()
    proc_params = ['python3', 'build_templates/setup_one.py']
    proc_params.extend(sys.argv[1:])
    proc_params.append(json.dumps(params))
    proc = subprocess.Popen(proc_params, stdout=subprocess.PIPE)
    for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
        if not line:
            break
        print(line.rstrip())

    # Cleanup
    cleanup_file_list.extend(['build', 'MANIFEST.in', project_name + '.egg-info'])
    for cleanup_file in cleanup_file_list:
        if os.path.exists(cleanup_file):
            if os.path.isdir(cleanup_file):
                shutil.rmtree(cleanup_file)
            else:
                os.remove(cleanup_file)
    if temp_dir is not None:
        shutil.move(os.path.join(temp_dir.name, 'configuration'), module_dir)
        temp_dir = None
    print('---------------------------------')
shutil.rmtree(TMP_MAPPING_DIR)
