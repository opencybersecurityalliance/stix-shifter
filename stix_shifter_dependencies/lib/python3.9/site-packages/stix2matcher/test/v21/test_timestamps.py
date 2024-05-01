import pytest
from stix2patterns.pattern import ParseException

from stix2matcher.matcher import MatcherException, match

_stix_version = '2.1'
_observations = [
    {
        "type": "bundle",
        "id": "bundle--de25dd14-209f-4d91-b645-c383b6422c10",
        "objects": [
            {
                "id": "observed-data--770dcb90-43f7-4455-92fd-80409ad4ebf7",
                "type": "observed-data",
                "number_observed": 1,
                "first_observed": "1983-04-21T15:31:06Z",
                "last_observed": "1983-04-21T15:31:06Z",
                "object_refs": [
                    "event--5ca25429-833b-4589-8350-e810db273d44"
                ],
                "spec_version": "2.1"
            },
            {
                "type": "event",
                "good_ts": "2010-05-21T13:21:43Z",
                "good_ts_frac": "2010-05-21T13:21:43.1234Z",
                "good_ts_frac_nano": "2010-05-21T13:21:43.123456789Z",
                "bad_ts": [
                    "2010-05-21T13:21:43",
                    "2010-05-21T13:21:43z",
                    "2010-05-21t13:21:43Z",
                    "2010/05/21T13:21:43Z",
                    "2010-05-21T13:21:99Z",
                    "2010-05-21T13:21Z"
                ],
                "id": "event--5ca25429-833b-4589-8350-e810db273d44"
            }
        ]
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
    for i in range(len(_observations[0]["objects"][1]["bad_ts"]))
])
def test_ts_json_error(pattern):
    with pytest.raises(MatcherException):
        match(pattern, _observations, stix_version=_stix_version)
