import sys
import importlib

MODULES = ['qradar', 'dummy', 'car', 'cim', 'splunk', 'elastic', 'csa', 'csa:at', 'csa:nf']
RESULTS = 'results'
QUERY = 'query'


class StixShifter:
    """
    StixShifter class - implements translations of stix data
    """

    def __init__(self):
        self.args = []

    def translate(self, module, translate_type, data_source, data, options={}):
        """
        Translated queries to a specified format
        :param module: What module to use
        :type module: one of MODULES 'qradar', 'dummy'
        :param translate_type: translation of a query or result set must be either 'results' or 'query'
        :type translate_type: str
        :param data: the data to translate
        :type data: str
        :param options: translation options { stix_validator: bool }
        :type options: dict
        :return: translated results
        :rtype: str
        """
        dialect = None
        mod_dia = module.split(':', 1)
        module = mod_dia[0]
        if len(mod_dia) > 1:
            dialect = mod_dia[1]
        
        if module not in MODULES:
            raise NotImplementedError

        translator_module = importlib.import_module(
            "stix_shifter.src.modules." + module + "." + module + "_translator")

        if dialect is not None:
            interface = translator_module.Translator(dialect=dialect)
        else:
            interface = translator_module.Translator()

        if translate_type == QUERY:
            # Converting STIX pattern to datasource query
            return interface.transform_query(data, options)
        elif translate_type == RESULTS:
            # Converting data from the datasource to STIX objects
            return interface.translate_results(data_source, data, options)
        else:
            raise NotImplementedError
