from abc import ABCMeta, abstractmethod
import os
from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.file_helper import read_json as helper_read_json
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers


class BaseResultTranslator(object, metaclass=ABCMeta):

    def __init__(self, options, dialect, base_file_path=None, callback=None):
        self.dialect = dialect
        self.options = options
        self.callback = callback
        self.module_name = base_file_path.split(os.sep)[-2]
        self.logger = logger.set_logger(__name__)
        self.map_data = self.fetch_mapping(base_file_path, dialect, options)
        self.transformers = get_module_transformers(self.module_name)

    def read_json(self, filepath, options):
        return helper_read_json(filepath, options)

    def fetch_mapping(self, basepath, dialect, options):
        """
        Fetches datasource-to-STIX mapping JSON from the module's <DIALECT>_to_stix_map.json file
        :param basepath: path of data source translation module
        :type basepath: str
        """
        stix_2_0_mapping_directory_path = os.path.join(basepath, 'json')
        stix_2_1_mapping_directory_path = os.path.join(basepath, 'json/stix_2_1')
        mapping_file = f'{dialect}_to_stix_map.json'
        to_stix_path = os.path.join(basepath, 'json', mapping_file)
        if not os.path.isfile(to_stix_path):
            # use default mapping file since 'default_stix_map.json' isn't a real dialect
            mapping_file = 'to_stix_map.json'
        if options.get("stix_2.1") and os.path.isdir(stix_2_1_mapping_directory_path):
            to_stix_path = os.path.join(stix_2_1_mapping_directory_path, mapping_file)
        else:
            to_stix_path = os.path.join(stix_2_0_mapping_directory_path, mapping_file)

        if os.path.isdir(stix_2_0_mapping_directory_path) and not os.path.isfile(to_stix_path):
            raise Exception('BaseResultTranslator Error: ' + to_stix_path + ' is not found for dialect ' + dialect)

        return self.read_json(to_stix_path, options)

    @abstractmethod
    def translate_results(self, data_source, data):
        """
        Translates data into STIX results based on a mapping file
        :param data_source: STIX identity object representing a data source
        :type data_source: str
        :param data: data to translate into STIX format
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to translate the given data to STIX.
        :  This should default to something if it hasn't been passed in
        :type mapping: str (filepath)
        :return: translated STIX formatted results
        :rtype: str
        """
        # if translating some datasource to STIX results...
        raise NotImplementedError()
