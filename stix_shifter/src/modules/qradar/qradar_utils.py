class FileHashLookupException(Exception):
    pass


def parse_hash_options(hash_options, obj):
    hash_types = hash_options.get('types', [])
    log_source_id_map = hash_options.get('log_source_id_map', {})
    generic_hash_name = hash_options.get('generic_name', '')
    # Collect hashes associated to specific hash-type results
    hash_type_values = []
    for type in hash_types:
        if type in obj:
            hash_type_values.append(obj[type])
    return hash_types, log_source_id_map, generic_hash_name, hash_type_values


def lookup_hash_with_logsource_id(obj, ds_key, hash_types, log_source_id_map, generic_hash_name, hash_type_values):
    if not generic_hash_name or ds_key != generic_hash_name:
        return ''
    else:
        if obj[ds_key] in hash_type_values:
            raise FileHashLookupException("Generic hash value already exists in specific hash-type result")
        else:
            # Determine hash type based on log source ID map
            logsourceid = obj.get('logsourceid', '')
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
