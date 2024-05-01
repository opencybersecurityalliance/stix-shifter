from datetime import datetime, timedelta

import pytest

from stix2matcher.matcher import match

_stix_version = '2.0'
_observations = [
    {
        "type": "observed-data",
        "first_observed": "2004-10-11T21:44:58Z",
        "last_observed": "2004-10-11T21:44:58Z",
        "number_observed": 2,
        "objects": {
            "a0": {
                "type": u"person",
                "name": u"alice",
                "age": 10
            }
        }
    },
    {
        "type": "observed-data",
        "first_observed": "2004-10-11T21:45:01Z",
        "last_observed": "2004-10-11T21:45:01Z",
        "number_observed": 3,
        "objects": {
            "b0": {
                "type": u"person",
                "name": u"bob",
                "age": 17
            }
        }
    },
    {
        "type": "observed-data",
        "first_observed": "2004-10-11T21:45:02Z",
        "last_observed": "2004-10-11T21:45:02Z",
        "number_observed": 2,
        "objects": {
            "c0": {
                "type": u"person",
                "name": u"carol",
                "age": 22
            }
        }
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
