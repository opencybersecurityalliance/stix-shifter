import pytest
from stix2patterns.pattern import ParseException

from stix2matcher.matcher import match

_stix_version = '2.1'
_observations = [
    {
        "type": "bundle",
        "id": "bundle--f9005c40-956b-4c5f-87ea-388fb7b198e4",
        "objects": [
            {
                "id": "observed-data--50af521a-236d-4cd5-b318-11c517450daf",
                "type": "observed-data",
                "number_observed": 1,
                "first_observed": "2004-10-11T21:44:58Z",
                "last_observed": "2004-10-11T21:44:58Z",
                "object_refs": [
                    "some-type--83916b58-850f-43f8-bd1b-4ac8847e35e6"
                ],
                "spec_version": "2.1"
            },
            {
                "type": "some-type",
                "has-hyphen": 1,
                "has.dot": 2,
                "has-hyphen.dot": 3,
                "id": "some-type--83916b58-850f-43f8-bd1b-4ac8847e35e6"
            }
        ]
    }
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
