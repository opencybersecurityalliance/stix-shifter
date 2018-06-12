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
        <module> <translate_type> <data>
        The module and translate_type will determine what module and method gets called
        """

        # process arguments
        parser = argparse.ArgumentParser(description='stix_shifter')
        subparsers = parser.add_subparsers(dest='command')

        ## translate parser
        translate_parser = subparsers.add_parser('translate', help='Translate a query or result set using a specific translation module')
        # positional arguments
        translate_parser.add_argument('module', choices=MODULES, help='what translation module to use')
        translate_parser.add_argument('translate_type', choices=[RESULTS, QUERY], help='what translation action to perform')
        translate_parser.add_argument('data', type=str, help='the data to be translated')
        # optional arguments
        translate_parser.add_argument('-x', '--stix-validator', action='store_true', help='run stix2 validator against the converted results')

        self.args = parser.parse_args()

        if self.args.command is None:
            parser.print_help(sys.stderr)
            sys.exit(1)

        options = {}
        if self.args.stix_validator:
            options['stix_validator'] = self.args.stix_validator

        result = self.translate(self.args.module, self.args.translate_type, self.args.data, options=options)
        print(result)
        exit(0)

    def translate(self, module, translate_type, data, options={}):
        """
        Translated queries to a specified format
        :param module: What module to use
        :type module: one of MODULES 'qradar', 'dummy', 'aql_passthrough'
        :param translate_type: translation of a query or result set must be either 'results' or 'query'
        :type translate_type: str
        :param data: the data to translate
        :type data: str
        :param options: translation options { stix_validator: bool }
        :type options: dict
        :return: translated results
        :rtype: str
        """

        if module not in MODULES:
            raise NotImplementedError

        translator_module = importlib.import_module(
            "src.modules." + module + "." + module + "_translator")

        interface = translator_module.Translator()

        if translate_type == QUERY:
            # Converting STIX pattern to datasource query
            return interface.transform_query(data, options)
        elif translate_type == RESULTS:
            # Converting data from the datasource to STIX objects
            return interface.translate_results(data, options)
        else:
            raise NotImplementedError


if __name__ == "__main__":
    Shifter = StixShifter()
    Shifter.main()
