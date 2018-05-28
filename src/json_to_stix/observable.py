
REGEX = {
            'date': '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z',
            'ipv4': ('^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'),  # noqa: E501
            'ipv6': ('(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))')  # noqa: E501
        }
# move it to its class (file)
common_props = {
    'created_by_ref': {'required': False},
    'created': {
        'required': True,
        'valid_regex': REGEX['date']
    },
    'modified': {
        'required': True,
        'valid_regex': REGEX['date']
    },
    'revoked': {'required': False},
    'labels': {'required': False},
    'confidence': {'required': False},
}

# move it to its class (file)
observation_props = {
    'first_observed': {
        'required': False,
        'valid_regex': REGEX['date']
    },
    'last_observed': {
        'required': False,
        'valid_regex': REGEX['date']
    },
    'number_observed': {'required': False},
}

# move it a file
simple_props = {
    'ipv4-addr.value': {
        'valid_regex': REGEX['ipv4']
    },
    'ipv6-addr.value': {
        'valid_regex': REGEX['ipv6']
    },
    'user-account': {'required': False},
    'url': {'required': False},
    'domain-name': {'required': False}
}

complex_props = {
    'network-traffic': {
    }
}
