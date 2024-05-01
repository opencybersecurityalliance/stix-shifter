import pytest

from stix2matcher.matcher import match

_stix_version = '2.1'
_observations = [
    {
        "type": "bundle",
        "id": "bundle--87475336-5492-4048-a5c4-2b87dc10fb46",
        "objects": [
            {
                "id": "observed-data--0b083894-21c0-433f-b924-7ea8e9bac52f",
                "type": "observed-data",
                "number_observed": 1,
                "first_observed": "2004-11-26T11:42:29Z",
                "last_observed": "2004-11-26T11:42:29Z",
                "object_refs": [
                    "person--43222df8-0c40-463b-aeae-95b1cb6f4859",
                    "person--3b50f568-ded0-433b-9995-9f538345f726"
                ],
                "spec_version": "2.1"
            },
            {
                "type": "person",
                "name": "alice",
                "age": 10,
                "id": "person--43222df8-0c40-463b-aeae-95b1cb6f4859"
            },
            {
                "type": "person",
                "name": "bob",
                "age": 15,
                "id": "person--3b50f568-ded0-433b-9995-9f538345f726"
            }
        ]
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
