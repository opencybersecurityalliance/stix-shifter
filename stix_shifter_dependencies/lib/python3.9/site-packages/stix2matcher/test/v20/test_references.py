import pytest

from stix2matcher.matcher import match

_stix_version = '2.0'
_observations = [
    {
        "type": "observed-data",
        "number_observed": 1,
        "first_observed": "1984-06-26T13:53:04Z",
        "last_observed": "1984-06-26T13:53:04Z",
        "objects": {
            "0": {
                "type": "person",
                "name": "alice",
                "knows_ref": u"1"
            },
            "1": {
                "type": "person",
                "name": "bob",
                "knows_refs": [u"0", u"2"]
            },
            "2": {
                "type": "person",
                "name": "carol",
                "knows_refs": [u"0", u"1", u"2"]
            }
        }
    }
]


@pytest.mark.parametrize("pattern", [
    "[person:knows_ref.name = 'bob']",
    "[person:knows_refs[*].name = 'alice' OR person:knows_ref.name = 'darlene']",
    "[person:knows_refs[*].name = 'carol' AND person:knows_refs[*].name = 'bob']",
    "[person:knows_refs[*].knows_refs[*].name = 'alice']"
])
def test_references_match(pattern):
    assert match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    "[person:knows_ref.name = 'erin']",
    "[person:knows_refs[*].name = 'alice' AND person:knows_ref.name = 'darlene']",
    "[person:knows_refs[*].name = 'erin' OR person:knows_refs[*].name = 'darlene']"
])
def test_references_nomatch(pattern):
    assert not match(pattern, _observations, stix_version=_stix_version)
