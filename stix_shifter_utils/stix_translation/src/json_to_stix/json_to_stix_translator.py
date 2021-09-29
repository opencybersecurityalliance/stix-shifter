import re
import uuid
import json

from stix_shifter_utils.stix_translation.src.json_to_stix import observable
from stix2validator import validate_instance, print_results
from datetime import datetime
from stix_shifter_utils.utils import logger

# "ID Contributing Properties" taken from https://docs.oasis-open.org/cti/stix/v2.1/csprd01/stix-v2.1-csprd01.html#_Toc16070594
UUID5_NAMESPACE = "00abedb4-aa42-466c-9c01-fed23315a9b7"
NUMBER_OBSERVED_KEY = 'number_observed'
FIRST_OBSERVED_KEY = 'first_observed'
LAST_OBSERVED_KEY = 'last_observed'


# convert JSON data to STIX object using map_data and transformers
def convert_to_stix(data_source, map_data, data, transformers, options, callback=None):

    ds2stix = DataSourceObjToStixObj(data_source, map_data, transformers, options, callback)

    # map data list to list of transformed objects
    observation = ds2stix.transform
    results = list(map(observation, data))

    for stix_object in results:
        if ds2stix.spec_version == "2.1":
            del stix_object["objects"]
        ds2stix.bundle["objects"].append(stix_object)

    for key, value in ds2stix.unique_cybox_objects.items():
        ds2stix.bundle["objects"].append(value)

    return ds2stix.bundle


class DataSourceObjToStixObj:
    logger = logger.set_logger(__name__)

    def __init__(self, data_source, ds_to_stix_map, transformers, options, callback=None):
        self.identity_id = data_source["id"]
        self.ds_to_stix_map = ds_to_stix_map
        self.transformers = transformers
        self.options = options
        self.callback = callback

        # parse through options
        self.stix_validator = options.get('stix_validator')
        self.cybox_default = options.get('cybox_default', True)

        self.properties = observable.properties

        self.data_source = data_source['name']
        self.ds_key_map = [val for val in self.gen_dict_extract('ds_key', ds_to_stix_map)]

        self.bundle = {
            "type": "bundle",
            "id": "bundle--" + str(uuid.uuid4()),
            "objects": []
        }


        if options.get("stix_2.1"):
            self.spec_version = "2.1"
        else:
            self.spec_version = "2.0"
            self.bundle["spec_version"] = "2.0"
        self.unique_cybox_objects = {}
        self.bundle['objects'] += [data_source]

    @staticmethod
    def _get_value(obj, ds_key, transformer):
        """
        Get value from source object, transforming if specified
        :param obj: the input object we are translating to STIX
        :param ds_key: the property from the input object
        :param transformer: the transform to apply to the property value (can be None)
        :return: the resulting STIX value
        """
        if ds_key not in obj:
            DataSourceObjToStixObj.logger.debug('{} not found in object'.format(ds_key))
            return None
        ret_val = obj[ds_key]
        if ret_val and transformer is not None:
            return transformer.transform(ret_val)
        return ret_val

    @staticmethod
    def _add_property(obj, key, stix_value, group=False):
        """
        Add stix_value to dictionary based on the input key, the key can be '.'-separated path to inner object
        :param obj: the dictionary we are adding our key to
        :param key: the key to add
        :param stix_value: the STIX value translated from the input object
        """
        split_key = key.split('.')
        child_obj = obj
        parent_props = split_key[0:-1]
        for prop in parent_props:
            if prop not in child_obj:
                child_obj[prop] = {}
            child_obj = child_obj[prop]

        if split_key[-1] not in child_obj.keys():
            child_obj[split_key[-1]] = stix_value
        elif group is True:  # Mapping of multiple data fields to single STIX object field. Ex: Network Protocols
            if (isinstance(child_obj[split_key[-1]], list)):
                child_obj[split_key[-1]].extend(stix_value)  # append to existing list

    def _handle_cybox_key_def(self, key_to_add, observation, stix_value, obj_name_map, obj_name, group=False):
        """
        Handle the translation of the input property to its STIX CybOX property
        :param key_to_add: STIX property key derived from the mapping file
        :param observation: the the STIX observation currently being worked on
        :param stix_value: the STIX value translated from the input object
        :param obj_name_map: the mapping of object name to actual object
        :param obj_name: the object name derived from the mapping file
        """
        obj_type, obj_prop = key_to_add.split('.', 1)
        objs_dir = observation['objects']

        if obj_name in obj_name_map:
            # add property to existing cybox object
            cybox_obj = objs_dir[obj_name_map[obj_name]]
        else:
            # create new cybox object
            cybox_obj = {'type': obj_type}
            if self.spec_version == "2.1":
                # Todo: Move this elsewhere?
                cybox_obj["id"] = "{}--{}".format(obj_type, str(uuid.uuid4()))
                observation["objects"][cybox_obj["id"]] = cybox_obj
                # resolves_to_refs lists have been deprecated in favor of relationship objects that have a relationship type of resolves-to. 
                # See the Domain Name cybox object https://docs.oasis-open.org/cti/stix/v2.1/csprd01/stix-v2.1-csprd01.html#_Toc16070687 for an example.
                obj_name_map[obj_name] = cybox_obj["id"]
            else:
                obj_dir_key = str(len(objs_dir))
                objs_dir[obj_dir_key] = cybox_obj
                if obj_name is not None:
                    obj_name_map[obj_name] = obj_dir_key

        self._add_property(cybox_obj, obj_prop, stix_value, group)

    @staticmethod
    def _valid_stix_value(props_map, key, stix_value, unwrap=False):
        """
        Checks that the given STIX value is valid for this STIX property
        :param props_map: the map of STIX properties which contains validation attributes
        :param key: the STIX property name
        :param stix_value: the STIX value translated from the input object
        :param unwrap: unwrapping datasource field value of type list
        :return: whether STIX value is valid for this STIX property
        :rtype: bool
        """

        if stix_value is None or stix_value == '':
            DataSourceObjToStixObj.logger.debug("Removing invalid value '{}' for {}".format(stix_value, key))
            return False
        elif isinstance(stix_value, list):
            if len(stix_value) == 0:
                DataSourceObjToStixObj.logger.debug("Removing invalid value '{}' for {}".format(stix_value, key))
                return False
        elif key in props_map and 'valid_regex' in props_map[key]:
            pattern = re.compile(props_map[key]['valid_regex'])
            if unwrap and isinstance(stix_value, list):
                for val in stix_value:
                    if not pattern.match(str(val)):
                        return False
            else:
                if not pattern.match(str(stix_value)):
                    return False
        return True

    # get the nested ds_keys in the mapping
    def gen_dict_extract(self, key, var):
        if hasattr(var, 'items'):
            for k, v in var.items():
                if k == key:
                    yield v
                if isinstance(v, dict):
                    for result in self.gen_dict_extract(key, v):
                        yield result
                elif isinstance(v, list):
                    for d in v:
                        for result in self.gen_dict_extract(key, d):
                            yield result
    # update the object key of the mapping
    @staticmethod
    def _update_object_key(ds_map, indx):
        for key, value in ds_map.items():
            if isinstance(value, dict):
                if 'object' in value:
                    value['object'] = str(value['object']) +'_' + str(indx)
            if isinstance(value, list):
                for item in value:
                    if 'object' in item:
                        item['object'] = str(item['object']) +'_' + str(indx)
                        if 'references' in item:
                            item['references'] = str(item['references']) +'_' + str(indx)

        return ds_map

    def _transform(self, object_map, observation, ds_map, ds_key, obj):

        to_map = obj[ds_key]

        if ds_key not in ds_map:
            if self.options.get('unmapped_fallback'):
                if ds_key not in self.ds_key_map:
                    self.logger.info(
                        'Unmapped fallback is enabled. Adding {} attribute to the custom object'.format(ds_key))
                    cust_obj = {"key": "x-" + self.data_source.replace("_", "-") + "." + ds_key, "object":
                                "cust_object"}
                    if to_map is None or to_map == '':
                        self.logger.debug("Removing invalid value '{}' for {}".format(to_map, ds_key))
                        return
                    self._handle_cybox_key_def(cust_obj["key"], observation, to_map, object_map, cust_obj["object"])
            else:
                self.logger.debug('{} is not found in map, skipping'.format(ds_key))
            return

        if isinstance(to_map, dict):
            self.logger.debug('{} is complex; descending'.format(to_map))
            # If the object is complex we must descend into the map on both sides
            for key in to_map.keys():
                self._transform(object_map, observation, ds_map[ds_key], key, to_map)
            return

        # if the datasource fields is a collection of json object than we need to unwrap it and create multiple objects
        if isinstance(to_map, list):
            self.logger.debug('{} is a list; unwrapping.'.format(to_map))
            for item in to_map:
                if isinstance(item, dict):
                    new_ds_map = self._update_object_key(ds_map[ds_key], to_map.index(item))
                    for field in item.keys():
                        self._transform(object_map, observation, new_ds_map, field, item)
        
        generic_hash_key = ''

        # get the stix keys that are mapped
        ds_key_def_obj = ds_map[ds_key]
        if isinstance(ds_key_def_obj, list):
            ds_key_def_list = ds_key_def_obj
        else:
            # Use callback function to run module-specific logic to handle unknown filehash types
            if self.callback:
                try:
                    generic_hash_key = self.callback(obj, ds_key, ds_key_def_obj['key'], self.options)
                except(Exception):
                    return

            ds_key_def_list = [ds_key_def_obj]


        for ds_key_def in ds_key_def_list:
            if ds_key_def is None or 'key' not in ds_key_def:
                self.logger.debug('{} is not valid (None, or missing key)'.format(ds_key_def))
                continue

            if generic_hash_key:
                key_to_add = generic_hash_key
            else:
                key_to_add = ds_key_def['key']

            transformer = self.transformers[ds_key_def['transformer']] if 'transformer' in ds_key_def else None

            group = False
            unwrap = False

            # unwrap array of stix values to separate stix objects
            if 'unwrap' in ds_key_def:
                unwrap = True

            if ds_key_def.get('cybox', self.cybox_default):
                object_name = ds_key_def.get('object')
                if 'references' in ds_key_def:
                    references = ds_key_def['references']
                    if isinstance(references, list):
                        stix_value = []
                        for ref in references:
                            if unwrap:
                                pattern = re.compile("{}_[0-9]+".format(ref))
                                for obj_name in object_map:
                                    if pattern.match(obj_name):
                                        val = object_map.get(obj_name)
                                        stix_value.append(val)
                            else:
                                val = object_map.get(ref)
                                if not self._valid_stix_value(self.properties, key_to_add, val):
                                    continue
                                stix_value.append(val)
                        if not stix_value:
                            continue
                    else:
                        if unwrap:
                            stix_value = []
                            pattern = re.compile("{}_[0-9]+".format(references))
                            for obj_name in object_map:
                                if pattern.match(obj_name):
                                    val = object_map.get(obj_name)
                                    stix_value.append(val)
                        else:
                            stix_value = object_map.get(references)
                            if not self._valid_stix_value(self.properties, key_to_add, stix_value):
                                continue
                else:
                    # use the hard-coded value in the mapping
                    if 'value' in ds_key_def:
                        stix_value = ds_key_def['value']
                    else:
                        stix_value = self._get_value(obj, ds_key, transformer)
                    if not self._valid_stix_value(self.properties, key_to_add, stix_value, unwrap):
                        continue

                # Group Values
                if 'group' in ds_key_def:
                    group = True

                if unwrap and 'references' not in ds_key_def and isinstance(stix_value, list):
                    self.logger.debug("Unwrapping {} of {}".format(stix_value, object_name))
                    for i in range(len(stix_value)):
                        obj_i_name = "{}_{}".format(object_name, i + 1)
                        val = stix_value[i]
                        self._handle_cybox_key_def(key_to_add, observation, val, object_map,
                                                                     obj_i_name, group)
                else:
                    self._handle_cybox_key_def(key_to_add, observation, stix_value, object_map,
                                                                 object_name, group)
            else:
                # get the object name defined for custom attributes
                if 'object' in ds_key_def:
                    object_name = ds_key_def.get('object')
                    # use the hard-coded value in the mapping
                    if 'value' in ds_key_def:
                        stix_value = ds_key_def['value']
                    # get the value from mapped key
                    elif 'ds_key' in ds_key_def:
                        ds_key = ds_key_def['ds_key']
                        stix_value = self._get_value(obj, ds_key, transformer)
                    if not self._valid_stix_value(self.properties, key_to_add, stix_value):
                        continue
                    self._handle_cybox_key_def(key_to_add, observation, stix_value, object_map,
                                                                 object_name, group)
                else:
                    stix_value = self._get_value(obj, ds_key, transformer)
                    if not self._valid_stix_value(self.properties, key_to_add, stix_value):
                        continue

                    self._add_property(observation, key_to_add, stix_value, group)

    # STIX 2.1 helper methods
    def _generate_and_apply_deterministic_id(self, object_id_map, cybox_objects):
        # Generates ID based on common namespace and SCO properties (omitting id and spec_version)
        # TODO: References may need to be include as part of the ID generation
        for key, cybox in cybox_objects.items():
            cybox_type = ""
            # set id mapping key to original id
            object_id_map[key] = ""
            cybox_properties = {}
            for property, value in cybox.items():
                if property == "type":
                    cybox_type = value
                if not (property == "id" or re.match(".*_ref$", property)):
                    cybox_properties[property] = value
            unique_id = cybox_type + "--" + str(uuid.uuid5(namespace=uuid.UUID(UUID5_NAMESPACE), name=json.dumps(cybox_properties)))
            # set id mapping value to new id
            object_id_map[key] = unique_id
            # replace old id with new
            cybox["id"] = unique_id

    def _replace_references(self, object_id_map, cybox_objects):
        for key, cybox in cybox_objects.items():
            # replace refs with new ids
            for property, value in cybox.items():
                if re.match(".*_ref$", property) and str(value) in object_id_map:
                    cybox[property] = object_id_map[value]
            cybox["spec_version"] = "2.1"

    def _collect_unique_cybox_objects(self, cybox_objects):
        for key, cybox in cybox_objects.items():
            if not cybox["id"] in self.unique_cybox_objects:
                self.unique_cybox_objects[cybox["id"]] = cybox

    def transform(self, obj):
        """
        Transforms the given object in to a STIX observation based on the mapping file and transform functions
        :param obj: the datasource object that is being converted to stix
        :return: the input object converted to stix valid json
        """
        object_map = {}
        stix_type = 'observed-data'
        ds_map = self.ds_to_stix_map
        now = "{}Z".format(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])
        object_id_map = {}

        observation = {
            'id': stix_type + '--' + str(uuid.uuid4()),
            'type': stix_type,
            'created_by_ref': self.identity_id,
            'created': now,
            'modified': now,
            'objects': {}
        }

        # create normal type objects
        if isinstance(obj, dict):
            for ds_key in obj.keys():
                self._transform(object_map, observation, ds_map, ds_key, obj)
        else:
            self.logger.debug("Not a dict: {}".format(obj))

        # special case:
        # remove object if:
        # a reference attribute object does not contain at least one property other than 'type'
        self._cleanup_references(object_map, observation, ds_map)

        # Add required properties to the observation if it wasn't added from the mapping
        if FIRST_OBSERVED_KEY not in observation:
            observation[FIRST_OBSERVED_KEY] = now
        if LAST_OBSERVED_KEY not in observation:
            observation[LAST_OBSERVED_KEY] = now
        if NUMBER_OBSERVED_KEY not in observation:
            observation[NUMBER_OBSERVED_KEY] = 1

        if self.spec_version == "2.1":
            cybox_objects = observation["objects"]
            self._generate_and_apply_deterministic_id(object_id_map, cybox_objects)
            self._replace_references(object_id_map, cybox_objects)
            object_refs = []
            # add cybox references to observed-data object
            for key, value in object_id_map.items():
                object_refs.append(value)
            observation["object_refs"] = object_refs
            observation["spec_version"] = "2.1"
            self._collect_unique_cybox_objects(cybox_objects)

        # Validate each STIX object
        if self.stix_validator:
            validated_result = validate_instance(observation)
            print_results(validated_result)

        return observation

    def _cleanup_references(self, object_map, observation, ds_map):
        objects = observation.get('objects')
        remove_keys = []
        for obj, values in objects.items():
            rm_keys = list(key for key in values if '_ref' in key)
            rm_keys.append('type')

            obj_keys = list(values.keys())

            if sorted(rm_keys) == sorted(obj_keys):
                self.logger.debug('Reference object does not contain required properties, removing: ' + str(values) )
                remove_keys.append(obj)

        for k in remove_keys:
            objects.pop(k)