import re
import logging
import uuid
from stix2validator import validate_instance, print_results
from . import observable
# convert JSON data to STIX object using map_data and transformers


def convert_to_stix(datasource, map_data, data, transformers):
    ds2stix = DataSourceObjToStixObj(
        datasource, map_data, transformers)

    # map data list to list of transformed objects
    results = list(map(ds2stix.transform, data))
    return results

# base class for valueTransformer


class ValueTransformer():
    """ Base class for value transformers """

    @staticmethod
    def transform(obj):
        """ abstract function for converting value to STIX format """
        raise NotImplemented


class DataSourceObjToStixObj():

    def __init__(self, datasource, dsToStixMap, transformers):
        self.dsToStixMap = dsToStixMap
        self.transformers = transformers
        self.datasource = datasource

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
        retVal = obj[ds_key]
        if transformer is not None:
            return transformer.transform(retVal)
        return retVal

    @staticmethod
    def _add_to_objects(key_to_add, stix_value, observation, index, ds_key,
                        refObjs, linked, linkedObjs):
        """ add the object from source to the resulting object
            Takes into consideration, if reference object and/or linked object
        """
        # splits the key on . to get child objects
        splitKey = key_to_add.split('.')
        typeStr = splitKey[0]
        # type is the root object type
        newObj = {
            'type': typeStr,
        }
        tmpObj = newObj
        childProps = splitKey[1:]

        # for each child property update down the chain to set the value
        for childProp in childProps:
            tmpObj.update({childProp: stix_value})

        refObjs.update({ds_key: index})
        # if the key is part of a linked object
        to_update = str(index)
        if linked is not None:
            # if linked object already exists get it and it's index
            if linked in linkedObjs:
                newObj = {**newObj, **linkedObjs[linked]['obj']}
                to_update = linkedObjs[linked]['index']
            # else add the object and increment the index
            else:
                observation['objects'].update({to_update: newObj})
                index = index + 1
            # update the linked objext
            linkedObjs[linked] = {"obj": newObj, "index": to_update}
        else:
            # just update the index
            index = index + 1

        # update the observation and the reference object
        observation['objects'].update({to_update: newObj})
        return index

    @staticmethod
    def _add_ref_to_objects(key_to_add, stix_value, observation, index, linked,
                            linkedObjs, transformer):
        """ add the reference to an object from source to the resulting object
            Takes into consideration, if linked object
        """
        splitKey = key_to_add.split('.')
        typeStr = splitKey[0]
        newObj = {
            'type': typeStr,
        }
        tmpObj = newObj
        childProps = splitKey[1:-1]

        for childProp in childProps:
            childObj = {}
            tmpObj.update({childProp: childObj})
            tmpObj = childObj

        if transformer is not None:
            stix_value = transformer.transform(stix_value)
        tmpObj.update({splitKey[-1]: stix_value})

        to_update = str(index)
        if linked is not None:
            if linked in linkedObjs:
                newObj = {**newObj, **linkedObjs[linked]['obj']}
                to_update = linkedObjs[linked]['index']
            else:
                observation['objects'].update({to_update: newObj})
                index = index + 1

            linkedObjs[linked] = {"obj": newObj, "index": to_update}
        else:
            index = index + 1

        observation['objects'].update({to_update: newObj})
        return index

    def transform(self, obj):
        """ Transforms the given object in to a STIX observation
            based on the mapping file and transform functions
        """
        refObjs = {}
        linkedObjs = {}
        stixType = 'observed-data'
        uniqID = str(uuid.uuid4())
        observation = {
            'x_com_ibm_uds_datasource': {'id': self.datasource['id'], 'name': self.datasource['name']},
            'id': stixType + '--' + uniqID,
            'type': stixType,
            'objects': {},
        }

        index = 0
        for ds_key in self.dsToStixMap:
            # get the stix keys that are mapped
            ds_key_def_obj = self.dsToStixMap[ds_key]
            ds_key_def_list = ds_key_def_obj if isinstance(
                ds_key_def_obj, list) else [ds_key_def_obj]
            for ds_key_def in ds_key_def_list:

                if (ds_key_def is None or 'key' not in ds_key_def or 'type' not in ds_key_def):
                    (logging.debug(
                        '{} is not valid (None, or missing key and type)'.format(ds_key_def)))
                    continue

                if ds_key_def['type'] != 'value':
                    continue

                key_to_add = ds_key_def['key']
                transformer = None
                if 'transformer' in ds_key_def:
                    transformer = self.transformers[ds_key_def['transformer']]
                linked = None
                if 'linked' in ds_key_def:
                    linked = ds_key_def['linked']

                stix_value = DataSourceObjToStixObj._get_value(obj, ds_key,
                                                               transformer)
                if stix_value is None:
                    continue

                prop_def = None
                prop_type = None

                # if outer property then set on outside
                if key_to_add in self.outer_props:
                    # TODO need to do something with isRequired
                    prop_def = self.outer_props[key_to_add]
                    prop_type = 'OUTER'

                # if simple prop then create new object
                for simple_prop_key in self.simple_props:
                    if (isinstance(key_to_add, str)
                            and key_to_add.startswith(simple_prop_key)):
                        # TODO need to do something with isRequired
                        prop_def = self.simple_props[simple_prop_key]
                        prop_type = 'SIMPLE'

                if prop_def is not None and 'valid_regex' in prop_def:
                    pattern = re.compile(prop_def['valid_regex'])
                    if not pattern.match(str(stix_value)):
                        continue
                # handle when object is linked
                if linked is not None:
                    key_to_add_split = key_to_add.split('.')
                    split_key = key_to_add_split[1]

                    # replace dashes with underscores to match stix formatting
                    observation_key = key_to_add_split[0].replace('-', '_')

                    if observation_key not in observation:
                        observation[observation_key] = {split_key: stix_value}
                    else:
                        observation[observation_key].update(
                            {split_key: stix_value})

                elif prop_type == 'OUTER':
                    observation.update({key_to_add: stix_value})
                else:
                    index = (self._add_to_objects(key_to_add, stix_value,
                                                  observation, index, ds_key,
                                                  refObjs, linked, linkedObjs))

        # complex types
        for ds_key in self.dsToStixMap:
            # get the stix keys that are mapped
            ds_key_def_obj = self.dsToStixMap[ds_key]
            ds_key_def_list = ds_key_def_obj if isinstance(
                ds_key_def_obj, list) else [ds_key_def_obj]
            for ds_key_def in ds_key_def_list:

                if (ds_key_def is None or
                        'key' not in ds_key_def or
                        'type' not in ds_key_def):
                    continue

                if ds_key_def['type'] != 'reference':
                    continue

                key_to_add = ds_key_def['key']
                transformer = None
                if 'transformer' in ds_key_def:
                    transformer = self.transformers[ds_key_def['transformer']]
                linked = None
                if 'linked' in ds_key_def:
                    linked = ds_key_def['linked']

                # if complex prop then create new object
                for complex_prop_key in self.complex_props:
                    if (isinstance(key_to_add, str) and key_to_add.startswith(complex_prop_key)):
                        # TODO need to do something with isRequired
                        stix_value = refObjs[ds_key]
                        if stix_value is None:
                            continue

                        index = self._add_ref_to_objects(
                            key_to_add, stix_value, observation, index,
                            linked, linkedObjs, transformer)

        # Validate each STIX object
        validated_result = validate_instance(observation)
        print_results(validated_result)
        return observation
