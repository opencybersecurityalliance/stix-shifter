# import re
import logging
import uuid
from stix2validator import validate_instance, print_results

# convert JSON data to STIX object using map_data and transformers


def convert_to_stix(datasource, map_data, data, transformers, options):
    ds2stix = DataSourceObjToStixObj(
        datasource, map_data, transformers, options)

    # map data list to list of transformed objects
    results = list(map(ds2stix.transform, data))
    return results


class DataSourceObjToStixObj:

    def __init__(self, datasource, ds_to_stix_map, transformers, options):
        self.datasource = datasource
        self.dsToStixMap = ds_to_stix_map
        self.transformers = transformers

        # parse through options
        self.stix_validator = options.get('stix_validator', False)

    @staticmethod
    def _split_key(key, contains_type_name=None):
        """
        Splits the given key into its constituent parts and returns them

        :param key: The key to be split apart on '.'
        :param contains_type_name: defaults to None, used to determine whether we should replace '-' with '_'
        :return: an array of string
        """
        try:
            if contains_type_name:
                return key.split('.') if key.index('.') else None
            else:
                # Replace '-' with '_' to confirm to stix standards
                return key.replace('-', '_').split('.') if key.index('.') else None
        except ValueError:
            logging.info('{0} cannot be split'.format(key))

    @staticmethod
    def _add_none_cybox_props(observation, stix_value, definition):
        """
        Adds properties that are not part of a cyber observable object to the stix object

        :param observation: current stix JSON object
        :param stix_value: Stix valid value
        :param definition: The current mapping key JSON definition
        :return: altered observation object
        """
        key = definition['key']
        split_key = DataSourceObjToStixObj._split_key(key)

        if split_key and split_key[0] not in observation:
            # Creates a custom object in observation if that object isn't present already
            observation.update({split_key[0]: {split_key[1]: stix_value}})
        elif split_key and split_key[0] in observation:
            # Updates custom object if it's already present
            observation[split_key[0]].update({split_key[1]: stix_value})
        else:
            # Adds simple properties(i.e. just key: value pairs) to the observation
            observation.update({key: stix_value})

        return observation

    @staticmethod
    def _deal_with_nested_props(observation, split_key, value, index):
        """
        Creates and/or updates a nested property inside a cyber observable object

        :param observation: current stix JSON object
        :param split_key: an array of keys(i.e. strings) that are used to construct the nested object
        :param value: the value, either reference or stix valid value, to be added to the nested property
        :param index: the index of the cybox object to be altered
        :return: altered observation object
        """
        # TODO improve this method
        if index in observation['objects'] and split_key[-2] in observation['objects'][index]:
            observation['objects'][index][split_key[-2]].update({split_key[-1]: value})
        else:
            new_obj = {'type': split_key[0]} if index not in observation['objects'] else {}
            nested_obj = new_obj
            child_props = split_key[1:-1]
            previous_key = ''

            for prop in child_props:
                child_obj = {}
                if previous_key == '':
                    nested_obj.update({prop: child_obj})
                else:
                    previous_key.update({prop: child_obj})
                previous_key = prop

            nested_obj.update({previous_key: {split_key[-1]: value}})

            if index not in observation['objects']:
                observation['objects'].update({index: nested_obj})
            else:
                obj_to_update = observation['objects'][index]
                obj_to_update.update(nested_obj)
                observation['objects'].update({index: obj_to_update})

        return observation

    @staticmethod
    def _update_cybox_props(index, observation, split_key, value, key_len):
        """
        Updates the given cyber observable object

        :param index: the index of the cybox object to be altered
        :param observation: current stix JSON object
        :param split_key: an array of keys(i.e. strings) that are used to construct the nested object
        :param value: the value, either reference or stix valid value, to be added to the nested property
        :param key_len: length of the split_key
        :return: altered observation object
        """
        if key_len > 2:
            observation = DataSourceObjToStixObj._deal_with_nested_props(observation, split_key, value, index, )
        elif index not in observation['objects']:
            observation['objects'].update({index: {'type': split_key[0], split_key[1]: value}})
        elif index in observation['objects']:
            obj_to_update = observation['objects'][index]
            obj_to_update.update({split_key[1]: value})
            observation['objects'].update({index: obj_to_update})

        return observation

    @staticmethod
    def _add_cybox_props(observation, stix_value, definition, linked, ref_obj_map, val_type):
        """
        Adds a property to a cyber observable object

        :param observation: current stix JSON object
        :param stix_value: stix valid value
        :param definition: The current mapping key JSON definition
        :param linked: a string that is used to find the indices that the property is linked to from the ref_obj_map
        :param ref_obj_map: object containing a list of keys and their respective indices
        :param val_type: string that can be either 'value' or 'reference'
        :return: altered observation object
        """
        split_key = DataSourceObjToStixObj._split_key(definition['key'], True)
        key_len = len(split_key)
        # Run through possible permutations of mapping file
        if val_type == 'value' and linked is None and split_key[0] in ref_obj_map:
            index = str(ref_obj_map[split_key[0]])
            observation['objects'].update({index: {'type': split_key[0], split_key[1]: stix_value}})
        elif val_type == 'value' and linked and linked in ref_obj_map:
            index = str(ref_obj_map[linked])
            observation = DataSourceObjToStixObj._update_cybox_props(index, observation, split_key, stix_value, key_len)
        elif val_type == 'reference' and linked and split_key[0] in ref_obj_map:
            index = str(ref_obj_map[linked])
            ref_value = str(ref_obj_map[definition['references']])
            observation = DataSourceObjToStixObj._update_cybox_props(index, observation, split_key, ref_value, key_len)
        elif val_type == 'reference' and linked and linked in ref_obj_map:
            index = str(ref_obj_map[linked])
            ref_value = str(ref_obj_map[definition['references']])
            observation = DataSourceObjToStixObj._update_cybox_props(index, observation, split_key, ref_value, key_len)

        return observation

    @staticmethod
    def _construct_ref_obj_map(obj, map_file):
        """
        Creates and populates an object of cyber observable object types and their respective indices

        :param obj: the datasource object that is being converted to stix
        :param map_file: the datasource map file
        :return: object containing a list of keys and their respective indices
        """
        obj_ref_map = {}
        index = 0

        for item in obj:
            if item in map_file:
                map_def = map_file[item]
                item_def = map_def if isinstance(map_def, list) else [map_def]

                for definition in item_def:
                    split_key = DataSourceObjToStixObj._split_key(definition['key'], True)
                    linked = definition['linked'] if 'linked' in definition else None
                    cybox = definition['cybox'] if 'cybox' in definition else None

                    if cybox and not linked and split_key[0] not in obj_ref_map:
                        obj_ref_map.update({split_key[0]: index})
                        index = index + 1
                    elif linked and linked not in obj_ref_map:
                        obj_ref_map.update({linked: index})
                        index = index + 1

        return obj_ref_map

    @staticmethod
    def _process_definitions(item, map_file, observation, transformers, obj, ref_obj_map):
        """
        Iterate through the datasource object that is being converted to stix and populate the observation object

        :param item: a single key:value from the datasource objectthat is being converted to stix
        :param map_file: the datasource map file
        :param observation: current stix JSON object
        :param transformers: a set of functions
        :param obj: the datasource object that is being converted to stix
        :param ref_obj_map: object containing a list of keys and their respective indices
        :return: altered observation object
        """
        map_def = map_file[item]
        item_def = map_def if isinstance(map_def, list) else [map_def]

        for definition in item_def:
            transformer = transformers[definition['transformer']] if 'transformer' in definition else None
            stix_value = transformer.transform(obj[item]) if transformer else obj[item]
            linked = definition['linked'] if 'linked' in definition else None
            cybox = definition['cybox'] if 'cybox' in definition else None
            val_type = definition['type']

            if stix_value is None:
                continue

            if not cybox:
                observation = DataSourceObjToStixObj._add_none_cybox_props(observation, stix_value, definition)
            elif cybox:
                observation = DataSourceObjToStixObj._add_cybox_props(observation, stix_value, definition,
                                                                      linked, ref_obj_map, val_type)

        return observation

    def transform(self, obj):
        """
        Transforms the given object in to a STIX observation based on the mapping file and transform functions

        :param obj: the datasource object that is being converted to stix
        :return: the input object converted to stix valid json
        """
        transformers = self.transformers
        map_file = self.dsToStixMap
        uniq_id = str(uuid.uuid4())
        stix_type = 'observed-data'

        # declare baseline observation object
        observation = {
            'x_com_ibm_uds_datasource': {'id': self.datasource['id'], 'name': self.datasource['name']},
            'id': stix_type + '--' + uniq_id,
            'type': stix_type,
            'objects': {}
        }

        ref_obj_map = DataSourceObjToStixObj._construct_ref_obj_map(obj, map_file)

        for item in obj:
            if item in map_file:
                observation = DataSourceObjToStixObj._process_definitions(item, map_file, observation,
                                                                          transformers, obj, ref_obj_map)

        if self.stix_validator:
            validated_result = validate_instance(observation)
            print_results(validated_result)
        return observation
