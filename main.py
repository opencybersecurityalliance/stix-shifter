import argparse
import sys
from stix_shifter import stix_shifter
import json


TRANSLATE = 'translate'
TRANSMIT = 'transmit'


def __main__():
    """
    In the case of converting a stix pattern to datasource query, arguments will take the form of...
    <module> <translate_type> <data> <options>
    The module and translate_type will determine what module and method gets called
    Options argument comes in as:
      "{
          "select_fields": <string array of fields in the datasource select statement>},
          "mapping": <mapping hash for either stix pattern to datasource or data results to stix observation objects>,
          "result_limit": <integer limit number for max results in the data source query>,
          "timerange": <integer time window in minutes used in the data source query when START STOP qualifiers are absent>
       }"
    """

    # process arguments
    parser = argparse.ArgumentParser(description='stix_shifter')
    subparsers = parser.add_subparsers(dest='command')

    # translate parser
    translate_parser = subparsers.add_parser(
        TRANSLATE, help='Translate a query or result set using a specific translation module')

    # positional arguments
    translate_parser.add_argument(
        'module', choices=stix_shifter.TRANSLATION_MODULES, help='what translation module to use')
    translate_parser.add_argument('translate_type', choices=[
        stix_shifter.RESULTS, stix_shifter.QUERY], help='what translation action to perform')
    translate_parser.add_argument(
        'data_source', help='STIX identity object representing a datasource')
    translate_parser.add_argument(
        'data', type=str, help='the data to be translated')
    translate_parser.add_argument('options', nargs='?', help='options that can be passed in')

    # optional arguments
    translate_parser.add_argument('-x', '--stix-validator', action='store_true',
                                  help='run stix2 validator against the converted results')
    translate_parser.add_argument('-m', '--data-mapper',
                                  help='module to use for the data mapper')

    # transmit parser
    transmit_parser = subparsers.add_parser(
        TRANSMIT, help='Connect to a datasource and exectue a query...')

    # positional arguments
    transmit_parser.add_argument(
        'module', choices=stix_shifter.TRANSMISSION_MODULES,
        help='choose which connection module to use'
    )
    transmit_parser.add_argument(
        'connection',
        type=str,
        help='Data source Host'
    )
    transmit_parser.add_argument(
        'configuration',
        type=str,
        help='Data source Port'
    )
    transmit_parser.add_argument(
        'operation',
        type=str,
        help='Operation being performed by stix transmission'
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help(sys.stderr)
        sys.exit(1)

    shifter = stix_shifter.StixShifter()

    if args.command == TRANSLATE:
        options = json.loads(args.options) if bool(args.options) else {}
        if args.stix_validator:
            options['stix_validator'] = args.stix_validator
        if args.data_mapper:
            options['data_mapper'] = args.data_mapper
        result = shifter.translate(
            args.module, args.translate_type, args.data_source, args.data, options=options)
    elif args.command == TRANSMIT:
        result = shifter.transmit(args)
    else:
        result = "Must call either 'translate' or 'transmit'."

    print(result)
    exit(0)


if __name__ == "__main__":
    __main__()
