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
        self.map_data = {}
        self.logger = logger.set_logger(__name__)
        filepath = os.path.abspath(os.path.join(base_file_path, "json", "to_stix_map.json"))
        self.map_data = self.read_json(filepath, options)
        self.transformers = get_module_transformers(base_file_path.split(os.sep)[-2])

    def read_json(self, filepath, options):
        return helper_read_json(filepath, options)

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
