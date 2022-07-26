# Changelog Generator

This script generates a list of GitHub commits between a specified release tag and the develop branch and adds them to the [CHANGELOG.md](https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/CHANGELOG.md) file. 

### Usage

Navigate to the `stix_shifter/scripts/changelog_generator` directory and run `./generate_changelog.sh <last_release_tag> <new_release_tag>`

Example:

```
./generate_changelog.sh 4.1.0 4.1.2
```