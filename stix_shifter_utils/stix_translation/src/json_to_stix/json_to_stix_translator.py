import re
import uuid
import copy
import json

from stix_shifter_utils.utils.helpers import dict_merge
from stix_shifter_utils.stix_translation.src.json_to_stix import observable
from stix2validator import validate_instance, print_results, ValidationOptions
from datetime import datetime
from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.helpers import StixObjectId, StixObjectIdEncoder

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

    for _, value in ds2stix.unique_cybox_objects.items():
        ds2stix.bundle["objects"].append(value)

    if options.get('stix_validator'):
        if ds2stix.spec_version == "2.1":
            # Serialize and Deserialize bundle to covert StixObjectIds to strings
            bundle_obj = json.dumps(ds2stix.bundle, sort_keys=False, cls=StixObjectIdEncoder)
            bundle_obj = json.loads(bundle_obj)
        else:
            bundle_obj = ds2stix.bundle
        validated_result = validate_instance(bundle_obj, ValidationOptions(version=ds2stix.spec_version))
        print_results(validated_result)

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
            with open("stix_shifter_utils/stix_translation/src/json_to_stix/id_contributing_properties.json", 'r') as f:
                self.contributing_properties_definitions =  json.load(f)
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
            child_obj_val = child_obj[split_key[-1]]
            if (isinstance(child_obj_val, list)):
                child_obj_val.extend(stix_value)  # append to existing list
                child_obj[split_key[-1]] = child_obj_val


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
            new_ds_map = copy.deepcopy(ds_map)
            for key, value in new_ds_map.items():
                if isinstance(value, dict):
                    if 'object' in value:
                        value['object'] = str(value['object']) + '_' + str(indx)
                if isinstance(value, list):
                    for item in value:
                        if 'object' in item:
                            item['object'] = str(item['object']) + '_' + str(indx)
                            if 'references' in item:
                                if isinstance(item['references'], list):
                                    for ref_idx, reference in enumerate(item['references']):
                                        item['references'][ref_idx] = str(reference) + '_' + str(indx)
                                else:
                                    item['references'] = str(item['references']) + '_' + str(indx)
            return new_ds_map

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


    def _valid_stix_value(self, observable_key, stix_value):
        """
        Checks that the given STIX value is valid for this STIX property
        :param observable_key: the STIX property name
        :param stix_value: the STIX value translated from the input object
        :return: whether STIX value is valid for this STIX property
        :rtype: bool
        """
        try: 
            if observable_key in self.properties and 'valid_regex' in self.properties[observable_key]:
                pattern = re.compile(self.properties[observable_key]['valid_regex'])
                match = pattern.match
                if not match(str(stix_value)):
                    return False
            return True
        except Exception as e:
            self.logger.debug("Failed to validate STIX property '{}' with value '{}'. Exception: {}".format(observable_key, stix_value, e))
            return False

    def _compose_value_object(self, value, key_list, observable_key=None, object_tag_ref_map=None, transformer=None, references=None, unwrap=False):
        """
        Converts the value of the data to STIX valid value
        """
        try:
            return_value = {}
            for key in key_list:
                return_value[key] = self._compose_value_object(value, key_list[1:], observable_key=observable_key, object_tag_ref_map=object_tag_ref_map, transformer=transformer, references=references, unwrap=unwrap)
                break
            else:
                if transformer:
                    try: 
                        value = transformer.transform(value)
                        if value is None:
                            return None
                    except Exception:
                        return None
                
                if references:
                    if isinstance(references, list):
                        return_value = []
                        for ref in references:
                            if not isinstance(value, list):
                                value = [value]
                            for i, _ in enumerate(value):
                                parent_key_ind = self._get_tag_ind(ref, object_tag_ref_map, create_on_absence=False, unwrap=i)
                                if parent_key_ind:
                                    return_value.append(parent_key_ind)
                    else:
                        return_value = self._get_tag_ind(references, object_tag_ref_map, create_on_absence=False)
                        # if the property has unwrap true and is not a list, convert to list
                        if unwrap is True and not isinstance(return_value, list):
                            return_value = [return_value]
                else:
                    if unwrap is False and observable_key and not self._valid_stix_value(observable_key, value):
                        return None
                    return_value = value

            return return_value
        except Exception as e:
            raise Exception("Error in json_to_stix_translator._compose_value_object: %s" % e)


    def _get_tag_ind(self, tag, object_tag_ref_map, create_on_absence=False, unwrap=False, property_key=None):
        """
        Gets the stringified index of the observable object from the `object_tag_ref_map` cached dictionary if it exists
        or creates otherwise.
        """
        tag_ind = None
        tag_ind_str = None
        try:
            # if the datasource fields is a collection of json object than we need to unwrap it and create multiple objects
            if unwrap:
                tag = tag + '_' + str(unwrap)

            if tag in object_tag_ref_map['tags']:
                tag_ind = object_tag_ref_map['tags'][tag]['i']
                object_tag_ref_map['tags'][tag]['n'] += 1
            elif create_on_absence:
                tag_ind_str = str(object_tag_ref_map[UUID5_NAMESPACE])
                if self.spec_version == "2.1":
                    tag_ind = StixObjectId(tag_ind_str)
                else:
                    tag_ind = tag_ind_str

                object_tag_ref_map[UUID5_NAMESPACE] += 1
                object_tag_ref_map['tags'][tag] = {'i': tag_ind, 'n': 0}
                
            if tag_ind is not None:
                if not tag_ind_str:
                    tag_ind_str = str(tag_ind)
                if property_key and '_ref' not in property_key:
                    object_tag_ref_map['non_ref_props'][tag_ind_str] = True
        except Exception as e:
            raise Exception("Error in json_to_stix_translator._get_tag_ind: %s : %s" % (e, e.__traceback__.tb_lineno))
        
        return tag_ind

    def _add_property(self, type_name, property_key, parent_key_ind, value, objects, group=False, cybox=True):
        """
        Add observable object property and its STIX valid value to the cached `objects` dictionary
        """
        parent_key_ind_str = str(parent_key_ind)
        if not parent_key_ind_str in objects:
            if cybox:
                objects[parent_key_ind_str] = {
                    'type': type_name,
                    property_key: value
                }
                if self.spec_version == "2.1":
                    objects[parent_key_ind_str]["id"] = parent_key_ind
                    objects[parent_key_ind_str]["spec_version"] = "2.1"
            else:
                objects[parent_key_ind_str] = {
                property_key: value
            }
        else:
            if not property_key in objects[parent_key_ind_str]:
                objects[parent_key_ind_str][property_key] = value
            elif isinstance(value, dict):
                objects[parent_key_ind_str][property_key] = dict_merge(objects[parent_key_ind_str][property_key], value)
            elif isinstance(objects[parent_key_ind_str][property_key], list) and group:
                objects[parent_key_ind_str][property_key].extend(value)

            
    def _handle_properties(self, to_stix_config_prop, data, objects, object_tag_ref_map, parent_data=None, ds_sub_key=None, object_key_ind=None):
        """ 
        Walks through data object, matches the property names of the data elements with the to_stix_map property names and 
        send the values to process if the data is the final value 
        """
        try:
            if data is not None:
                if isinstance(to_stix_config_prop, dict) and to_stix_config_prop.get('key') is not None and not isinstance(to_stix_config_prop.get('key'), dict):
                    # data variable is the final value, process in bulk
                    self._handle_value(data, parent_data, ds_sub_key, to_stix_config_prop, objects, object_tag_ref_map, object_key_ind)

                elif isinstance(data, list):
                    for i, d in enumerate(data):
                        if isinstance(d, list) or isinstance(d, dict):
                            self._handle_properties(to_stix_config_prop, d, objects, object_tag_ref_map, data, ds_sub_key, i)
                        else:
                            # data variable is the final value, process in bulk
                            self._handle_value(data, parent_data, ds_sub_key, to_stix_config_prop, objects, object_tag_ref_map, object_key_ind)
                            break

                elif isinstance(data, dict):
                    for k in data:
                        cust_prop = None
                        if k in to_stix_config_prop:
                            cust_prop = to_stix_config_prop[k]
                        elif self.options.get('unmapped_fallback') and k not in object_tag_ref_map['ds_key_cybox']:
                            cust_prop = {"key": "x-" + self.data_source.replace("_", "-") + "." + k, "object": "cust_object"}
                            
                        if cust_prop:
                            self._handle_properties(cust_prop, data[k], objects, object_tag_ref_map, data, k, object_key_ind)
                else:
                    self._handle_value(data, parent_data, ds_sub_key, to_stix_config_prop, objects, object_tag_ref_map, object_key_ind)
        except Exception as e:
            raise Exception("Error in json_to_stix_translator._handle_properties: %s" % e)


    def _handle_value(self, data, parent_data, ds_sub_key, to_stix_config_prop, objects, object_tag_ref_map, object_key_ind=None):
        """
        Receives the raw value of a data property, converts to a STIX valid value and adds to the cached observable `objects` dictionary
        """
        try: 
            if isinstance(to_stix_config_prop, dict):
                props = [to_stix_config_prop]
            else:
                props = to_stix_config_prop
            
            for prop in props:
                key = prop.get('key', None)
                if key is None:
                    continue

                transformer = self.transformers[prop['transformer']] if 'transformer' in prop else None
                references = references = prop['references'] if 'references' in prop else None
                # unwrap array of stix values to separate stix objects
                unwrap = True if 'unwrap' in prop and isinstance(data, list) else False
                cybox = prop.get('cybox', self.cybox_default)

                if self.callback:
                    try:
                        generic_hash_key = self.callback(parent_data, ds_sub_key, key, self.options)
                        if generic_hash_key:
                            key = generic_hash_key
                    except Exception as e:
                        continue

                config_keys = key.split('.')
                if len(config_keys) < 2:
                    if False is prop.get('cybox', self.cybox_default): 
                        object_tag_ref_map['out_cybox'][key] = self._compose_value_object(data, [], observable_key=key, object_tag_ref_map=object_tag_ref_map, transformer=transformer, references=references, unwrap=unwrap)
                    pass
                else:
                    type_name = config_keys[0]
                    property_key = config_keys[1]
                    parent_key = prop['object'] if 'object' in prop else type_name

                    group = prop['group'] if 'group' in prop else False
                    substitute_key = prop['ds_key'] if 'ds_key' in prop else None

                    if False is cybox and not substitute_key:
                        value = self._compose_value_object(data, config_keys[2:], observable_key=key, object_tag_ref_map=object_tag_ref_map, transformer=transformer, references=references, unwrap=unwrap)
                        self._add_property(type_name, property_key, type_name, value, object_tag_ref_map['out_cybox'], cybox=False)
                        continue

                    if object_key_ind:
                        parent_key = parent_key + '_' + str(object_key_ind)

                    # use the hard-coded value in the mapping
                    if 'value' in prop:
                        value = prop['value']
                    else:
                        if substitute_key and parent_data:
                            data = parent_data.get(substitute_key)

                            if False is cybox:
                                object_tag_ref_map['ds_key_cybox'][substitute_key] = True
                        
                        value = self._compose_value_object(data, config_keys[2:], observable_key=key, object_tag_ref_map=object_tag_ref_map, transformer=transformer, references=references, unwrap=unwrap)

                    if value is None or value == '':
                        continue

                    if not references and unwrap and isinstance(value, list):
                        for i, val_el in enumerate(value):
                            parent_key_ind = self._get_tag_ind(parent_key, object_tag_ref_map, create_on_absence=True, unwrap=i, property_key=property_key)
                            self._add_property(type_name, property_key, parent_key_ind, val_el, objects, group=group)
                    else:
                        parent_key_ind = self._get_tag_ind(parent_key, object_tag_ref_map, create_on_absence=True, property_key=property_key)
                        self._add_property(type_name, property_key, parent_key_ind, value, objects, group=group)
        except Exception as e:
            raise Exception("Error in json_to_stix_translator._handle_value: %s : %s" % (e, e.__traceback__.tb_lineno))


    def _generate_deterministic_id(self, cybox):
        # Generates ID based on common namespace and SCO properties (omitting id and spec_version)

        unique_id = None
        cybox_properties = {}
        cybox_type = cybox.get("type")
        contributing_properties = self.contributing_properties_definitions.get(cybox_type)

        if contributing_properties:
            for contr_prop in contributing_properties:
                if type(contr_prop) is list: # list of hash types
                    for hashtype in contr_prop:
                        hash_prop = "hashes.{}".format(hashtype)
                        if hash_prop in cybox:
                            cybox_properties[hash_prop] = cybox[hash_prop]
                            break
                elif contr_prop in cybox and '_ref' not in contr_prop:
                    cybox_properties[contr_prop] = cybox[contr_prop] 
            
            if cybox_properties:
                unique_id = cybox_type + "--" + str(uuid.uuid5(namespace=uuid.UUID(UUID5_NAMESPACE), name=json.dumps(cybox_properties)))

        else: # STIX process or custom object used UUID4 for identifier
            unique_id = "{}--{}".format(cybox_type, str(uuid.uuid4()))

        return unique_id


    def transform(self, obj):
        try:
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
                object_tag_ref_map = {UUID5_NAMESPACE: 0, 'tags': {}, 'non_ref_props': {}, 'out_cybox': {}, 'ds_key_cybox': {}}

                self._handle_properties(ds_map, obj, object_map, object_tag_ref_map)
                # special case:
                # remove object if:
                # a reference attribute object does not contain at least one property other than 'type'
                object_map = self._cleanup_references(object_map, object_tag_ref_map['non_ref_props'])
                observation['objects'] = object_map

                for k, v in object_tag_ref_map['out_cybox'].items():
                    observation[k] = v
            
            else:
                self.logger.debug("Not a dict: {}".format(obj))

            # Add required properties to the observation if it wasn't added from the mapping
            if FIRST_OBSERVED_KEY not in observation:
                observation[FIRST_OBSERVED_KEY] = now
            if LAST_OBSERVED_KEY not in observation:
                observation[LAST_OBSERVED_KEY] = now
            if NUMBER_OBSERVED_KEY not in observation:
                observation[NUMBER_OBSERVED_KEY] = 1

            if self.spec_version == "2.1":
                object_refs = []

                for key, value in observation["objects"].items():
                    unique_id = self._generate_deterministic_id(value)
                    if unique_id:
                        if isinstance(value['id'], StixObjectId):
                            value['id'].update(unique_id)

                        if unique_id not in object_refs:
                            object_refs.append(unique_id)
                            self.unique_cybox_objects[key] = value

                observation["object_refs"] = object_refs
                observation["spec_version"] = "2.1"

        except Exception as e:
            raise Exception("Error in json_to_stix_translator.transform %s : %s" % (e, e.__traceback__.tb_lineno))

        return observation


    def _cleanup_references(self, objects, tags):
        new_objects = {}
        tag_keys = list(tags.keys())

        if not self.spec_version == "2.1":
            try:
                tag_keys.sort(key=lambda x: int(x))
            except Exception:
                pass

        for ind in tag_keys:
            new_objects[ind] = objects[ind]
            
        return new_objects