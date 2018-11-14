from stix_shifter.src.json_to_stix import observable
from stix_shifter.src.json_to_stix.json_to_stix_translator import DataSourceObjToStixObj
import logging
from stix2validator import validate_instance, print_results
import uuid


def convert_to_stix(data_source, map_data, data, transformers, options):
    bundle = {
        "type": "bundle",
        "id": "bundle--" + str(uuid.uuid4()),
        "objects": []
    }

    identity_id = data_source['id']
    bundle['objects'] += [data_source]

    ds2stix = QradarObjToStixObj(identity_id, map_data, transformers, options)

    # map data list to list of transformed objects
    results = list(map(ds2stix.transform, data))

    bundle["objects"] += results

    return bundle


class QradarObjToStixObj (DataSourceObjToStixObj):

    def __init__(self, identity_id, ds_to_stix_map, transformers, options):
        self.identity_id = identity_id
        self.ds_to_stix_map = ds_to_stix_map
        self.transformers = transformers

        # parse through options
        self.stix_validator = options.get('stix_validator', False)
        self.cybox_default = options.get('cybox_default', True)
        self.hash_options = options.get('hash_options', {})
        self.properties = observable.properties

    def transform(self, obj):
        """
        Transforms the given object in to a STIX observation based on the mapping file and transform functions

        :param obj: the datasource object that is being converted to stix
        :return: the input object converted to stix valid json
        """
        object_map = {}
        stix_type = 'observed-data'
        ds_map = self.ds_to_stix_map
        transformers = self.transformers
        observation = {
            'id': stix_type + '--' + str(uuid.uuid4()),
            'type': stix_type,
            'created_by_ref': self.identity_id,
            'objects': {}
        }

        # Taken from the data source config
        hash_types = self.hash_options.get('types', [])
        log_source_id_map = self.hash_options.get('log_source_id_map', {})
        generic_hash_name = self.hash_options.get('generic_name', '')

        # Collect hashes associated to specific hash-type results
        hash_type_values = []
        for type in hash_types:
            if type in obj:
                hash_type_values.append(obj[type])

        # create normal type objects
        for ds_key in obj:
            is_generic_file_hash = False
            if ds_key not in ds_map:
                logging.debug('{} is not found in map, skipping'.format(ds_key))
                continue
            # Handle file hash of unknown type
            if generic_hash_name and ds_key == generic_hash_name:
                is_generic_file_hash = True
                if obj[ds_key] in hash_type_values:
                    # Generic hash value already exists in specific hash-type result, so skip.
                    continue
                else:
                    # Determine hash type based on log source ID map
                    logsourceid = obj.get('logsourceid', '')
                    if not logsourceid or logsourceid not in log_source_id_map:
                        logging.debug('Unable to determine type of file hash based on log source ID.')
                        continue
                    else:
                        hash_type = log_source_id_map.get(logsourceid)
                        # set the hash key to what's mapped to the log source id
                        key_to_add = "file.hashes.{}".format(hash_type.upper())

            # get the stix keys that are mapped
            ds_key_def_obj = self.ds_to_stix_map[ds_key]
            ds_key_def_list = ds_key_def_obj if isinstance(ds_key_def_obj, list) else [ds_key_def_obj]
            for ds_key_def in ds_key_def_list:
                if ds_key_def is None or 'key' not in ds_key_def:
                    logging.debug('{} is not valid (None, or missing key)'.format(ds_key_def))
                    continue

                if not is_generic_file_hash:
                    key_to_add = ds_key_def['key']
                transformer = transformers[ds_key_def['transformer']] if 'transformer' in ds_key_def else None

                if ds_key_def.get('cybox', self.cybox_default):
                    object_name = ds_key_def.get('object')
                    if 'references' in ds_key_def:
                        stix_value = object_map[ds_key_def['references']]
                    else:
                        stix_value = DataSourceObjToStixObj._get_value(obj, ds_key, transformer)
                        if not DataSourceObjToStixObj._valid_stix_value(self.properties, key_to_add, stix_value):
                            continue
                    DataSourceObjToStixObj._handle_cybox_key_def(key_to_add, observation, stix_value, object_map, object_name)
                else:
                    stix_value = DataSourceObjToStixObj._get_value(obj, ds_key, transformer)
                    if not DataSourceObjToStixObj._valid_stix_value(self.properties, key_to_add, stix_value):
                        continue
                    DataSourceObjToStixObj._add_property(observation, key_to_add, stix_value)

        # Validate each STIX object
        if self.stix_validator:
            validated_result = validate_instance(observation)
            print_results(validated_result)
        return observation
