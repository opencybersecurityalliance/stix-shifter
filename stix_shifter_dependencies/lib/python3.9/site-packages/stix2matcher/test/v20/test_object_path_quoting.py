import pytest
from stix2patterns.pattern import ParseException

from stix2matcher.matcher import match

_stix_version = '2.0'
_observations = [
    {
        "type": "observed-data",
        "first_observed": "2004-10-11T21:44:58Z",
        "last_observed": "2004-10-11T21:44:58Z",
        "number_observed": 1,
        "objects": {
            "0": {
                "type": u"some-type",
                "has-hyphen": 1,
                "has.dot": 2,
                "has-hyphen.dot": 3
            }
        }
    },
]


@pytest.mark.parametrize("pattern", [
    "[some-type:'has-hyphen' = 1]",
    "[some-type:'has.dot' = 2]",
    "[some-type:'has-hyphen.dot' = 3]"
])
def test_quoting(pattern):
    assert match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    "[some-type:needs-quotes = 1]"
])
def test_quoting_error(pattern):
    with pytest.raises(ParseException):
        match(pattern, _observations, stix_version=_stix_version)
