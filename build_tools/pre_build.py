import os
import sys
import subprocess

from .logging_setup import get_logger, is_debug


logger = get_logger("pre_build")


class PreBuildError(RuntimeError):
    """Raised when a pre-build step fails."""


def _check_python_version():
    """
    Ensure Python interpreter is 3.10 or greater. If not, print an error and exit.
    """
    if sys.version_info.major == 3 and sys.version_info.minor >= 10:
        logger.info(f"Python version {sys.version} OK")
    else:
        logger.critical("Error: Python 3.10 or greater is required")
        raise PreBuildError(f"Python 3.10 or greater is required (found {sys.version})")


def _generate_requirements():
    """
    Compile requirements.txt consisting of requirements defined across listed src_folders.
    """
    src_folders = ["stix_shifter_utils", "stix_shifter", "stix_shifter_modules"]
    install_requires = set()
    requirements_files = []

    for src_folder in src_folders:
        for r, d, f in os.walk(src_folder):
            for file in f:
                if 'requirements.txt'==file and not os.path.isfile(os.path.join(r, 'SKIP.ME')):
                    requirements_files.append(os.path.join(r, file))

    logger.info('requirements_files: %s' % requirements_files)

    for requirements_file in requirements_files:
        with open(requirements_file) as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]
        lines = list(filter(lambda s: len(s)>0, lines))
        install_requires.update(lines)

    install_requires = list(install_requires)
    install_requires.sort()

    logger.info('install_requires: %s' % install_requires)

    with open('requirements.txt', 'w') as out_file:
        for item in install_requires:
            out_file.write(item)
            out_file.write('\n')


def _install_dev_requirements():
    """
    Install development requirements via pip using requirements-dev.txt.
    Shows full pip output if debug mode is enabled; otherwise, hides output unless there's an error.
    Raises PreBuildError on failure.
    """
    cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"]

    if is_debug():
        # Show pip output directly
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as exc:
            raise PreBuildError(f"pip install failed: {exc}") from exc
    else:
        # Capture output, only log if there is an error
        try:
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            logger.info("Dev requirements installed successfully.")
        except subprocess.CalledProcessError as exc:
            out = (exc.stdout or "").strip()
            err = (exc.stderr or "").strip()
            msg = (
                f"Failed to install dev requirements ({' '.join(cmd)}). "
                f"Return code: {exc.returncode}\nSTDOUT: {out}\nSTDERR: {err}"
            )
            raise PreBuildError(msg) from exc


def main():
    _check_python_version()
    _generate_requirements()
    _install_dev_requirements()

if __name__ == "__main__":
    main()
