# I'll specially test some critical internal time-interval related code,
# since it's easier to test it separately than create lots of SDOs AND
# patterns.
import pytest
from stix2patterns.pattern import ParseException

from stix2matcher.matcher import (_OVERLAP, _OVERLAP_NONE,
                                  _OVERLAP_TOUCH_INNER, _OVERLAP_TOUCH_OUTER,
                                  _OVERLAP_TOUCH_POINT, MatcherException,
                                  _overlap, _timestamp_intervals_within, match)

_stix_version = '2.0'
_observations = [
    {
        "type": "observed-data",
        "first_observed": "1994-11-29T13:37:52Z",
        "last_observed": "1994-11-29T13:37:52Z",
        "number_observed": 1,
        "objects": {
            "0": {
                "type": u"person",
                "name": u"alice"
            }
        }
    },
    {
        "type": "observed-data",
        "first_observed": "1994-11-29T13:37:57Z",
        "last_observed": "1994-11-29T13:37:57Z",
        "number_observed": 1,
        "objects": {
            "0": {
                "type": u"person",
                "name": u"bob"
            }
        }
    },
    {
        "type": "observed-data",
        "first_observed": "1994-11-29T13:38:02Z",
        "last_observed": "1994-11-29T13:38:02Z",
        "number_observed": 1,
        "objects": {
            "0": {
                "type": u"person",
                "name": u"carol"
            }
        }
    }
]


@pytest.mark.parametrize("pattern", [
    # WITHIN tests
    "[person:name = 'bob'] WITHIN 1 SECONDS",
    "[person:name = 'bob'] WITHIN .0001 SECONDS",
    "[person:name = 'alice'] AND [person:name < 'carol'] WITHIN 1 SECONDS",
    "([person:name = 'alice'] AND [person:name < 'carol']) WITHIN 5 SECONDS",
    "([person:name = 'alice'] AND [person:name < 'carol']) WITHIN 6 SECONDS",
    "([person:name = 'alice'] OR [person:name = 'darlene']) WITHIN 1 SECONDS",

    # START/STOP tests
    "[person:name = 'bob'] START '1994-11-29T13:37:57Z' STOP '1994-11-29T13:37:58Z'",
    "[person:name LIKE 'a%'] AND [person:name = 'bob'] START '1994-11-29T13:37:57Z' STOP '1994-11-29T13:37:58Z'",
    "([person:name LIKE 'a%'] AND [person:name = 'bob']) START '1994-11-29T13:37:50Z' STOP '1994-11-29T13:37:58Z'",
    "[person:name = 'alice'] OR [person:name = 'darlene'] START '1994-11-29T13:37:57Z' STOP '1994-11-29T13:37:58Z'",
    "([person:name = 'alice'] OR [person:name = 'darlene']) START '1994-11-29T13:37:52Z' STOP '1994-11-29T13:37:58Z'",
    "[person:name MATCHES ''] REPEATS 2 TIMES START '1994-11-29T13:37:50Z' STOP '1994-11-29T13:37:58Z'",
])
def test_temp_qual_match(pattern):
    assert match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    # WITHIN tests
    "([person:name = 'alice'] AND [person:name < 'carol']) WITHIN 4 SECONDS",
    "([person:name = 'alice'] AND [person:name < 'carol']) WITHIN 4.9999 SECONDS",
    "[person:name = 'elizabeth'] WITHIN 10 SECONDS",
    "([person:name < 'alice'] OR [person:name = 'darlene']) WITHIN 10 SECONDS",

    # START/STOP tests
    "[person:name = 'bob'] START '1994-11-29T13:37:58Z' STOP '1994-11-29T13:37:58Z'",
    "[person:name = 'bob'] START '1994-11-29T13:37:59Z' STOP '1994-11-29T13:37:58Z'",
    "[person:name = 'bob'] START '1994-11-29T13:37:58Z' STOP '1994-11-29T13:37:59Z'",
    "([person:name LIKE 'a%'] AND [person:name = 'bob']) START '1994-11-29T13:37:50Z' STOP '1994-11-29T13:37:57Z'",
    "([person:name LIKE 'z%'] OR [person:name = 'darlene']) START '1994-11-29T13:37:50Z' STOP '1994-11-29T13:37:57Z'",
    "[person:name MATCHES ''] REPEATS 3 TIMES START '1994-11-29T13:37:50Z' STOP '1994-11-29T13:37:58Z'",
    "[person:name NOT LIKE 'foo'] START '1994-11-29T13:37:50Z' STOP '1994-11-29T13:37:57Z' REPEATS 3 TIMES",
])
def test_temp_qual_nomatch(pattern):
    assert not match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    # WITHIN tests
    "[person:name = 'alice'] WITHIN 0 SECONDS",

    # START/STOP tests
    "[person:name = 'hannah'] START '1994-11-29t13:37:58Z' STOP '1994-11-29T13:37:58Z'",
    "[person:name = 'hannah'] START '1994-11-29T13:37:58Z' STOP '1994-11-29T13:37:58z'",
    "[person:name = 'hannah'] START '1994-11-29t13:37:58Z' STOP '1994-11-29T13:37:58'",
    "[person:name = 'hannah'] START '1994-11-29T13:37Z' STOP '1994-11-29T13:37:58Z'",
])
def test_temp_qual_error_match(pattern):
    with pytest.raises(MatcherException):
        match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    # WITHIN tests
    "[person:name = 'alice'] WITHIN 1 second",
    "[person:name = 'alice'] WITHIN -123.367 SECONDS",

    # START/STOP tests
    "[person:name = 'hannah'] START '1994-11-29T13:37:58Z'",
])
def test_temp_qual_error_parse(pattern):
    with pytest.raises(ParseException):
        match(pattern, _observations, stix_version=_stix_version)

# The below tests use ints instead of timestamps.  The code is generic enough
# and it's much easier to test with simple ints.


@pytest.mark.parametrize("min1,max1,min2,max2,expected_overlap", [
    (1, 1, 1, 1, _OVERLAP_TOUCH_POINT),
    (1, 1, 1, 2, _OVERLAP_TOUCH_INNER),
    (1, 2, 1, 1, _OVERLAP_TOUCH_OUTER),
    (1, 2, 2, 2, _OVERLAP_TOUCH_INNER),
    (2, 2, 1, 2, _OVERLAP_TOUCH_OUTER),
    (1, 2, 2, 3, _OVERLAP_TOUCH_INNER),
    (2, 3, 1, 2, _OVERLAP_TOUCH_OUTER),
    (1, 2, 1, 3, _OVERLAP),
    (1, 3, 1, 2, _OVERLAP),
    (1, 3, 2, 3, _OVERLAP),
    (2, 3, 1, 3, _OVERLAP),
    (1, 3, 2, 4, _OVERLAP),
    (2, 4, 1, 3, _OVERLAP),
    (1, 4, 2, 3, _OVERLAP),
    (2, 3, 1, 4, _OVERLAP),
    (1, 3, 2, 2, _OVERLAP),
    (2, 2, 1, 3, _OVERLAP),
    (1, 2, 3, 4, _OVERLAP_NONE),
    (3, 4, 1, 2, _OVERLAP_NONE)
])
def test_overlap(min1, max1, min2, max2, expected_overlap):
    assert _overlap(min1, max1, min2, max2) == expected_overlap


@pytest.mark.parametrize("intervals,duration", [
    (((1, 1), (1, 1)), 0),
    (((1, 1), (1, 1)), 1),
    (((1, 1), (1, 2)), 1),
    (((1, 2), (3, 4)), 1),
    (((1, 4), (2, 3)), 1),
    (((1, 3), (2, 4)), 1),
    (((1, 2), (3, 4), (5, 6)), 4),
    (((1, 4), (2, 3), (4, 5)), 1),
    (((1, 2), (2, 3), (4, 5)), 2),
    (((1, 2), (2, 3), (4, 5)), 3)
])
def test_intervals_within_match(intervals, duration):
    assert _timestamp_intervals_within(intervals, duration)


@pytest.mark.parametrize("intervals,duration", [
    (((1, 2), (3, 4)), 0),
    (((1, 2), (4, 5)), 1),
    (((1, 2), (3, 4), (5, 6)), 2),
    (((1, 5), (1, 2), (4, 5)), 1),
    (((1, 2), (1, 3), (1, 4), (4, 5)), 1)
])
def test_intervals_within_nomatch(intervals, duration):
    assert not _timestamp_intervals_within(intervals, duration)


# For these tests, instead of keeping the data fixed and changing the
# pattern, we adjust timestamps in the data to further exercise temporal
# operations, and keep the pattern mostly fixed.
_1 = "2000-01-01T00:00:00Z"
_2 = "2000-01-01T00:00:01Z"
_3 = "2000-01-01T00:00:02Z"
_4 = "2000-01-01T00:00:03Z"
_5 = "2000-01-01T00:00:04Z"


@pytest.mark.parametrize("interval1,interval2,duration", [
    ((_1, _1), (_1, _1), 1),
    ((_1, _1), (_1, _2), 1),
    ((_1, _1), (_1, _2), 2),
    ((_1, _2), (_2, _3), 1),
    ((_1, _2), (_3, _4), 1),
    ((_1, _4), (_2, _3), 1),
    ((_1, _3), (_2, _4), 1),
    ((_1, _2), (_4, _5), 2),
])
def test_within_match(interval1, interval2, duration):

    _observations[0]["first_observed"] = interval1[0]
    _observations[0]["last_observed"] = interval1[1]

    _observations[1]["first_observed"] = interval2[0]
    _observations[1]["last_observed"] = interval2[1]

    pattern = "([person:name='alice'] AND [person:name='bob']) " \
              "WITHIN {0} SECONDS".format(duration)
    assert match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("interval1,interval2,duration", [
    ((_1, _2), (_4, _5), 1),
    ((_1, _1), (_4, _5), 2),
    ((_1, _2), (_5, _5), 2),
])
def test_within_nomatch(interval1, interval2, duration):

    _observations[0]["first_observed"] = interval1[0]
    _observations[0]["last_observed"] = interval1[1]

    _observations[1]["first_observed"] = interval2[0]
    _observations[1]["last_observed"] = interval2[1]

    pattern = "([person:name='alice'] AND [person:name='bob']) " \
              "WITHIN {0} SECONDS".format(duration)
    assert not match(pattern, _observations, stix_version=_stix_version)
