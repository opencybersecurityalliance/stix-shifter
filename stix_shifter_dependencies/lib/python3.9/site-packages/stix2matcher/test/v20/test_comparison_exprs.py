import pytest

from stix2matcher.matcher import match

_stix_version = '2.0'
_observations = [
    {
        "type": "observed-data",
        "number_observed": 1,
        "first_observed": "2004-11-26T11:42:29Z",
        "last_observed": "2004-11-26T11:42:29Z",
        "objects": {
            "0": {
                "type": u"person",
                "name": u"alice",
                "age": 10
            },
            "1": {
                "type": u"person",
                "name": u"bob",
                "age": 15
            }
        }
    }
]


@pytest.mark.parametrize("pattern", [
    "[person:name = 'alice' AND person:age < 20]",
    "[person:name = 'alice' OR person:age > 20]",
    "[person:name = 'alice' OR person:age > 1000 AND person:age < 0]",
    "[(person:name = 'carol' OR person:name = 'bob') AND person:age > 10]",
    "[(person:name = 'darlene' OR person:name = 'carol') AND person:age < 0 OR person:age > 5]"
])
def test_comparison_and_or_match(pattern):
    assert match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    "[person:name = 'alice' AND person:age > 10]",
    "[person:name = 'carol' OR person:age > 20]",
    "[(person:age = 'alice' OR person:age > 1000) AND person:age < 0]",
    "[(person:name = 'darlene' OR person:name = 'carol') AND (person:age < 0 OR person:age > 5)]"
])
def test_comparison_and_or_nomatch(pattern):
    assert not match(pattern, _observations, stix_version=_stix_version)
