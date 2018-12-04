class FileHashLookupException(Exception):
    pass


def hash_type_lookup(obj, ds_key, options):
    hash_options = options.get('hash_options', {})
    log_source_id_map = hash_options.get('log_source_id_map', {})
    generic_hash_name = hash_options.get('generic_name', '')
    if not generic_hash_name or ds_key != generic_hash_name:
        # Current key is not generic hash, so return and let regular mapping resume
        return ''
    else:
        generic_hash_value = obj[generic_hash_name]
        # These values must match with the aliases set in aql_event_fields.json
        for type in ["sha256hash", "md5hash", "sha1hash"]:
            if type in obj and obj[type] == generic_hash_value:
                raise FileHashLookupException("Generic hash value already exists in specific hash-type result")
        # Determine hash type based on log source ID map
        logsourceid = str(obj.get('logsourceid', ''))
        if not logsourceid or logsourceid not in log_source_id_map:
            raise FileHashLookupException('Unable to determine type of file hash based on log source ID.')
        else:
            hash_type = log_source_id_map.get(logsourceid)
            hash_type = hash_type.upper()
            # Raise and skip if type is still set to the unknown flag
            if hash_type == 'UNKNOWN':
                raise FileHashLookupException("Invalid {} hash type".format(hash_type))
            else:
                return "file.hashes.{}".format(hash_type)
