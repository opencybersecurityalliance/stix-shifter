from abc import ABCMeta, abstractmethod
import json
import os

from stix_shifter_utils.utils import logger

class BaseResultTranslator(object, metaclass=ABCMeta):

    def __init__(self, options, dialect, base_file_path=None, callback=None):
        self.dialect = dialect
        self.options = options
        filepath = os.path.abspath(
            os.path.join(base_file_path, "json", "to_stix_map.json"))
        self.default_mapping_file_path = filepath
        self.callback = callback
        self.map_data = {}
        self.logger = logger.set_logger(__name__)

        mapping = options['mapping'] if 'mapping' in options else {}
        if mapping and dialect in mapping:
            map_data = mapping[dialect]
            if 'to_stix' in map_data:
                self.map_data = map_data['to_stix']
        if not self.map_data:
            try:
                map_file = self.read_mapping_file(self.default_mapping_file_path)
                self.map_data = json.loads(map_file)
            except Exception as ex:
                self.logger.error(ex)

    def read_mapping_file(self, path):
        return open(path).read()

    @abstractmethod
    def translate_results(self, data_source, data):
        """
        Translates data into STIX results based on a mapping file
        :param data_source: STIX identity object representing a data source
        :type data_source: str
        :param data: data to translate into STIX format
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to translate the given data to STIX. This should default to something if it hasn't been passed in
        :type mapping: str (filepath)
        :return: translated STIX formatted results
        :rtype: str
        """
        # if translating some datasource to STIX results...
        raise NotImplementedError()
