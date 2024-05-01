import pytest
import six

from stix2matcher.matcher import match

_stix_version = '2.0'
_observations = [
    {
        "id": "observed-data--a49751b8-b041-4c00-96c2-76af472bfbbe",
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
        "id": "observed-data--7d34018e-986c-4817-a2c5-21fe95284109",
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
        "id": "observed-data--52a5bab7-2cfd-40c6-a35a-b5bcb8afb11b",
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


@pytest.mark.parametrize("pattern,expected_ids", [
    # match() returns the SDOs only for the first binding
    # found, so to assure results are predictable, it's best if
    # only one binding is possible for each pattern.
    ("[person:name='alice']",
     "observed-data--a49751b8-b041-4c00-96c2-76af472bfbbe"),
    ("[person:name='bob'] AND [person:name='carol']",
        ("observed-data--7d34018e-986c-4817-a2c5-21fe95284109",
         "observed-data--52a5bab7-2cfd-40c6-a35a-b5bcb8afb11b")),
    ("[person:name='carol'] OR [person:name>'zelda']",
     "observed-data--52a5bab7-2cfd-40c6-a35a-b5bcb8afb11b")
])
def test_matching_sdos(pattern, expected_ids):
    sdos = match(pattern, _observations, stix_version=_stix_version)
#    import pprint
#    pprint.pprint(sdos)
    sdo_ids = [sdo["id"] for sdo in sdos]

    if isinstance(expected_ids, six.string_types):
        assert sdo_ids == [expected_ids]
    else:
        assert sorted(sdo_ids) == sorted(expected_ids)
