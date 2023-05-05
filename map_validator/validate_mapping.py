import argparse
import json
import logging


# create logging formatter
logFormatter = logging.Formatter(fmt='%(levelname)s: %(message)s')

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)

# Add console handler to logger
logger.addHandler(consoleHandler)


msg_fmt = '%s in mapping %s'


def log_warning(mapping, msg):
    logger.warning(msg_fmt, msg, mapping)


def log_error(mapping, msg):
    logger.error(msg_fmt, msg, mapping)


def get_mapping(to_stix_map):
    for _, mappings in to_stix_map.items():
        if isinstance(mappings, list):
            for mapping in mappings:
                if isinstance(mapping, dict):
                    yield mapping
                else:
                    log_error(mappings, 'Nothing found')
                    break
        elif isinstance(mappings, dict):  # and not all(type(v) in (str, bool) for v in mappings.values()):
            if 'key' in mappings and isinstance(mappings['key'], str):  # and 'object' in mappings:
                yield mappings
            else:
                # Step down into nested mapping
                yield from get_mapping(mappings)


# From stix_shifter_utils/stix_translation/src/json_to_stix/json_to_stix_translator.py
# TODO: use pydantic to validate structure?
KNOWN_KEYS = {
    'cybox',       # bool; is this a SCO property (or observed-data SDO prop)?
    'ds_key',      # ???
    'group',       # bool; combine this value into a list
    'group_ref',   # ???
    'key',         # str; path-like name of property target
    'object',      # str; named object to add property to
    'references',  # str|list[str]; named objects to reference
    'transformer', # str; function to apply on value
    'unwrap',      # bool; ???
    'value',       # any; constant (literal) value for property
}


def ip_types(*args):
    return all(arg in ('ipv4-addr', 'ipv6-addr') for arg in args)


def main():
    parser = argparse.ArgumentParser('Generate a bundle of STIX observed-data')
    parser.add_argument('-l', '--level', metavar='LEVEL', default='warning', type=str)
    parser.add_argument('filename')
    args = parser.parse_args()

    logger.setLevel(args.level.upper())

    with open(args.filename, 'r') as fp:
        to_stix_map = json.load(fp)

    # Track named objects
    objects = {}
    reffed = {}

    for mapping in get_mapping(to_stix_map):
        #TODO: make each "check" a function?

        # Check cybox flag
        cybox = mapping.get('cybox', True)
        if not isinstance(cybox, bool):  # Note: this could be checked by pydantic
            log_error(mapping, '"cybox" is not a boolean')
        obj = mapping.get('object')
        if not obj and cybox:
            log_warning(mapping, 'no "object"')

        # Validate key
        key = mapping['key']
        if not isinstance(key, str):
            log_error(mapping, '"key" is not a string')
            continue  # This is "fatal" for this mapping
        otype, _, rest = key.partition('.')
        if otype and obj:
            prev_otype = objects.get(obj)
            if (prev_otype and
                prev_otype != otype and
                not ip_types(prev_otype, otype) and
                '_ref.' not in rest):
                log_error(mapping, f'conflicting types for {objects[obj]} {obj}')
            else:
                objects[obj] = otype
        if not otype and cybox != False:
            log_error(mapping, 'No type in "key" and "cybox" != False')
        if cybox is False and otype:
            if '-' in otype:
                log_error(mapping, f'"key" type is {otype} but "cybox" is False')
            elif rest:
                log_warning(mapping, f'dict {otype} as observed-data property')

        # Check refs
        if '_ref.' in rest:
            log_error(mapping, 'invalid reference syntax')
        if rest.endswith('_ref'):
            # Must reference something
            if 'references' not in mapping:
                log_error(mapping, f'no "references" for {key}')
            else:
                ref_objs = mapping['references']
                if not isinstance(ref_objs, list):
                    ref_objs = [ref_objs]
                for ref_obj in ref_objs:
                    reffed[ref_obj] = mapping   # Save and check at end of file

        # Look for any unknown mapping dict keys
        for key in mapping:
            if key not in KNOWN_KEYS:
                log_warning(mapping, f'unknown param "{key}"')

    # Check for undefined reference objects
    for ref_obj, mapping in reffed.items():
        if ref_obj not in objects:
            log_error(mapping, 'unknown "references" object')


if __name__ == '__main__':
    main()
