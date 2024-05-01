import pytest

from stix2matcher.matcher import match

_stix_version = '2.1'
_observations = [
    {
        "type": "bundle",
        "id": "bundle--276d1378-9999-478d-9d95-890923b83afe",
        "objects": [
            {
                "id": "observed-data--0d79fc02-e24c-427e-bdcb-e82960f80ac3",
                "type": "observed-data",
                "number_observed": 1,
                "first_observed": "2004-10-11T21:44:58Z",
                "last_observed": "2004-10-11T21:44:58Z",
                "object_refs": [
                    "person--8d3c710f-6890-4fe0-912c-6413ecf7a69f"
                ],
                "spec_version": "2.1"
            },
            {
                "type": "person",
                "name": "alice",
                "age": 10,
                "id": "person--8d3c710f-6890-4fe0-912c-6413ecf7a69f"
            }
        ]
    },
    {
        "type": "bundle",
        "id": "bundle--48a70a11-352e-4326-8209-33d78b16630e",
        "objects": [
            {
                "id": "observed-data--cce88c5f-dd5b-4260-837d-ed3545d14d8f",
                "type": "observed-data",
                "number_observed": 1,
                "first_observed": "2008-05-09T01:21:58.6Z",
                "last_observed": "2008-05-09T01:21:58.6Z",
                "object_refs": [
                    "person--0e6f880c-6db6-4bba-887b-8125fde272ce"
                ],
                "spec_version": "2.1"
            },
            {
                "type": "person",
                "name": "bob",
                "age": 17,
                "id": "person--0e6f880c-6db6-4bba-887b-8125fde272ce"
            }
        ]
    },
    {
        "type": "bundle",
        "id": "bundle--3f071c17-9d97-4caf-b067-c73b8af2bfc5",
        "objects": [
            {
                "id": "observed-data--1f875b50-eb3e-4f0f-84cc-e86a3ddc79a7",
                "type": "observed-data",
                "number_observed": 1,
                "first_observed": "2006-11-03T07:42:18.96Z",
                "last_observed": "2006-11-03T07:42:18.96Z",
                "object_refs": [
                    "person--82a1b41b-e162-47ab-bb83-2136293f12b5"
                ],
                "spec_version": "2.1"
            },
            {
                "type": "person",
                "name": "carol",
                "age": 22,
                "id": "person--82a1b41b-e162-47ab-bb83-2136293f12b5"
            }
        ]
    }
]


@pytest.mark.parametrize("pattern", [
    "[person:name='alice'] AND [person:age>20]",
    "[person:name='alice'] OR [person:name='carol']",
    "[person:name='alice'] OR [person:name='zelda']",
    "[person:age>10] OR [person:name='bob'] OR [person:name>'amber']",
    "[person:name='alice'] FOLLOWEDBY [person:name>'bill']",
    "[person:age > 20] OR ([person:name > 'zelda'] FOLLOWEDBY [person:age < 0])",
    "[person:age > 20] OR [person:name > 'zelda'] AND [person:age < 0]",
    "([person:name='carol'] FOLLOWEDBY [person:name < 'elizabeth']) AND [person:age < 15]"
])
def test_observation_ops_match(pattern):
    assert match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    "[person:name='alice'] AND [person:name='zelda']",
    "[person:name='alice'] AND [person:age=10]",
    "[person:name='alice'] FOLLOWEDBY [person:age=10]",
    "[person:name='mary'] OR [person:name='zelda']",
    "[person:age > 70] OR [person:name > 'zelda'] AND [person:name MATCHES '^...?$']",
    "[person:name='bob'] FOLLOWEDBY [person:age<15]",
    "[person:age > 20] OR [person:name > 'zelda'] FOLLOWEDBY [person:age < 0]",
    "([person:age > 20] OR [person:name > 'zelda']) AND [person:age < 0]",
    "[person:name='carol'] FOLLOWEDBY [person:name < 'elizabeth'] AND [person:age < 15]"
])
def test_observation_ops_nomatch(pattern):
    assert not match(pattern, _observations, stix_version=_stix_version)
