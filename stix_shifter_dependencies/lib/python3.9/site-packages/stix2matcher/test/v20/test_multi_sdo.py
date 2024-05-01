import pytest

from stix2matcher.matcher import match

_stix_version = '2.0'
_observations = [
    {
        "type": "observed-data",
        "number_observed": 1,
        "first_observed": "1000-12-03T21:34:41Z",
        "last_observed": "1000-12-03T21:34:41Z",
        "objects": {
            "0": {
                "type": u"binary_test",
                "name": u"alice"
            }
        }
    },
    {
        "type": "observed-data",
        "number_observed": 1,
        "first_observed": "2011-12-03T21:34:41Z",
        "last_observed": "2011-12-03T21:34:41Z",
        "objects": {
            "0": {
                "type": u"binary_test",
                "name": u"alice"
            }
        }
    }
]


@pytest.mark.parametrize("pattern", [
    "[binary_test:name = h'616c696365']",
])
def test_multy_sdo_match(pattern):
    # Only the first matched SDO will be returned
    res = match(pattern, _observations, stix_version=_stix_version)
    assert res
    assert len(res) == 1
    assert res[0]["first_observed"] == "1000-12-03T21:34:41Z"
