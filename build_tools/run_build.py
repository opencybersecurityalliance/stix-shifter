import os
import sys
import subprocess

from pathlib import Path
from .logging_setup import get_logger, init_logging
from .pre_build import main as pre_build_main


# Initialise logging once at program start (respects LOG_LEVEL env)
init_logging()
logger = get_logger("run_build")


def main():
    # Check if install present in arguments, set flag if true
    additional_args = sys.argv[1:]
    do_install = False
    if 'install' in additional_args:
        additional_args.remove('install')
        do_install = True

    # Prepare the build, i.e., install requirements
    logger.info("Running STIX-Shifter's pre-build (i.e., acquiring requirements)")

    try:
        pre_build_main()
    except Exception as e:
        logger.critical("Pre-build failed: %s", e, exc_info=True)
        sys.exit(1)

    # If only installing requirements, exit early
    if os.getenv('INSTALL_REQUIREMENTS_ONLY', None) == '1':
        logger.info("INSTALL_REQUIREMENTS_ONLY set; exiting after pre-build.")
        sys.exit(0)
    
    # Import build_main only after pre_build has run and dependencies are installed
    try:
        from .build import main as build_main
    except ModuleNotFoundError as e:
        logger.critical("Build module not found: %s", e, exc_info=True)
        sys.exit(1)

    # Run the actual build
    logger.info("Running STIX-Shifter's main build")
    try:
        build_main(additional_args)
    except Exception as e:
        logger.critical("Main build failed: %s", e, exc_info=True)
        sys.exit(1)

    # Install via pip the wheels we compiled in ./dist (if "install" was present in args)
    if do_install:
        logger.info("Installing wheels that were output to ./dist")

        dist_dir = Path(__file__).parent.parent / "dist"
        for whl_path in dist_dir.glob("*.whl"):
            subprocess.run([sys.executable, "-m", "pip", "install", str(whl_path)], check=True)

    logger.info("Build completed successfully.")


if __name__ == "__main__":
    main()
