from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer


class SplunkToTimestamp(ValueTransformer):
    """A value transformer for converting Splunk timestamp to regular timestamp"""

    @staticmethod
    def transform(splunkTime):
        return splunkTime[:-6] + 'Z'


class SplunkHash(ValueTransformer):
    """
    A value transformer for converting the following hash format, into multiple fields.

    Example for Sysmon hashes:

    Input: "process_hash": "MD5=5A0B0E6F407C89916515328F318842A1,SHA256=8FC86B75926043F048971696BC7A407615C9A03D9B1BFACC54785C8903B82A91,IMPHASH=406DD24835F1447987FB607C78597252",

    Desired output:
    "hashes": {
                        "MD5": "5A0B0E6F407C89916515328F318842A1",
                        "SHA256":"8FC86B75926043F048971696BC7A407615C9A03D9B1BFACC54785C8903B82A91,
                        "IMPHASH": "406DD24835F1447987FB607C78597252"
                    }

    """

    @staticmethod
    def transform(obj):
        def get_pair_of_hash(hash_raw):
            """
            :param hash_raw: Expected input of the following form MD5=5A0B0E6F407C89916515328F318842A1
            :return:
            """
            if hash_raw:
                splitted = hash_raw.split("=")
                if len(splitted) != 2:
                    raise ValueError("hash should be in the format of <hash_name=hash_value>")
                return splitted[0], splitted[1]

        # expected to be string
        if obj:
            hashes = str(obj).split(",")
            if len(hashes) == 1 and '=' not in hashes[0]:
                return obj
            hashes = dict(map(lambda x: get_pair_of_hash(x), hashes))
            return hashes
