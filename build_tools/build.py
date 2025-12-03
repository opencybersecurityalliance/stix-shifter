import os
import subprocess
import sys
import shutil
import json
import io
import tempfile
import importlib

# To use a consistent encoding
from codecs import open
from typing import List, Tuple
from pathlib import Path
from jsonmerge import merge
from setuptools import find_packages

from .logging_setup import get_logger, is_debug
from .generate_pyproject import generate_pyproject_from_values


# Constants used across the script
SKIP_ME = 'SKIP.ME'
TMP_MAPPING_DIR = 'tmp_mapping'
MODULES_DIR = 'stix_shifter_modules'
# DO NOT remove spaces around the equal sign at the line below
DEFAULT_VERSION = '1.0.0'
DEFAULT_MODE = 'N'

PACKAGE_ROOT = Path(__file__).resolve().parent  # build_tools/
PROJECT_ROOT = PACKAGE_ROOT.parent              # project/
TEMPLATES_DIR = PROJECT_ROOT / "build_templates"
README_PATH = "docs/README.md"

OUT_DIR = "dist"
TEMP_DIR = "_temp"


logger = get_logger("build")


# ------------------------------------------------------------------------------
# Low-level utility functions
# ------------------------------------------------------------------------------


def _ensure_tmp_mapping_dir() -> Path:
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


def _generate_connector_mappings(tmp_mapping_dir=TMP_MAPPING_DIR, modules_dir=MODULES_DIR):
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
            logger.info(f"Processing mapping for {module}...")
            connector_module = importlib.import_module(f"stix_shifter_modules.{module}.entry_point")
            entry_point = connector_module.EntryPoint()
            mapping = entry_point.get_mapping()
            out_path = os.path.join(tmp_mapping_dir, module + '.json')
            with open(out_path, 'w', encoding="utf-8") as f:
                json.dump(mapping, f, sort_keys=False, indent=4)


# ------------------------------------------------------------------------------
# Project population helpers
# ------------------------------------------------------------------------------


def _fill_connectors(projects, modules_path):
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


def _determine_mode_and_version() -> Tuple[str, str]:
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
# Helpers for populating temporary project directories
# ------------------------------------------------------------------------------


def _copy_shared_files(destination_dir: Path):
    """
    Copy essential shared files into the module build directory.

    Behaviour:
      - This function depends on hard-coded paths
        - i.e., expects MANIFEST, LICENSE, NOTICE, AUTHORS in PROJECT_ROOT
          expects shared README file in docs folder
      - Will raise exception if files are not found
      - README is copied from PROJECT_ROOT/docs/README.md to destination_dir.
      - Other shared files (MANIFEST.in, LICENSE.md, NOTICE, AUTHORS.md) are
        copied as-is, relative to PROJECT_ROOT.
    """
    destination_dir = Path(destination_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)

    shared_files = ["MANIFEST.in", "LICENSE.md", "NOTICE", "AUTHORS.md"]
    readme_src = PROJECT_ROOT / README_PATH

    # Copy shared files
    for file_name in shared_files:
        src = PROJECT_ROOT / file_name
        dest = destination_dir / file_name
        if src.exists():
            shutil.copy(src, dest)
            logger.debug("Copied shared file: %s -> %s", src, dest)
        else:
            logger.warning("Shared file not found, skipping: %s", src)
            raise FileNotFoundError(f"Shared file not found: {src}")

    # Copy README
    if readme_src.exists():
        dest = destination_dir / "README.md"
        shutil.copy(readme_src, dest)
        logger.debug("Copied README -> %s", dest)
    else:
        logger.warning("README not found: %s", readme_src)
        raise FileNotFoundError(f"README not found: {readme_src}")


def _copy_src_folders_to_dir(src_folders: list[str], project_build_dir: Path):
    """
    Copy each src_folder into project_build_dir, preserving the full path hierarchy
    of each source folder relative to PROJECT_ROOT.

    Args:
        src_folders: list of source folder paths (list[str]), relative to PROJECT_ROOT.
        project_build_dir: Path to the temporary build directory.
    """
    project_build_dir = Path(project_build_dir)
    logger.info("Copying %d source folders into %s", len(src_folders), project_build_dir)

    for src in src_folders:
        src_path = (PROJECT_ROOT / src).resolve()
        if not src_path.exists():
            logger.warning("Source folder not found, skipping: %s", src_path)
            raise FileNotFoundError(f"Source folder not found, skipping: {src_path}")

        # Compute destination path: preserve hierarchy relative to PROJECT_ROOT
        rel_path = src_path.relative_to(PROJECT_ROOT)
        dest = project_build_dir / rel_path

        # Make parent directories as needed
        os.makedirs(os.path.dirname(dest), exist_ok=True)

        shutil.copytree(src_path, dest, dirs_exist_ok=True)
        logger.debug("Copied %s -> %s", src_path, dest)


# ------------------------------------------------------------------------------
# Project packaging and setup
# ------------------------------------------------------------------------------


def _collect_packages_for_src_folders(src_folders) -> list[str]:
    """
    Build the include patterns and call find_packages.
    Returns the list of packages found.
    """
    packages_include = []

    for src_folder in src_folders:
        packages_include.append(src_folder.replace('/', '.'))
        packages_include.append(src_folder.replace('/', '.') + '.*')
    packages = find_packages(include=packages_include)

    logger.debug('packages_include: %s' % packages_include)
    logger.debug('packages: %s' % packages)

    return packages


def _collect_requirements_for_src_folders(src_folders) -> list[str]:
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
    logger.debug('requirements_files: %s' % requirements_files)
    for requirements_file in requirements_files:
        with open(requirements_file, encoding="utf-8") as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]
        lines = list(filter(lambda s: (not s.startswith('#')) and len(s) > 0, lines))
        lines = list(filter(lambda s: (not 'git+' in s) and len(s) > 0, lines))
        install_requires.update(lines)
    install_requires = list(install_requires)
    logger.debug('install_requires: %s' % install_requires)
    return install_requires


def _collect_entry_points_for_src_folders(project_name, src_folders) -> dict[str, list]:
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
    logger.debug('entry_points: %s' % entry_points)
    return entry_points


# NOTE: could be replaced by hard-coding directly into pyproject.template.toml
def _get_hardcoded_metadata() -> dict[str, str]:
    """
    Hard-coded metadata to add to pyproject.toml
    """
    params = {
        'description': 'Tools and interface to translate STIX formatted results and queries to different data source '
                       + 'formats and to set up appropriate connection strings for invoking and triggering actions '
                       + 'in openwhisk',  # Required
        'author': 'ibm',
        'author_email': '',  # Optional
    }
    return params


def _prepare_manifest_and_configs(project_name, src_folders, mode_value, tmp_mapping_dir) -> tuple[list, list, list]:
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


# ------------------------------------------------------------------------------
# Main processing loop - per project
# ------------------------------------------------------------------------------


def _run_build(
    *,
    params: dict,
    additional_args: List[str] | None = None,
    src_folders: List[str],
    project_name: str,
    packages: List[str],
    install_requires: List[str],
    entry_points: dict | None = None,
    version: str,
    debug_keep_temp: bool = False,
    build_no_isolation: bool = False,
) -> List[Path]:
    """
    Returns:
        A list of Path objects pointing to created wheel files (in `out_dir`).

    Args:
        additional_args: extra arguments to pass through to the build command.
        params: hardcoded metadata containing description, author details.
        src_folders: src_folders to be included in project package.
        project_name: name of project being build.
        packages: a list of package dotted names that helps build [tool.setuptools.packages.find] include.
        install_requires: iterable of dependency strings (e.g. ["requests>=2.28"])
        entry_points: A mapping of entry-point groups
        version: projects version number
        debug_keep_temp: if True, preserves the temporary build directory for inspection.
        build_no_isolation: toggles --no-isolation flag, defaults to True.
    """
    # Resolve paths, create directories, gather template
    temp_parent = PROJECT_ROOT / TEMP_DIR
    temp_parent.mkdir(parents=True, exist_ok=True)
    out_dir = PROJECT_ROOT / OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    pyproject_template_path = TEMPLATES_DIR / "pyproject.template.toml"
    if not pyproject_template_path.exists():
        raise FileNotFoundError(f"pyproject template not found: {pyproject_template_path}")

    logger.info(f"Building {project_name} ...")
    logger.debug("temp_parent_dir=%s", temp_parent)
    logger.debug("out_dir=%s", out_dir)

    wheel_paths: List[Path] = []

    # Use context manager so tmp cleaned automatically unless we keep it for debug
    with tempfile.TemporaryDirectory(dir=str(temp_parent)) as tmp_dir:
        project_build_dir = Path(tmp_dir)
        logger.info("Temporary build dir: %s", project_build_dir)

        _copy_src_folders_to_dir(src_folders, project_build_dir) 
        _copy_shared_files(project_build_dir)

        # generate pyproject.toml; exceptions may bubble up
        generate_pyproject_from_values(
            template_path=str(pyproject_template_path),
            target_dir=str(project_build_dir),
            package_name=project_name,
            version=version,
            description=params.get("description", ""),
            author=params.get("author", "IBM"),
            author_email=params.get("author_email", ""),
            license_text=params.get("license_text", "Apache-2.0"),
            dependencies=list(install_requires),
            packages_list=list(packages),
            entry_points=entry_points or {},
        )

        # Creating build command, i.e., python -m build --wheel --outdir ...
        cmd = [
            sys.executable, "-m", "build", "--wheel",
            "--outdir", str(out_dir),
        ]

        if build_no_isolation:
            cmd.append("--no-isolation")

        cmd.append(str(project_build_dir))

        if additional_args:
            cmd.extend(additional_args)

        # Use subprocess.run to capture output (avoid blocking reads)
        logger.info("Running build command: %s", " ".join(cmd))
        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
                cwd=str(project_build_dir),
                timeout=600,
            )
        except subprocess.CalledProcessError as e:
            logger.error("Build failed (exit %s).", e.returncode)
            if debug_keep_temp:
                logger.info("Preserving temp build dir for inspection: %s", project_build_dir)
                preserved = temp_parent / f"preserved_{project_name}_{project_build_dir.name}"
                shutil.copytree(project_build_dir, preserved, dirs_exist_ok=True)
                logger.info("Copied preserved build dir to %s", preserved)
            raise

        # log build output at debug level
        logger.debug("Build output:\n%s", result.stdout)
        logger.debug("Build errors:\n%s", result.stderr)

        # Find wheels in out_dir and return list
        for p in out_dir.glob("*.whl"):
            wheel_paths.append(p.resolve())

        if not wheel_paths:
            logger.warning("No wheels produced in %s; contents: %s", out_dir, list(out_dir.iterdir()))

        # If debug_keep_temp requested, preserve temp build directory
        if debug_keep_temp:
            # Create the top-level folder for this project inside temp_parent
            project_folder = temp_parent / project_name
            project_folder.mkdir(parents=True, exist_ok=True)

            # Copy the build directory inside the project folder
            destination = project_folder / project_build_dir.name
            shutil.copytree(project_build_dir, destination, dirs_exist_ok=True)

            logger.info("Preserved temporary build directory at %s", destination)

    # end with TemporaryDirectory cleaned up (unless copied to preserved_*)
    logger.info("Wheels placed in: %s", out_dir)
    return wheel_paths


def _cleanup_after_setup(cleanup_file_list, temp_dir_list, project_name):
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


def _process_projects(projects, version_value, additional_args, mode_value, tmp_mapping_dir):
    """
    Iterate over each project in the projects mapping and run the full packaging flow
    (collect packages, requirements, entry points; prepare manifest/config; run build; cleanup).
    """
    for project_name in projects.keys():
        print("~" * 50)
        logger.info("Building: %s", project_name)

        src_folders = projects[project_name]

        # Prepare packages
        packages = _collect_packages_for_src_folders(src_folders)

        # Prepare install_requires list
        install_requires = _collect_requirements_for_src_folders(src_folders)

        # Prepare entry points
        entry_points = _collect_entry_points_for_src_folders(project_name, src_folders)

        # Build params for setup
        params = _get_hardcoded_metadata()

        # Prepare MANIFEST and configuration files; collect cleanup/temp data
        cleanup_file_list, temp_dir_list, _ = _prepare_manifest_and_configs(
            project_name, src_folders, mode_value, tmp_mapping_dir
        )

        _run_build(
            params=params,
            additional_args=additional_args,
            src_folders=src_folders,
            project_name=project_name,
            packages=packages,
            install_requires=install_requires,
            entry_points=entry_points,
            version=version_value,
        )

        # Cleanup and restore moved directories
        _cleanup_after_setup(cleanup_file_list, temp_dir_list, project_name)

        logger.info("Completed: %s", project_name)
        print("~" * 50)


# ------------------------------------------------------------------------------
# Entry point / driver
# ------------------------------------------------------------------------------


def main(additional_args=None):
    """
    Main driver that orchestrates the entire script in a readable sequence.
    """
    try:
        _ensure_tmp_mapping_dir()
        _generate_connector_mappings(TMP_MAPPING_DIR, MODULES_DIR)

        mode_value, version_value = _determine_mode_and_version()

        # Decide project structure
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
            _fill_connectors(projects, "stix_shifter_modules")
        else:
            module_path = 'stix_shifter_modules/' + mode_value
            if os.path.isdir(module_path):
                projects = {
                    "stix_shifter_modules_" + mode_value: [module_path]
                }
            else:
                raise ValueError(
                    f"Unexpected value in MODE environment variable: {mode_value}. Allowed values: 1|3|N|module_name"
                )

        print("=" * 50)
        _process_projects(projects, version_value, additional_args, mode_value, TMP_MAPPING_DIR)
        print("=" * 50)

    finally:
        if os.path.exists(TMP_MAPPING_DIR):
            shutil.rmtree(TMP_MAPPING_DIR)


if __name__ == '__main__':
    main()
