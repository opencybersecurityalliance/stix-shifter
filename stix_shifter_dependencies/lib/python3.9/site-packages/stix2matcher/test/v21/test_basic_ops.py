import pytest

from stix2matcher.matcher import MatcherException, match

_stix_version = '2.1'
_observations = [
    {
        "type": "bundle",
        "id": "bundle--c2a23389-17c9-4247-8aa2-d2ffde3de334",
        "objects": [
            {
                "id": "observed-data--647947aa-4cc3-43a3-a42f-2c670986d777",
                "type": "observed-data",
                "number_observed": 1,
                "first_observed": "2014-04-19T06:51:26Z",
                "last_observed": "2014-04-19T06:51:26Z",
                "object_refs": [
                    "test--9c61d8ff-21ca-489a-accd-7356c2ea0a7b"
                ],
                "spec_version": "2.1"
            },
            {
                "type": "test",
                "int": 5,
                "float": 12.658,
                "float_int": 12.0,
                "bool": True,
                "string": "hello",
                "ip": "11.22.33.44",
                "cidr": "11.22.33.44/20",
                "id": "test--9c61d8ff-21ca-489a-accd-7356c2ea0a7b"
            }
        ]
    }
]


@pytest.mark.parametrize("pattern", [
    "[test:int = 5]",
    "[test:int NOT != 5]",
    "[test:int > 3]",
    "[test:int NOT < 3]",
    "[test:int < 12]",
    "[test:int > 4.9]",
    "[test:int < 5.1]",
    "[test:int >= 5]",
    "[test:int NOT < 5]",
    "[test:int <= 5]",
    "[test:int != false]",
    "[test:int != true]",
    "[test:int NOT = true]",
    "[test:int != 'world']",
    "[test:int != h'010203']",
    "[test:int != b'AQIDBA==']",
    "[test:int != t'1965-07-19T22:41:38Z']",
    "[test:int IN (-4, 5, 6)]",
    "[test:int IN (-4, 5, 6.6)]",
    "[test:int NOT IN ('a', 'b', 'c')]",
    "[test:int NOT MATCHES 'l+']",
    "[test:int NOT LIKE 'he%']",
])
def test_basic_ops_int_match(pattern):
    assert match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    "[test:int NOT = 5]",
    "[test:int NOT != 8]",
    "[test:int > 8]",
    "[test:int < 2]",
    "[test:int > 5.1]",
    "[test:int < 4.9]",
    "[test:int = false]",
    "[test:int = true]",
    "[test:int = 'world']",
    "[test:int = h'010203']",
    "[test:int > h'010203']",
    "[test:int = b'AQIDBA==']",
    "[test:int < b'AQIDBA==']",
    "[test:int = t'1965-07-19T22:41:38Z']",
    "[test:int > t'1965-07-19T22:41:38Z']",
    "[test:int LIKE 'he%']",
    "[test:int MATCHES 'l+']",
    "[test:int NOT IN (-4, 5, 6)]",
    "[test:int NOT IN (-4, 5, 6.6)]",
    "[test:int IN ('a', 'b', 'c')]"
])
def test_basic_ops_int_nomatch(pattern):
    assert not match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    "[test:float = 12.658]",
    "[test:float NOT != 12.658]",
    "[test:float > 3]",
    "[test:float NOT < 3]",
    "[test:float < 22]",
    "[test:float > 12.65799]",
    "[test:float < 12.65801]",
    "[test:float >= 12.658]",
    "[test:float <= 12.658]",
    "[test:float != false]",
    "[test:float != true]",
    "[test:float != 'world']",
    "[test:float != h'010203']",
    "[test:float != b'AQIDBA==']",
    "[test:float != t'1965-07-19T22:41:38Z']",
    "[test:float IN (-4.21, 12.658, 964.321)]",
    "[test:float_int IN (11, 12, 13)]",
    "[test:float_int IN (11.1, 12, 13)]",
    "[test:float NOT IN ('a', 'b', 'c')]",
    "[test:float NOT MATCHES 'l+']",
    "[test:float NOT LIKE 'he%']",
])
def test_basic_ops_float_match(pattern):
    assert match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    "[test:float NOT = 12.658]",
    "[test:float != 12.658]",
    "[test:float > 22]",
    "[test:float < 3]",
    "[test:float > 12.65801]",
    "[test:float < 12.65799]",
    "[test:float = false]",
    "[test:float = true]",
    "[test:float = 'world']",
    "[test:float NOT != 'world']",
    "[test:float = h'010203']",
    "[test:float > h'010203']",
    "[test:float = b'AQIDBA==']",
    "[test:float < b'AQIDBA==']",
    "[test:float = t'1965-07-19T22:41:38Z']",
    "[test:float > t'1965-07-19T22:41:38Z']",
    "[test:float LIKE 'he%']",
    "[test:float MATCHES 'l+']",
    "[test:float NOT IN (-4.21, 12.658, 964.321)]",
    "[test:float_int NOT IN (11, 12, 13)]",
    "[test:float_int NOT IN (11.1, 12, 13)]",
    "[test:float IN ('a', 'b', 'c')]"
])
def test_basic_ops_float_nomatch(pattern):
    assert not match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    "[test:bool != 1]",
    "[test:bool != 32.567]",
    "[test:bool = true]",
    "[test:bool NOT != true]",
    "[test:bool != false]",
    "[test:bool NOT = false]",
    "[test:bool != 'world']",
    "[test:bool != h'010203']",
    "[test:bool != b'AQIDBA==']",
    "[test:bool != t'1965-07-19T22:41:38Z']",
    "[test:bool IN (false, true, false)]",
    "[test:bool NOT IN ('a', 'b', 'c')]",
    "[test:bool NOT MATCHES 'l+']",
    "[test:bool NOT LIKE 'he%']",
])
def test_basic_ops_bool_match(pattern):
    assert match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    "[test:bool = 1]",
    "[test:bool = 32.567]",
    "[test:bool != true]",
    "[test:bool NOT = true]",
    "[test:bool = false]",
    "[test:bool NOT != false]",
    "[test:bool = 'world']",
    "[test:bool = h'010203']",
    "[test:bool = b'AQIDBA==']",
    "[test:bool = t'1965-07-19T22:41:38Z']",
    "[test:bool LIKE 'he%']",
    "[test:bool MATCHES 'l+']",
    "[test:bool NOT IN (false, true, false)]",
    "[test:bool IN ('a', 'b', 'c')]"
])
def test_basic_ops_bool_nomatch(pattern):
    assert not match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    "[test:string != 1]",
    "[test:string != 32.567]",
    "[test:string != true]",
    "[test:string != false]",
    "[test:string = 'hello']",
    "[test:string NOT != 'hello']",
    "[test:string != 'world']",
    "[test:string NOT = 'world']",
    "[test:string > 'alice']",
    "[test:string < 'zelda']",
    "[test:string >= 'hello']",
    "[test:string <= 'hello']",
    "[test:string != h'010203']",
    "[test:string != b'AQIDBA==']",
    "[test:string LIKE 'he%']",
    "[test:string LIKE 'he__o']",
    "[test:string MATCHES 'l+']",
    "[test:string MATCHES '.lo$']",
    "[test:string IN ('goodbye', 'hello', 'world')]",
    "[test:string NOT IN (1, 2, 3)]"
])
def test_basic_ops_string_match(pattern):
    assert match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    "[test:string = 1]",
    "[test:string = 32.567]",
    "[test:string = true]",
    "[test:string = false]",
    "[test:string != 'hello']",
    "[test:string NOT = 'hello']",
    "[test:string = 'world']",
    "[test:string NOT != 'world']",
    "[test:string < 'alice']",
    "[test:string > 'zelda']",
    "[test:string <= 'alice']",
    "[test:string >= 'zelda']",
    "[test:string = h'010203']",
    "[test:string = b'AQIDBA==']",
    "[test:string NOT LIKE 'he%']",
    "[test:string NOT LIKE 'he__o']",
    "[test:string NOT MATCHES 'l+']",
    "[test:string NOT MATCHES '.lo$']",
    "[test:string NOT IN ('goodbye', 'hello', 'world')]",
    "[test:string IN (1, 2, 3)]"
])
def test_basic_ops_string_nomatch(pattern):
    assert not match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    # These are errors because a timestamp literal is used in the pattern,
    # which causes the matcher to try to interpret the JSON value as a
    # timestamp as well.  If this merely caused a false (for '=') or true
    # (for '!=') result, then timestamp formatting errors in the JSON would
    # silently slip through, causing potential false negatives.  It's
    # perhaps safer to assume in this situation that a string JSON value was
    # really intended to be a timestamp, and error out if it's incorrectly
    # formatted.
    "[test:string = t'1965-07-19T22:41:38Z']",
    "[test:string != t'1965-07-19T22:41:38Z']",
    "[test:string > t'1965-07-19T22:41:38Z']",
])
def test_basic_ops_string_err(pattern):
    with pytest.raises(MatcherException):
        assert match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    "[test:ip ISSUBSET '11.22.41.123/20']",
    "[test:ip NOT ISSUBSET '11.22.123.41/20']",
    "[test:cidr ISSUPERSET '11.22.41.123']",
    "[test:cidr ISSUPERSET '11.22.41.123/29']",
    "[test:cidr NOT ISSUPERSET '11.22.33.44/13']",
    "[test:cidr NOT ISSUPERSET '11.22.123.41/29']",
    "[test:int NOT ISSUPERSET '11.22.33.44']",
    "[test:int NOT ISSUBSET '11.22.33.44']",
    "[test:float NOT ISSUPERSET '11.22.33.44']",
    "[test:float NOT ISSUBSET '11.22.33.44']",
    "[test:bool NOT ISSUPERSET '11.22.33.44']",
    "[test:bool NOT ISSUBSET '11.22.33.44']",
])
def test_basic_ops_ip_match(pattern):
    assert match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    "[test:ip NOT ISSUBSET '11.22.41.123/20']",
    "[test:ip ISSUBSET '11.22.123.41/20']",
    "[test:cidr NOT ISSUPERSET '11.22.41.123']",
    "[test:cidr NOT ISSUPERSET '11.22.41.123/29']",
    "[test:cidr ISSUPERSET '11.22.33.44/13']",
    "[test:cidr ISSUPERSET '11.22.123.41/29']",
    "[test:int ISSUPERSET '11.22.33.44']",
    "[test:int ISSUBSET '11.22.33.44']",
    "[test:float ISSUPERSET '11.22.33.44']",
    "[test:float ISSUBSET '11.22.33.44']",
    "[test:bool ISSUPERSET '11.22.33.44']",
    "[test:bool ISSUBSET '11.22.33.44']",
])
def test_basic_ops_ip_nomatch(pattern):
    assert not match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    "[test:string NOT IN ()]"
])
def test_basic_ops_emptyset_match(pattern):
    assert match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    "[test:string IN ()]"
])
def test_basic_ops_emptyset_nomatch(pattern):
    assert not match(pattern, _observations, stix_version=_stix_version)


@pytest.mark.parametrize("pattern", [
    # Sets are required to contain elements of a single type.
    "[test:string IN (1, true)]",
    "[test:string IN (1, 2.2, true)]",
    "[test:string IN (1.1, 2.2, true)]",
])
def test_basic_ops_set_err(pattern):
    with pytest.raises(MatcherException):
        assert match(pattern, _observations, stix_version=_stix_version)
