import pytest

from stix2matcher.matcher import match

_stix_version = '2.1'
_observations = [
    {
        "type": "bundle",
        "id": "bundle--d33ba274-6623-4ff9-af64-0e2d17de9bbe",
        "objects": [
            {
                "type": "observed-data",
                "spec_version": "2.1",
                "id": "observed-data--1209f166-bba6-4307-a566-60e3a6c39cd2",
                "created": "2022-10-25T08:59:09.295455Z",
                "modified": "2022-10-29T01:53:18.132077Z",
                "first_observed": "2022-11-27T19:50:46.889315Z",
                "last_observed": "2023-01-05T05:35:31.372958Z",
                "number_observed": 1,
                "object_refs": [
                    "ipv4-addr--0ddfa859-1a40-4aa0-b440-136c498cc5a5"
                ]
            },
            {
                "type": "observed-data",
                "spec_version": "2.1",
                "id": "observed-data--10000000-bba6-4307-a566-60e3a6c39cd2",
                "created": "2022-10-25T08:59:09.295455Z",
                "modified": "2022-10-29T01:53:18.132077Z",
                "first_observed": "2022-11-27T19:50:46.889315Z",
                "last_observed": "2023-01-05T05:35:31.372958Z",
                "number_observed": 1,
                "object_refs": [
                    "ipv4-addr--00000000-1a40-4aa0-b440-136c498cc5a5"
                ]
            },
            {
                "type": "observed-data",
                "spec_version": "2.1",
                "id": "observed-data--9813cee6-9e9d-4199-88d2-a740331fa8a1",
                "created": "2021-09-17T05:06:25.871976Z",
                "modified": "2022-06-19T20:23:09.126157Z",
                "first_observed": "2022-11-05T10:47:16.435447Z",
                "last_observed": "2023-01-17T23:00:47.872163Z",
                "number_observed": 1,
                "object_refs": [
                    "ipv4-addr--11111111-1a40-4aa0-b440-555c495cc5a5"
                ]
            },
            {
                "type": "ipv4-addr",
                "spec_version": "2.1",
                "id": "ipv4-addr--0ddfa859-1a40-4aa0-b440-136c498cc5a5",
                "value": "127.0.0.10"
            },
            {
                "type": "ipv4-addr",
                "spec_version": "2.1",
                "id": "ipv4-addr--00000000-1a40-4aa0-b440-136c498cc5a5",
                "value": "127.0.0.10"
            },
            {
                "type": "ipv4-addr",
                "spec_version": "2.1",
                "id": "ipv4-addr--11111111-1a40-4aa0-b440-555c495cc5a5",
                "value": "127.0.0.200"
            }
        ]
    }
]


@pytest.mark.parametrize("pattern", [
    "[ipv4-addr:value = '127.0.0.10']",
])
def test_multy_sdo_match(pattern):
    # Only the first matched SDO will be returned
    res = match(pattern, _observations, stix_version=_stix_version)
    assert res
    assert len(res) == 1
    assert res[0]['objects'][0]['id'] == 'observed-data--1209f166-bba6-4307-a566-60e3a6c39cd2'


@pytest.mark.parametrize("pattern", [
    "[ipv4-addr:value = '127.0.0.10'] REPEATS 2 TIMES",
])
def test_multy_repeat_match(pattern):
    res = match(pattern, _observations, stix_version=_stix_version)
    assert res
    assert len(res) == 2
