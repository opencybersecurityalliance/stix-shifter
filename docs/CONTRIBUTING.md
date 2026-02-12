# Contributing

## <a id="openParticipation">Public Participation Invited</a>

The Open Cybersecurity Alliance (OCA) is an [OASIS Open Project](https://oasis-open-projects.org/) and welcomes participation by anyone, whether affiliated with OASIS or not.  Substantive contributions and feedback are invited from all parties, following the common conventions for participation in GitHub public repository projects.  

Participation is expected to be consistent with the [Code of Conduct](https://github.com/opencybersecurityalliance/oca-admin/blob/master/CODE_OF_CONDUCT.md), the [licenses](https://github.com/opencybersecurityalliance/oca-admin/blob/master/LICENSE.md), and the acceptance of our [individual Contributor License Agreement](https://cla-assistant.io/opencybersecurityalliance/oasis-open-project), generally at the time of first contribution.

## <a id="development">Development Workflow</a>

### Running Tests Locally

Before submitting a pull request, run the CI test suite locally to ensure your changes pass all checks:

```bash
# Quick test with your current Python version
./run_ci_tests.sh

# Comprehensive test across Python 3.10, 3.11, and 3.12 (requires pyenv)
./run_ci_tests.sh --all-versions
```

The CI script runs the same checks as GitHub Actions:
1. Generates consolidated requirements
2. Installs dependencies
3. Runs flake8 linting (syntax errors and style warnings)
4. Executes the full pytest test suite

**Note**: The `--all-versions` flag requires Python 3.10, 3.11, and 3.12 to be installed via pyenv. Install missing versions with:
```bash
pyenv install 3.11.11
pyenv install 3.12.8
```

### Testing Individual Connectors

To test a specific connector module:

```bash
pytest stix_shifter_modules/<module-name>/tests/ -vv
```

For more development commands and guidance, see [CLAUDE.md](../CLAUDE.md).

## <a id="feedback">Feedback</a>

Questions or comments about the OCA's activities may be composed as GitHub issues or comments or may be directed to the project's general email list at oca@lists.oasis-open-projects.org. General questions about OASIS Open Projects may be directed to OASIS staff at op-admin@lists.oasis-open-projects.org
