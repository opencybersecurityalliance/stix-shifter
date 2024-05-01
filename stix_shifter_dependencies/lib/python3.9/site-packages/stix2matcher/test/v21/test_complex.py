from datetime import datetime, timedelta

import pytest

from stix2matcher.matcher import match

_stix_version = '2.1'
_observations = [
    {
        "type": "bundle",
        "id": "bundle--c7011d7f-cda7-4990-85c6-cc232d3c5d00",
        "objects": [
            {
                "id": "observed-data--c15497e0-5436-40bd-b990-52d77300f6b8",
                "type": "observed-data",
                "number_observed": 2,
                "first_observed": "2004-10-11T21:44:58Z",
                "last_observed": "2004-10-11T21:44:58Z",
                "objects": {},
                "object_refs": [
                    "person--3b0c887a-1aac-4514-b3a5-1911622f52f7"
                ],
                "spec_version": "2.1"
            },
            {
                "type": "person",
                "name": "alice",
                "age": 10,
                "id": "person--3b0c887a-1aac-4514-b3a5-1911622f52f7"
            }
        ]
    },
    {
        "type": "bundle",
        "id": "bundle--9461ed04-4358-4646-954f-4c1290857f8d",
        "objects": [
            {
                "id": "observed-data--3ecdd013-ffe5-4aae-b973-ab4cf41eaf1d",
                "type": "observed-data",
                "number_observed": 3,
                "first_observed": "2004-10-11T21:45:01Z",
                "last_observed": "2004-10-11T21:45:01Z",
                "objects": {},
                "object_refs": [
                    "person--2e048392-6aac-49b3-aba4-21e4a6de6e10"
                ],
                "spec_version": "2.1"
            },
            {
                "type": "person",
                "name": "bob",
                "age": 17,
                "id": "person--2e048392-6aac-49b3-aba4-21e4a6de6e10"
            }
        ]
    },
    {
        "type": "bundle",
        "id": "bundle--c21c91b4-b316-41db-92f9-fa8c17e42d62",
        "objects": [
            {
                "id": "observed-data--8f405559-9f1d-4e14-9411-3787c22b9690",
                "type": "observed-data",
                "number_observed": 2,
                "first_observed": "2004-10-11T21:45:02Z",
                "last_observed": "2004-10-11T21:45:02Z",
                "object_refs": [
                    "person--16170c30-f1e2-4453-bb3f-686830198acf"
                ],
                "spec_version": "2.1"
            },
            {
                "type": "person",
                "name": "carol",
                "age": 22,
                "id": "person--16170c30-f1e2-4453-bb3f-686830198acf"
            }
        ]
    }
]


# These SDOs have number_observed > 1; these patterns require contributions
# of several observations from several SDOs to satisfy.
@pytest.mark.parametrize("pattern", [
    "[person:age < 20] REPEATS 5 TIMES",
    "[person:age < 20] REPEATS 2 TIMES REPEATS 2 TIMES",
    "[person:name > 'aaron'] REPEATS 5 TIMES WITHIN 1 SECONDS",
    "([person:age < 30] AND [person:name > 'aaron']) WITHIN 2 SECONDS REPEATS 3 TIMES",
])
def test_complex_match(pattern):
    assert match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    "[person:age < 20] REPEATS 10 TIMES",
    "[person:age < 20] REPEATS 2 TIMES REPEATS 3 TIMES"
])
def test_complex_nomatch(pattern):
    assert not match(pattern, _observations, stix_version=_stix_version)


_observations_combinatorial_explosion = []
for i in range(20):
    time = datetime(2004, 10, 11, 21, 44, 58) + timedelta(seconds=i)
    time_str = time.isoformat("T") + "Z"
    _observations_combinatorial_explosion.append(
        {
            "type": "observed-data",
            "first_observed": time_str,
            "last_observed": time_str,
            "number_observed": 1,
            "objects": {
                "a0": {
                    "type": u"person",
                    "name": u"alice",
                    "age": i % 20
                }
            }
        }
    )


@pytest.mark.parametrize("pattern", [
    "[person:age < 20] REPEATS 10 TIMES",
    "[person:age < 20] REPEATS 10 TIMES WITHIN 10 SECONDS",
    "[person:age < 20] REPEATS 10 TIMES START '2004-10-11T21:40:00Z' STOP '2004-10-11T21:50:00Z'",
    "[person:age < 20] REPEATS 10 TIMES AND [person:age < 20]",
    "[person:age < 20] REPEATS 10 TIMES OR [person:age < 20]",
    "[person:age < 20] REPEATS 10 TIMES FOLLOWEDBY [person:age < 20]",
    "[person:age < 20] REPEATS 5 TIMES REPEATS 2 TIMES",
    "[person:age < 20] REPEATS 2 TIMES REPEATS 5 TIMES",
    " AND ".join("[person:age < 20]" for _ in range(10)),
    " OR ".join("[person:age < 20]" for _ in range(10)),
    "([person:age < 20] FOLLOWEDBY [person:age > 5]) REPEATS 10 TIMES",
])
def test_combinatorial_explosion_match(pattern):
    assert match(pattern, _observations_combinatorial_explosion)


@pytest.mark.parametrize("pattern", [
    "[person:age < 20] REPEATS 10 TIMES WITHIN 8 SECONDS",
])
def test_combinatorial_explosion_nomatch(pattern):
    assert not match(pattern, _observations_combinatorial_explosion)
