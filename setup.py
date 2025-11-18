#!/usr/bin/env python3
import os
import subprocess
import sys
import shutil
import json
import io
import tempfile
import importlib

from setuptools import find_packages
# To use a consistent encoding
from codecs import open
from jsonmerge import merge

# Constants used across the script (kept the same names/semantics)
here = os.path.abspath(os.path.dirname(__file__))
SKIP_ME = 'SKIP.ME'
TMP_MAPPING_DIR = 'tmp_mapping'
MODULES_DIR = 'stix_shifter_modules'
# DO NOT remove spaces around the equal sign at the line below
DEFAULT_VERSION = '1.0.0'
DEFAULT_MODE = 'N'

# ------------------------------------------------------------------------------
# Low-level utility functions
# ------------------------------------------------------------------------------


def check_python_version():
    """
    Ensure Python interpreter is 3.10 or greater. If not, print an error and exit.
    """
    if sys.version_info.major == 3 and sys.version_info.minor >= 10:
        print(sys.version)
    else:
        print("Error: stix-shifter requires python 3.10 or greater")
        exit(1)


def run_generate_requirements():
    """
    Import and run the generate_requirements() function.
    """
    from generate_requirements import generate_requirements
    generate_requirements()


def install_dev_requirements():
    """
    Install development requirements via pip using the requirements-dev.txt file.
    """
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"])


def ensure_tmp_mapping_dir():
    """
    Create a temporary mapping directory, clearing any pre-existing one.
    Returns the path.
    """
    if os.path.isdir(TMP_MAPPING_DIR):
        shutil.rmtree(TMP_MAPPING_DIR)
    os.mkdir(TMP_MAPPING_DIR)
    return TMP_MAPPING_DIR


# ------------------------------------------------------------------------------
# Mapping generation for connectors
# ------------------------------------------------------------------------------


def generate_connector_mappings(tmp_mapping_dir=TMP_MAPPING_DIR, modules_dir=MODULES_DIR):
    """
    Iterate over connectors in stix_shifter_modules and write each connector's mapping
    file into TMP_MAPPING_DIR/<module>.json unless the module contains SKIP.ME.
    """
    for module in [
        o for o in os.listdir(modules_dir)
        if (os.path.isdir(os.path.join(modules_dir, o)) and not o.startswith('_'))
    ]:
        skip_path = os.path.join(modules_dir, module, SKIP_ME)
        if not os.path.isfile(skip_path):
            print(f"processing mapping for {module}...")
            connector_module = importlib.import_module(f"stix_shifter_modules.{module}.entry_point")
            entry_point = connector_module.EntryPoint()
            mapping = entry_point.get_mapping()
            out_path = os.path.join(tmp_mapping_dir, module + '.json')
            with open(out_path, 'w', encoding="utf-8") as f:
                json.dump(mapping, f, sort_keys=False, indent=4)


# ------------------------------------------------------------------------------
# Project population helpers
# ------------------------------------------------------------------------------


def fill_connectors(projects, modules_path):
    """
    Discover connector directories under modules_path and add entries to the projects dict.
    Used to populate projects var when mode == 'N'.
    """
    modules = [
        name for name in os.listdir(modules_path)
        if (os.path.isdir(os.path.join(modules_path, name)) and (not name.startswith('__')))
    ]
    for module in modules:
        if not os.path.isfile(os.path.join(modules_path, module, SKIP_ME)):
            projects['stix_shifter_modules_' + module] = ['stix_shifter_modules/' + module]


# ------------------------------------------------------------------------------
# Mode and version determination
# ------------------------------------------------------------------------------


def determine_mode_and_version():
    """
    Determine packaging MODE and VERSION from environment variables.
    Defaults: mode = 'N', version = '1.0.0' (but defaults may be overridden via constants).
    Returns (mode, version_value).
    """
    mode = DEFAULT_MODE
    if 'MODE' in os.environ:
        mode = os.environ['MODE']

    version_value = DEFAULT_VERSION
    if 'VERSION' in os.environ:
        version_value = os.environ['VERSION']

    return mode, version_value


# ------------------------------------------------------------------------------
# Packaging / setup per project
# ------------------------------------------------------------------------------


def collect_packages_for_src_folders(src_folders):
    """
    Build the include patterns and call find_packages.
    Returns the list of packages found.
    """
    packages_include = []
    for src_folder in src_folders:
        packages_include.append(src_folder.replace('/', '.'))
        packages_include.append(src_folder.replace('/', '.') + '.*')
    print('packages_include: %s' % packages_include)
    packages = find_packages(include=packages_include)
    print('packages: %s' % packages)
    return packages


def collect_requirements_for_src_folders(src_folders):
    """
    Walk src_folders to find all requirements.txt files (except when SKIP.ME exists),
    parse them, filter comments and git+ entries, and return a list of unique install_requires.
    """
    install_requires = set()
    requirements_files = []
    for src_folder in src_folders:
        for r, d, f in os.walk(src_folder):
            for file in f:
                if 'requirements.txt' == file and not os.path.isfile(os.path.join(r, SKIP_ME)):
                    requirements_files.append(os.path.join(r, file))
    print('requirements_files: %s' % requirements_files)
    for requirements_file in requirements_files:
        with open(requirements_file, encoding="utf-8") as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]
        lines = list(filter(lambda s: (not s.startswith('#')) and len(s) > 0, lines))
        lines = list(filter(lambda s: (not 'git+' in s) and len(s) > 0, lines))
        install_requires.update(lines)
    install_requires = list(install_requires)
    print('install_requires: %s' % install_requires)
    return install_requires


def collect_entry_points_for_src_folders(project_name, src_folders):
    """
    Search for console script entry points under src_folders/scripts/<src_folder>.py
    and return entry_points dict for setup() (or empty dict if none).
    """
    entry_points_items = []
    for src_folder in src_folders:
        entry_point_path = os.path.join(src_folder, 'scripts', src_folder + '.py')
        if os.path.exists(entry_point_path):
            entry_points_items.append('%s=%s.scripts.%s:main' %
                                      (project_name.replace('_', '-'), project_name, project_name))
    entry_points = {}
    if len(entry_points_items) > 0:
        entry_points = {
            'console_scripts': entry_points_items
        }
    print('entry_points: %s' % entry_points)
    return entry_points

# TODO: This will be removed and instead we will migrate to using generate_pyproject.py
def prepare_setup_params(project_name, version_value, long_description, packages, install_requires, entry_points):
    """
    Prepare the params dict that will be serialized and passed to the external build script.
    """
    params = {
        'name': project_name,  # Required
        'version': version_value,  # Required
        'description': 'Tools and interface to translate STIX formatted results and queries to different data source '
                       + 'formats and to set up appropriate connection strings for invoking and triggering actions '
                       + 'in openwhisk',  # Required
        'long_description': long_description,  # Optional
        'long_description_content_type': 'text/markdown',
        'url': 'https://github.com/opencybersecurityalliance/stix-shifter',  # Optional
        'author': 'ibm',
        'author_email': '',  # Optional
        'classifiers': [  # Optional
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
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
    return params


def prepare_manifest_and_configs(project_name, src_folders, mode_value, tmp_mapping_dir):
    """
    Main function that:
    - Writes MANIFEST.in from template
    - Collects JSON include lines
    - Injects util files when needed
    - Processes configuration directories: merging base JSONs, inserting mapping defaults,
      writing conf/dialects.json, moving configuration directories to temporary dir for packaging,
      and tracking cleanup items and temp dirs.
    Returns:
        cleanup_file_list: list of files/dirs to remove/restore after setup
        temp_dir_list: list of [TemporaryDirectory, module_dir] used to restore configuration later
        json_include_lines: list of 'include <path>' lines to append to MANIFEST.in
    """
    cleanup_file_list = []
    temp_dir_list = []
    json_include_lines = []
    utils_include_list = {
        'stix_shifter_utils/stix_translation/src/json_to_stix/json_to_stix_translator.py':
            '%s/stix_translation/json_to_stix_translator.py'
    }

    module_dir = None

    for json_search_path in src_folders:
        connector_name = ''
        json_search_path_split = json_search_path.split(os.sep)
        if len(json_search_path_split) > 1:
            connector_name = json_search_path_split[1]

        module_dir = json_search_path
        configuration_path = os.path.join(module_dir, 'configuration')
        # If configuration subdirectory exists: merge config files and produce confs
        if os.path.isdir(configuration_path):
            conf_path = os.path.join(module_dir, 'conf')
            shutil.rmtree(conf_path, ignore_errors=True)
            os.mkdir(conf_path)
            # walk configuration_path and merge base + module JSONs
            for r, d, f in os.walk(configuration_path):
                for file in f:
                    configuration_file_path = os.path.join(r, file)
                    with open(configuration_file_path, encoding="utf-8") as json_file:
                        module_data = json.load(json_file)
                    base_data = None
                    data = dict()
                    base_path = os.path.join(r, '..', '..', file)
                    if os.path.isfile(base_path):
                        with open(base_path, encoding="utf-8") as json_file:
                            base_data = json.load(json_file)
                        data = base_data
                    data = merge(module_data, data)
                    # If the file is config.json, insert the mapping default from tmp_mapping_dir
                    if file == 'config.json':
                        mapping_file = os.path.join(tmp_mapping_dir, connector_name + '.json')
                        with open(mapping_file, encoding="utf-8") as f:
                            mapping = json.load(f)
                            data['connection']['options']['mapping']['default'] = mapping
                    json_file_path = os.path.join(r, '..', 'conf', file)
                    with open(json_file_path, 'w') as json_file:
                        json_file.write(json.dumps(data, indent=4, sort_keys=False))
            # generate dialects.json using connector entry point
            connector_module = importlib.import_module("stix_shifter_modules." + connector_name + ".entry_point")
            entry_point = connector_module.EntryPoint()
            dialects_full = entry_point.get_dialects_full()
            with open(os.path.join(conf_path, 'dialects.json'), 'w', encoding="utf-8") as f:
                f.write(json.dumps(dialects_full, indent=4, sort_keys=False))
            # Move the real configuration out temporarily and replace with conf created
            temp_dir = tempfile.TemporaryDirectory()
            temp_dir_list.append([temp_dir, module_dir])
            shutil.move(configuration_path, temp_dir.name)
            os.rename(conf_path, configuration_path)
            cleanup_file_list.append(configuration_path)

        # Inject util files when packaging (when mode != "1")
        if mode_value != "1":
            for util_src, util_dest in utils_include_list.items():
                util_dest = util_dest % module_dir
                if shutil.os.path.exists(util_src) and not shutil.os.path.exists(util_dest):
                    try:
                        shutil.copyfile(util_src, util_dest)
                        cleanup_file_list.append(util_dest)
                    except Exception:
                        # Swallow exceptions during util injection
                        pass

        # Collect JSON include lines for manifest, skipping certain test/tools paths (keeps same filtering)
        for r, d, f in os.walk(module_dir):
            r_split = r.split(os.sep)
            if not (len(r_split) >= 3 and ('tests' == r_split[2] or 'tools' == r_split[2])):
                for file in f:
                    if '.json' in file:
                        json_include_lines.append('include ' + os.path.join(r, file) + ' \n')

    # write/update MANIFEST.in (start from template then append found json includes)
    shutil.rmtree('MANIFEST.in', ignore_errors=True)
    shutil.copyfile('build_templates/MANIFEST.in', 'MANIFEST.in')
    with open('MANIFEST.in', 'a', encoding="utf-8") as out_file:
        out_file.writelines(json_include_lines)

    return cleanup_file_list, temp_dir_list, json_include_lines


def run_setup_and_capture_output(params, additional_args):
    """
    Run the external build script 'build_templates/setup_one.py' with serialized params and
    stream its stdout to the current process stdout.
    """
    proc_params = ['python3', 'build_templates/setup_one.py']
    proc_params.extend(additional_args)
    proc_params.append(json.dumps(params))
    proc = subprocess.Popen(proc_params, stdout=subprocess.PIPE)
    for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
        if not line:
            break
        print(line.rstrip())


def cleanup_after_setup(cleanup_file_list, temp_dir_list, project_name):
    """
    Remove any temporary files and restore the original configuration directories moved to
    TemporaryDirectory objects earlier.
    """
    # Add build artifacts to cleanup list
    cleanup_file_list.extend(['build', 'MANIFEST.in', project_name + '.egg-info'])
    for cleanup_file in cleanup_file_list:
        if os.path.exists(cleanup_file):
            if os.path.isdir(cleanup_file):
                shutil.rmtree(cleanup_file)
            else:
                os.remove(cleanup_file)
    # Restore configuration directories moved into temporary dirs
    for temp_dir, module_dir in temp_dir_list:
        if temp_dir is not None:
            shutil.move(os.path.join(temp_dir.name, 'configuration'), module_dir)
            temp_dir.cleanup()


# ------------------------------------------------------------------------------
# Main processing loop - per project
# ------------------------------------------------------------------------------


def process_projects(projects, version_value, long_description, additional_args, mode_value, tmp_mapping_dir):
    """
    Iterate over each project in the projects mapping and run the full packaging flow
    (collect packages, requirements, entry points; prepare manifest/config; run setup; cleanup).
    """
    for project_name in projects.keys():
        print('processing project_name %s' % project_name)

        src_folders = projects[project_name]

        # Prepare packages
        packages = collect_packages_for_src_folders(src_folders)

        # Prepare install_requires list
        install_requires = collect_requirements_for_src_folders(src_folders)

        # Prepare entry points
        entry_points = collect_entry_points_for_src_folders(project_name, src_folders)

        # Build params for setup
        params = prepare_setup_params(project_name, version_value, long_description, packages,
                                      install_requires, entry_points)

        # Prepare MANIFEST and configuration files; collect cleanup/temp data
        cleanup_file_list, temp_dir_list, _ = prepare_manifest_and_configs(
            project_name, src_folders, mode_value, tmp_mapping_dir
        )

        # Run external setup/build script and stream its output
        run_setup_and_capture_output(params, additional_args)

        # Cleanup and restore moved directories
        cleanup_after_setup(cleanup_file_list, temp_dir_list, project_name)

        print('---------------------------------')


# ------------------------------------------------------------------------------
# Entry point / driver
# ------------------------------------------------------------------------------


def main():
    """
    Main driver that orchestrates the entire script in a readable sequence.
    """
    # Validate Python version
    check_python_version()

    # Generate requirements
    run_generate_requirements()

    # Install dev requirements
    install_dev_requirements()

    # If user only wanted to install requirements, exit early
    if os.getenv('INSTALL_REQUIREMENTS_ONLY', None) == '1':
        exit(0)

    # Read long_description from docs/README.md
    with open(os.path.join(here, 'docs/README.md'), encoding='utf-8') as f:
        long_description = f.read()

    # Prepare temporary mapping directory and write connector mappings into it
    ensure_tmp_mapping_dir()
    generate_connector_mappings(TMP_MAPPING_DIR, MODULES_DIR)

    # Determine mode and version (env override)
    mode_value, version_value = determine_mode_and_version()

    # Decide how projects is structured based on mode
    if mode_value == '1':
        projects = {
            "stix_shifter": [
                'stix_shifter_utils',
                'stix_shifter',
                'stix_shifter_modules'
            ]
        }
    elif mode_value == 'N':
        projects = {
            "stix_shifter_utils": ["stix_shifter_utils"],
            "stix_shifter": ["stix_shifter"]
        }
        fill_connectors(projects, "stix_shifter_modules")
    else:
        module_path = 'stix_shifter_modules/' + mode_value
        if os.path.isdir(module_path):
            projects = {
                "stix_shifter_modules_" + mode_value: [module_path]
            }
        else:
            print('Unexpected value in MODE environment variable: %s' % mode_value)
            print('Allowed values: 1|3|N|module_name')
            exit(1)

    # Pass through command line args to external build script
    additional_args = sys.argv[1:]

    # Process each project (packages, manifest/config handling, build, cleanup)
    process_projects(projects, version_value, long_description, additional_args, mode_value, TMP_MAPPING_DIR)

    # Final cleanup of temporary mapping directory
    shutil.rmtree(TMP_MAPPING_DIR)


if __name__ == '__main__':
    main()
