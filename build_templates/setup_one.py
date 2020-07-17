"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup
import sys
import json

if __name__ == "__main__":
    if len(sys.argv) > 2:
        params = json.loads(sys.argv[-1])
        sys.argv = sys.argv[:-1]
        setup(**params)
