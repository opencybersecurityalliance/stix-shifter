import sys
import importlib
import argparse

MODULES = ['qradar', 'dummy', 'aql_passthrough']

RESULTS = 'results'
QUERY = 'query'


class StixShifter:
    """
    StixShifter class - implements translations of stix data
    """

    def __init__(self):
        self.args = []

    def main(self):
        """
        In the case of converting a stix pattern to datasource query, arguments will take the form of...
        <module> <input_data_translation> <data>
        The module and input_translation_type will determine what module and method gets called
        """

        # Process arguments
        parser = argparse.ArgumentParser(description='stix_shifter')
        subparsers = parser.add_subparsers(dest='command', help="sub-command help")

        # translate query command
        translation_parser = subparsers.add_parser('translate',
                                             help='Translate a query or result set using a specific translation module')
        translation_parser.add_argument('module', help='What translation module to use',
                                  choices=MODULES)
        translation_parser.add_argument('action', help='What translation action to perform', choices=[RESULTS, QUERY])
        translation_parser.add_argument('data', help='The data to be translated', type=str)

        self.args = parser.parse_args()

        if self.args.command is None:
            parser.print_help(sys.stderr)
            sys.exit(1)

        result = self.translate(self.args.module, self.args.action, self.args.data)
        print(result)
        exit(0)

    def translate(self, module, translation_type, data):
        """
        Translated queries to a specified format
        :param module: What module to use
        :type module: one of MODULES 'qradar', 'dummy', 'aql_passthrough'
        :param translation_type: translation of a query or result set must be either 'results' or 'query'
        :type translation_type: str
        :param data: the data to translate
        :type data: str
        :return: translated results
        :rtype: str
        """
        if module not in MODULES:
            raise NotImplementedError

        translator_module = importlib.import_module(
            "src.modules." + module + "." + module + "_translator")

        interface = translator_module.Translator()

        if translation_type == QUERY:
            # Converting STIX pattern to datasource query
            return interface.transform_query(data)
        elif translation_type == RESULTS:
            # Converting data from the data source to STIX objects
            return interface.translate_results(data)
        else:
            raise NotImplementedError


if __name__ == "__main__":
    Shifter = StixShifter()
    Shifter.main()
