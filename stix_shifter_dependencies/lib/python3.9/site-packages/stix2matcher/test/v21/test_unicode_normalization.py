import pytest

from stix2matcher.matcher import match

_stix_version = '2.1'
_observations = [
    {
        "type": "bundle",
        "id": "bundle--6ecbed3f-dbdd-4e68-8083-c7802fef4757",
        "objects": [
            {
                "id": "observed-data--9a0169e0-80c7-4adb-9ea4-43ed5acde57a",
                "type": "observed-data",
                "number_observed": 1,
                "first_observed": "2011-08-08T20:02:48Z",
                "last_observed": "2011-08-08T20:02:48Z",
                "object_refs": [
                    "test--da9516c0-c4b5-4788-a1d8-c68dce578a38"
                ],
                "spec_version": "2.1"
            },
            {
                "type": "test",
                "ddots": {
                    # Three different ways of representing "d" with dot above
                    # and below.
                    "nfc": "\u1e0d\u0307",
                    "nfd": "d\u0323\u0307",
                    "alt1": "\u1e0b\u0323"
                },
                "id": "test--da9516c0-c4b5-4788-a1d8-c68dce578a38"
            }
        ]
    }
]


def _all_kv_pairs():
    """
    This combines the prop names and values in all different combinations.
    """
    for k in _observations[0]["objects"][1]["ddots"]:
        for v in _observations[0]["objects"][1]["ddots"].values():
            yield k, v


def _matched_kv_pairs():
    """
    This returns an iterable through all the matched prop name/value pairs.
    """
    return _observations[0]["objects"][1]["ddots"].items()


def _mismatched_kv_pairs():
    """
    This combines the prop names and values in all different combinations,
    except for the matching pairs.
    """
    for i, k in enumerate(_observations[0]["objects"][1]["ddots"]):
        for j, v in enumerate(_observations[0]["objects"][1]["ddots"].values()):
            if i != j:
                yield k, v


@pytest.mark.parametrize("pattern", [
    u"[test:ddots.{} LIKE '{}']".format(k, v)
    for k, v in _all_kv_pairs()
])
def test_unicode_normalization_like_match(pattern):
    assert match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    u"[test:ddots.{} MATCHES '^{}$']".format(k, v)
    for k, v in _all_kv_pairs()
])
def test_unicode_normalization_regex_match(pattern):
    assert match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    u"[test:ddots.{} != '{}']".format(k, v)
    for k, v in _mismatched_kv_pairs()
])
def test_unicode_normalization_ne_match(pattern):
    assert match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    u"[test:ddots.{} != '{}']".format(k, v)
    for k, v in _matched_kv_pairs()
])
def test_unicode_normalization_ne_nomatch(pattern):
    assert not match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    u"[test:ddots.{} = '{}']".format(k, v)
    for k, v in _matched_kv_pairs()
])
def test_unicode_normalization_eq_match(pattern):
    assert match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    u"[test:ddots.{} = '{}']".format(k, v)
    for k, v in _mismatched_kv_pairs()
])
def test_unicode_normalization_eq_nomatch(pattern):
    assert not match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    u"[test:ddots.{} IN ('{}')]".format(k, v)
    for k, v in _matched_kv_pairs()
])
def test_unicode_normalization_set_match(pattern):
    assert match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    u"[test:ddots.{} IN ('{}')]".format(k, v)
    for k, v in _mismatched_kv_pairs()
])
def test_unicode_normalization_set_nomatch(pattern):
    assert not match(pattern, _observations, stix_version=_stix_version)
