class FileHashLookupException(Exception):
    pass


def _find_hash_type_by_length(value):
    HASH_LENGTH = {'40': 'sha-1', '64': 'sha-256', '32': 'md5'}
    hash_type = HASH_LENGTH.get(str(len(value)), '')
    if hash_type:
        return "file.hashes.{}".format(hash_type.upper())
    else:
        return ''


def _find_hash_type_by_logsource(obj, hash_options):
    logsourceid = str(obj.get('logsourceid', ''))
    log_source_id_map = hash_options.get('log_source_id_map', {})
    if logsourceid and logsourceid in log_source_id_map:
        hash_type = log_source_id_map.get(logsourceid)
        return "file.hashes.{}".format(hash_type.upper())
    else:
        return ''


def hash_type_lookup(obj, ds_key, mapped_stix_attribute, options):
    UNKNOWN_HASH_TYPE_STIX_ATTRIBUTE = 'file.hashes.UNKNOWN'
    STIX_HASH_TYPES = ['file.hashes.SHA-256', 'file.hashes.SHA-1', 'file.hashes.MD5', UNKNOWN_HASH_TYPE_STIX_ATTRIBUTE]
    if mapped_stix_attribute not in STIX_HASH_TYPES:
        return ''
    hash_options = options.get('hash_options', {})
    generic_hash_name = hash_options.get('generic_name', '')
    if generic_hash_name and ds_key == generic_hash_name:
        generic_hash_value = obj[generic_hash_name]
        # These values must match with the aliases set in the select fields
        for type in ["sha256hash", "md5hash", "sha1hash"]:
            if type in obj and obj[type] == generic_hash_value:
                raise FileHashLookupException("Generic hash value already exists in specific hash-type result")

        return _find_hash_type_by_logsource(obj, hash_options) or _find_hash_type_by_length(obj.get(ds_key, ''))
    elif mapped_stix_attribute == UNKNOWN_HASH_TYPE_STIX_ATTRIBUTE:
        return _find_hash_type_by_length(obj.get(ds_key, ''))
    else:
        return ''
