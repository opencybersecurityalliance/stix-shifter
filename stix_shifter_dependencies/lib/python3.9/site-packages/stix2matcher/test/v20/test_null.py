import pytest
from stix2patterns.pattern import ParseException

from stix2matcher.matcher import match

_stix_version = '2.0'
_observations = [
    {
        "type": "observed-data",
        "first_observed": "2005-10-09T21:44:58Z",
        "last_observed": "2005-10-09T21:44:58Z",
        "number_observed": 1,
        "objects": {
            "0": {
                "type": "null_test",
                "name": None
            }
        }
    }
]


@pytest.mark.parametrize("pattern", [
    "[null_test:name > 'alice']",
    "[null_test:name <= 'alice']",
    "[null_test:name = 'alice']",
    "[null_test:name IN ('alice', 'bob', 'carol')]",
    "[null_test:name LIKE 'alice']",
    "[null_test:name MATCHES 'alice']",
    "[null_test:name ISSUBSET '12.23.32.12/14']",
    "[null_test:name ISSUPERSET '12.23.32.12/14']"
])
def test_null_json(pattern):
    assert not match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    "[null_test:name != 'alice']"
])
def test_notequal_null_json(pattern):
    assert match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    "[null_test:name = null]",
    "[null_test:name IN (null, null, null)]",
    "[null_test:name LIKE null]",
    "[null_test:name MATCHES null]",
    "[null_test:name ISSUBSET null]",
    "[null_test:name ISSUPERSET null]"
])
def test_null_pattern(pattern):
    with pytest.raises(ParseException):
        match(pattern, _observations, stix_version=_stix_version)
