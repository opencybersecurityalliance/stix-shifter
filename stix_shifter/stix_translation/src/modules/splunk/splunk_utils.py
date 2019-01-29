import re


class FileHashLookupException(Exception):
    pass


def hash_type_lookup(obj, ds_key, mapped_stix_attribute, options):

    file_hash_map = "file.hashes.{}"

    if ds_key == "file_hash" and mapped_stix_attribute == "file.hashes.UNKNOWN":
        if re.compile("^[a-f0-9]{32}$").match(obj["file_hash"]) is not None:
            file_hash_map = file_hash_map.format("MD5")
            return file_hash_map
        elif re.compile(r'\b[0-9a-f]{40}\b').match(obj["file_hash"]) is not None:
            file_hash_map = file_hash_map.format("SHA-1")
            return file_hash_map
        elif re.compile("[A-Fa-f0-9]{64}").match(obj["file_hash"]) is not None:
            file_hash_map = file_hash_map.format("SHA-256")
            return file_hash_map
        else:
            file_hash_map = file_hash_map.format("Unknown")
            return file_hash_map
