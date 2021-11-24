import re
import uuid
import json

from stix_shifter_utils.utils.helpers import dict_merge
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


    def _check_stix_value_pattern(self, observable_key, return_value):
        try: 
            if observable_key in self.properties and 'valid_regex' in self.properties[observable_key]:
                pattern = re.compile(self.properties[observable_key]['valid_regex'])
                match = pattern.match
                if not match(str(return_value)):
                    return False
            return True
        except Exception as e:
            return False
    
    def _compose_value_object(self, value, key_list, observable_key=None, object_tag_ref_map=None, transformer=None, references=None, unwrap=False, group=False):
        try:
            return_value = {}
            for key in key_list:
                return_value[key] = self._compose_value_object(value, key_list[1:], observable_key=observable_key, object_tag_ref_map=object_tag_ref_map, transformer=transformer, references=references, unwrap=unwrap, group=group)
                break
            else:
                if transformer:
                    value = transformer.transform(value)
                    if value is None:
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
                        if unwrap is not False and not isinstance(return_value, list):
                            return_value = [return_value]
                else:
                    if unwrap is False and observable_key and not self._check_stix_value_pattern(observable_key, value):
                        return None
                    return_value = value

            return return_value
        except Exception as e:
            raise Exception("Error in json_to_stix_translator._compose_value_object: %s" % e)


    def _get_tag_ind(self, tag, object_tag_ref_map, create_on_absence=False, unwrap=False, property_key=None):
        tag_ind = None
        if unwrap:
            tag = '%s_%s' % (tag, unwrap)

        if tag in object_tag_ref_map['tags']:
            tag_ind = object_tag_ref_map['tags'][tag]['i']
            object_tag_ref_map['tags'][tag]['n'] += 1
        elif create_on_absence:
            tag_ind = object_tag_ref_map[UUID5_NAMESPACE]
            object_tag_ref_map[UUID5_NAMESPACE] += 1
            object_tag_ref_map['tags'][tag] = {'i': tag_ind, 'n': 0}
            
        if tag_ind is not None:
            tag_ind = str(tag_ind)
            if property_key and '_ref' not in property_key:
                object_tag_ref_map['non_ref_props'][tag_ind] = True

        return tag_ind

    def _add_prperty(self, type_name, property_key, parent_key_ind, value, objects, group=False, cybox=True):
        if not parent_key_ind in objects:
            if cybox:
                objects[parent_key_ind] = {
                    'type': type_name,
                    property_key: value
                }
            else:
                objects[parent_key_ind] = {
                property_key: value
            }
        else:
            if not property_key in objects[parent_key_ind]:
                objects[parent_key_ind][property_key] = value
            elif isinstance(value, dict):
                objects[parent_key_ind][property_key] = dict_merge(objects[parent_key_ind][property_key], value)
            elif isinstance(objects[parent_key_ind][property_key], list) and group:
                objects[parent_key_ind][property_key].extend(value)
            else: #TODO: get rid of this weird 'else'
                # print({'old': objects[parent_key_ind][property_key], 'new': value})
                pass

    def _process_properties(self, to_stix_config_prop, data, objects, object_tag_ref_map, parent_data=None, ds_sub_key=None, object_key_ind=None):
        try:
            if isinstance(to_stix_config_prop, dict):
                if True:
                # if to_stix_config_prop.get('cybox', self.cybox_default):
                    key = to_stix_config_prop.get('key', None)
                    if not key or (isinstance(key, dict)):
                        if not isinstance(data, list):
                            data = [data]
                        for i, d_el in enumerate(data):
                            if isinstance(d_el, dict):
                                for ds_sub_key in d_el.keys():
                                    prop = to_stix_config_prop.get(ds_sub_key)
                                    if prop:
                                        self._process_properties(prop, d_el[ds_sub_key], objects, object_tag_ref_map, parent_data=d_el, ds_sub_key=ds_sub_key, object_key_ind=i)
                                    else:
                                        if self.options.get('unmapped_fallback') and ds_sub_key not in object_tag_ref_map['ds_key_cybox']:
                                            cust_prop = {"key": "x-" + self.data_source.replace("_", "-") + "." + ds_sub_key, "object": "cust_object"}
                                            self._process_properties(cust_prop, d_el[ds_sub_key], objects, object_tag_ref_map, parent_data=d_el, ds_sub_key=ds_sub_key, object_key_ind=i)
                    else:
                        if data is not None or data == '':
                            transformer = self.transformers[to_stix_config_prop['transformer']] if 'transformer' in to_stix_config_prop else None
                            references = references = to_stix_config_prop['references'] if 'references' in to_stix_config_prop else None
                            unwrap = True if 'unwrap' in to_stix_config_prop and isinstance(data, list) else False
                            group = to_stix_config_prop['group'] if 'group' in to_stix_config_prop else False
                            cybox = to_stix_config_prop.get('cybox', self.cybox_default)
                            substitute_key = to_stix_config_prop['ds_key'] if 'ds_key' in to_stix_config_prop else None

                            if self.callback:
                                try:
                                    generic_hash_key = self.callback(parent_data, ds_sub_key, key, self.options)
                                    if generic_hash_key:
                                       key = generic_hash_key
                                except Exception as e:
                                    return

                            config_keys = key.split('.')
                            if len(config_keys) < 2:
                                if False is cybox: 
                                    object_tag_ref_map['out_cybox'][key] = self._compose_value_object(data, [], observable_key=key, object_tag_ref_map=object_tag_ref_map, transformer=transformer, references=references, unwrap=unwrap, group=group)
                                return

                            type_name = config_keys[0]
                            property_key = config_keys[1]
                            parent_key = to_stix_config_prop['object'] if 'object' in to_stix_config_prop else type_name
                            
                            if False is cybox and not substitute_key:
                                value = self._compose_value_object(data, config_keys[2:], observable_key=key, object_tag_ref_map=object_tag_ref_map, transformer=transformer, references=references, unwrap=unwrap, group=group)
                                self._add_prperty(type_name, property_key, type_name, value, object_tag_ref_map['out_cybox'], cybox=False)
                            else:
                                if object_key_ind:
                                    parent_key = '%s_%s' % (parent_key, object_key_ind)
                                
                                # use the hard-coded value in the mapping
                                if 'value' in to_stix_config_prop:
                                    value = to_stix_config_prop['value']
                                else:
                                    if substitute_key and parent_data:
                                        data = parent_data.get(substitute_key)

                                        if False is cybox: 
                                            object_tag_ref_map['ds_key_cybox'][substitute_key] = True
                                    
                                    value = self._compose_value_object(data, config_keys[2:], observable_key=key, object_tag_ref_map=object_tag_ref_map, transformer=transformer, references=references, unwrap=unwrap, group=group)
                                    
                                if value is None or value == '':
                                    return None                                
                                    
                                if not references and unwrap and isinstance(value, list):
                                    for i, val_el in enumerate(value):
                                        parent_key_ind = self._get_tag_ind(parent_key, object_tag_ref_map, create_on_absence=True, unwrap=i, property_key=property_key)
                                        self._add_prperty(type_name, property_key, parent_key_ind, val_el, objects, group=group)
                                else:
                                    parent_key_ind = self._get_tag_ind(parent_key, object_tag_ref_map, create_on_absence=True, property_key=property_key)
                                    self._add_prperty(type_name, property_key, parent_key_ind, value, objects, group=group)

            elif isinstance(to_stix_config_prop, list):
                for prop in to_stix_config_prop:
                    self._process_properties(prop, data, objects, object_tag_ref_map, parent_data=parent_data, object_key_ind=object_key_ind)

            else:
                # self.logger.debug('to_stix_config_prop is neither dictionary nor list')
                # self.logger.debug(to_stix_config_prop)
                pass
        except Exception as e:
            raise Exception("Error in json_to_stix_translator._process_properties: %s" % e)

    # STIX 2.1 helper methods
    def _generate_and_apply_deterministic_id(self, object_id_map, cybox_objects):
        # Generates ID based on common namespace and SCO properties (omitting id and spec_version)
        # TODO: Handle references when part of ID contributing properties

        with open("stix_shifter_utils/stix_translation/src/json_to_stix/id_contributing_properties.json", 'r') as f:
            contributing_properties_definitions =  json.load(f)

        for key, cybox in cybox_objects.items():
            object_id_map[key] = ""
            cybox_properties = {}
            cybox_type = cybox.get("type")
            contributing_properties = contributing_properties_definitions.get(cybox_type)

            if contributing_properties:
                for contr_prop in contributing_properties:
                    if type(contr_prop) is list: # list of hash types
                        for hashtype in contr_prop:
                            hash_prop = "hashes.{}".format(hashtype)
                            if hash_prop in cybox:
                                cybox_properties[hash_prop] = cybox[hash_prop]
                                break
                    elif contr_prop in cybox and not re.match(".*_ref$", contr_prop): # chicken and egg problem with refs
                        cybox_properties[contr_prop] = cybox[contr_prop] 
                if cybox_properties:
                    unique_id = cybox_type + "--" + str(uuid.uuid5(namespace=uuid.UUID(UUID5_NAMESPACE), name=json.dumps(cybox_properties)))
                else:
                    self.logger.error("STIX object '{}' needs at least one of the following properties to generate ID {}".format(cybox_type, contributing_properties))
            else: # STIX process or custom object used UUID4 for identifier
                unique_id = "{}--{}".format(cybox_type, str(uuid.uuid4()))

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
            object_tag_ref_map = {UUID5_NAMESPACE: 0, 'tags': {}, 'non_ref_props': {}, 'out_cybox': {}, 'ds_key_cybox': {}}

            self._process_properties(ds_map, obj, object_map, object_tag_ref_map)
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

    def _cleanup_references(self, objects, tags):
        new_objects = {}

        tag_keys = list(tags.keys())
        tag_keys.sort(key=lambda x: int(x))

        for ind in tag_keys:
            new_objects[ind] = objects[ind]
            
        return new_objects