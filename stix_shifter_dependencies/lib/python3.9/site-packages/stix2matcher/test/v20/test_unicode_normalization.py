import pytest

from stix2matcher.matcher import match

_stix_version = '2.0'
_observations = [
    {
        "type": "cybox-container",
        "first_observed": "2011-08-08T20:02:48Z",
        "last_observed": "2011-08-08T20:02:48Z",
        "number_observed": 1,
        "objects": {
            "0": {
                "type": "test",
                "ddots": {
                    # Three different ways of representing "d" with dot above
                    # and below.
                    "nfc": u"\u1e0d\u0307",
                    "nfd": u"d\u0323\u0307",
                    "alt1": u"\u1e0b\u0323"
                }
            }
        }
    }
]


def _all_kv_pairs():
    """
    This combines the prop names and values in all different combinations.
    """
    for k in _observations[0]["objects"]["0"]["ddots"]:
        for v in _observations[0]["objects"]["0"]["ddots"].values():
            yield k, v


def _matched_kv_pairs():
    """
    This returns an iterable through all the matched prop name/value pairs.
    """
    return _observations[0]["objects"]["0"]["ddots"].items()


def _mismatched_kv_pairs():
    """
    This combines the prop names and values in all different combinations,
    except for the matching pairs.
    """
    for i, k in enumerate(_observations[0]["objects"]["0"]["ddots"]):
        for j, v in enumerate(_observations[0]["objects"]["0"]["ddots"].values()):
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
