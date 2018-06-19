import re
import logging
import uuid
from stix2validator import validate_instance, print_results
from . import observable
# convert JSON data to STIX object using map_data and transformers


def convert_to_stix(datasource, map_data, data, transformers, options):
    ds2stix = DataSourceObjToStixObj(
        datasource, map_data, transformers, options)

    # map data list to list of transformed objects
    results = list(map(ds2stix.transform, data))
    return results


class DataSourceObjToStixObj:

    def __init__(self, datasource, dsToStixMap, transformers, options):
        self.datasource = datasource
        self.dsToStixMap = dsToStixMap
        self.transformers = transformers

        # parse through options
        self.stix_validator = options.get('stix_validator', False)

        self.common_props = observable.common_props
        self.observation_props = observable.observation_props

        # outer props
        self.outer_props = {**self.common_props, **self.observation_props}

        self.simple_props = observable.simple_props
        self.complex_props = observable.complex_props

    @staticmethod
    def _merge_dicts(dict1, dict2):
        z = dict1.copy()
        z.update(dict2)
        return z

    @staticmethod
    def _get_value(obj, ds_key, transformer):
        """ get value from source object, transforming if specified """
        if ds_key not in obj:
            logging.debug('{} not found in object'.format(ds_key))
            return None
        ret_val = obj[ds_key]
        if transformer is not None:
            return transformer.transform(ret_val)
        return ret_val

    @staticmethod
    def _handle_linked(key_to_add, observation, stix_value):
        # replace dashes with underscores to match stix formatting
        observation_key = key_to_add.split('.')[0].replace('-', '_')
        key_to_add_split = key_to_add.split('.')
        split_key = key_to_add_split[1]

        if observation_key not in observation:
            observation[observation_key] = {split_key: stix_value}
        else:
            observation[observation_key].update({split_key: stix_value})

        return observation

    @staticmethod
    def _determine_prop_attr(key_to_add, outer_props, simple_props):
        prop_type = None
        prop_def = None
        # if outer property then set on outside
        if key_to_add in outer_props:
            prop_def = outer_props[key_to_add]
            prop_type = 'OUTER'
        # if simple prop then create new object
        for simple_prop_key in simple_props:
            if isinstance(key_to_add, str) and key_to_add.startswith(simple_prop_key):
                prop_def = simple_props[simple_prop_key]
                prop_type = 'SIMPLE'

        return [prop_def, prop_type]

    @staticmethod
    def _create_complex_objects(ds_map, transformers, index, observation, ref_objs, linked_objs, obj):
        for ds_key in ds_map:
            # get the stix keys that are mapped
            ds_key_def_obj = ds_map[ds_key]
            ds_key_def_list = ds_key_def_obj if isinstance(ds_key_def_obj, list) else [ds_key_def_obj]
            for ds_key_def in ds_key_def_list:
                if ds_key_def is None or 'key' not in ds_key_def or 'type' not in ds_key_def:
                    continue
                if ds_key_def['type'] != 'reference' and 'cybox' not in ds_key_def:
                    continue

                key_to_add = ds_key_def['key']
                transformer = transformers[ds_key_def['transformer']] if 'transformer' in ds_key_def else None
                linked = ds_key_def['linked'] if 'linked' in ds_key_def else None

                # if complex prop then create new object
                for complex_prop_key in observable.complex_props:
                    if isinstance(key_to_add, str) and key_to_add.startswith(complex_prop_key):
                        # TODO need to do something with isRequired
                        stix_value = ref_objs[ds_key] if ds_key_def['type'] == 'reference' else None
                        stix_value = DataSourceObjToStixObj._get_value(obj, ds_key, transformer) \
                            if 'cybox' in ds_key_def else stix_value
                        index = DataSourceObjToStixObj._add_to_objects(
                            key_to_add, stix_value, observation, index, ds_key, ref_objs,
                            linked, linked_objs, False, transformer)

    @staticmethod
    def _add_to_objects(key_to_add, stix_value, observation, index, ds_key,
                        ref_objs, linked, linked_objs, is_obj, transformer):

        """ add the object from source to the resulting object
            Takes into consideration, if reference object and/or linked object
        """
        to_update = str(index)
        split_key = key_to_add.split('.')
        type_str = split_key[0]
        # type is the root object type
        new_obj = {'type': type_str}
        tmp_obj = new_obj

        if is_obj:
            child_props = split_key[1:]
            # for each child property update down the chain to set the value
            for child_prop in child_props:
                tmp_obj.update({child_prop: stix_value})
            ref_objs.update({ds_key: index})
        else:
            child_props = split_key[1:-1]
            for child_prop in child_props:
                child_obj = {}
                tmp_obj.update({child_prop: child_obj})
                tmp_obj = child_obj
            if transformer is not None:
                if stix_value is None:
                    return index
                stix_value = transformer.transform(stix_value)

            tmp_obj.update({split_key[-1]: stix_value})

        # if the key is part of a linked object
        if linked is not None:
            # if linked object already exists get it and it's index
            if linked in linked_objs:
                new_obj = {**new_obj, **linked_objs[linked]['obj']}
                to_update = linked_objs[linked]['index']
            # else add the object and increment the index
            else:
                observation['objects'].update({to_update: new_obj})
                index = index + 1
            # update the linked object
            linked_objs[linked] = {"obj": new_obj, "index": to_update}
        else:
            index = index + 1
        observation['objects'].update({to_update: new_obj})
        return index

    def transform(self, obj):
        """ Transforms the given object in to a STIX observation
            based on the mapping file and transform functions
        """

        index = 0
        ref_objs = {}
        linked_objs = {}
        stix_type = 'observed-data'
        uniq_id = str(uuid.uuid4())
        ds_map = self.dsToStixMap
        xformers = self.transformers
        observation = {
            'x_com_ibm_uds_datasource': {'id': self.datasource['id'], 'name': self.datasource['name']},
            'id': stix_type + '--' + uniq_id,
            'type': stix_type,
            'objects': {},
        }
        # create normal type objects
        for ds_key in ds_map:
            # get the stix keys that are mapped
            ds_key_def_obj = self.dsToStixMap[ds_key]
            ds_key_def_list = ds_key_def_obj if isinstance(ds_key_def_obj, list) else [ds_key_def_obj]
            for ds_key_def in ds_key_def_list:
                if ds_key_def is None or 'key' not in ds_key_def or 'type' not in ds_key_def:
                    logging.debug('{} is not valid (None, or missing key and type)'.format(ds_key_def))
                    continue
                if ds_key_def['type'] != 'value' or 'cybox' in ds_key_def:
                    continue

                key_to_add = ds_key_def['key']
                transformer = xformers[ds_key_def['transformer']] if 'transformer' in ds_key_def else None
                linked = ds_key_def['linked'] if 'linked' in ds_key_def else None
                stix_value = DataSourceObjToStixObj._get_value(obj, ds_key, transformer)

                if stix_value is None:
                    continue

                prop_obj = DataSourceObjToStixObj._determine_prop_attr(key_to_add, self.outer_props, self.simple_props)
                if prop_obj[0] is not None and 'valid_regex' in prop_obj[0]:
                    pattern = re.compile(prop_obj[0]['valid_regex'])
                    if not pattern.match(str(stix_value)):
                        continue
                # handle when object is linked
                if linked is not None:
                    observation = DataSourceObjToStixObj._handle_linked(key_to_add, observation, stix_value)
                elif prop_obj[1] == 'OUTER':
                    observation.update({key_to_add: stix_value})
                else:
                    index = (self._add_to_objects(key_to_add, stix_value, observation, index, ds_key,
                                                  ref_objs, linked, linked_objs, True, None))
        # create complex type objects
        DataSourceObjToStixObj._create_complex_objects(ds_map, xformers, index, observation, ref_objs, linked_objs, obj)
        # Validate each STIX object
        if self.stix_validator:
            validated_result = validate_instance(observation)
            print_results(validated_result)
        return observation
