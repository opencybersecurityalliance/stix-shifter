import pytest
from stix2patterns.pattern import ParseException

from stix2matcher.matcher import MatcherException, match

_stix_version = '2.0'
_observations = [
    {
        "type": "observed-data",
        "first_observed": "1983-04-21T15:31:06Z",
        "last_observed": "1983-04-21T15:31:06Z",
        "number_observed": 1,
        "objects": {
            "0": {
                "type": "event",
                "good_ts": u"2010-05-21T13:21:43Z",
                "good_ts_frac": u"2010-05-21T13:21:43.1234Z",
                "good_ts_frac_nano": u"2010-05-21T13:21:43.123456789Z",
                "bad_ts": [
                    u"2010-05-21T13:21:43",
                    u"2010-05-21T13:21:43z",
                    u"2010-05-21t13:21:43Z",
                    u"2010/05/21T13:21:43Z",
                    u"2010-05-21T13:21:99Z",
                    u"2010-05-21T13:21Z"
                ]
            }
        }
    }
]


@pytest.mark.parametrize("pattern", [
    "[event:good_ts = t'2010-05-21T13:21:43Z']",
    "[event:good_ts != t'1974-11-05T05:31:11Z']",
    "[event:good_ts > t'1974-11-05T05:31:11Z']",
    "[event:good_ts < t'3012-08-17T17:43:55Z']",
    "[event:good_ts_frac = t'2010-05-21T13:21:43.1234Z']",
    "[event:good_ts_frac_nano = t'2010-05-21T13:21:43.123456789Z']",
    "[event:good_ts IN (t'1953-11-26T14:25:33Z', t'2010-05-21T13:21:43Z', t'2000-06-17T17:25:51.44Z')]",
    "[event:good_ts NOT IN (t'1953-11-26T14:25:33Z', t'1985-07-25T20:27:52Z', t'2000-06-17T17:25:51.44Z')]"
])
def test_ts_match(pattern):
    assert match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    # Same as above with operators reversed.
    "[event:good_ts != t'2010-05-21T13:21:43Z']",
    "[event:good_ts = t'1974-11-05T05:31:11Z']",
    "[event:good_ts <= t'1974-11-05T05:31:11Z']",
    "[event:good_ts >= t'3012-08-17T17:43:55Z']",
    "[event:good_ts_frac != t'2010-05-21T13:21:43.1234Z']",
    "[event:good_ts_frac_nano != t'2010-05-21T13:21:43.123456789Z']",
    "[event:good_ts NOT IN (t'1953-11-26T14:25:33Z', t'2010-05-21T13:21:43Z', t'2000-06-17T17:25:51.44Z')]",
    "[event:good_ts IN (t'1953-11-26T14:25:33Z', t'1985-07-25T20:27:52Z', t'2000-06-17T17:25:51.44Z')]"
])
def test_ts_nomatch(pattern):
    assert not match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    "[event:good_ts = t'2010-05-21T13:21:43']",
    "[event:good_ts = t'2010-05-21T13:21:43z']",
    "[event:good_ts = t'2010-05-21t13:21:43Z']",
    "[event:good_ts = t'2010/05/21T13:21:43Z']",
    "[event:good_ts = t'2010-05-21T13:21Z']",
    "[event:good_ts = t'2010-05-21T13:21:99Z']"
])
def test_ts_pattern_error_parse(pattern):
    with pytest.raises(ParseException):
        match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    # auto-generate simple tests for all the bad timestamps
    "[event:bad_ts[{}] = t'1996-07-11T09:17:10Z']".format(i)
    for i in range(len(_observations[0]["objects"]["0"]["bad_ts"]))
])
def test_ts_json_error(pattern):
    with pytest.raises(MatcherException):
        match(pattern, _observations, stix_version=_stix_version)
