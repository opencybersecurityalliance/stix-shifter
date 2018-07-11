import argparse
import sys
from stix_shifter import stix_shifter


def __main__():
    """
    In the case of converting a stix pattern to datasource query, arguments will take the form of...
    <module> <translate_type> <data>
    The module and translate_type will determine what module and method gets called
    """

    # process arguments
    parser = argparse.ArgumentParser(description='stix_shifter')
    subparsers = parser.add_subparsers(dest='command')

    # translate parser
    translate_parser = subparsers.add_parser(
        'translate', help='Translate a query or result set using a specific translation module')
    # positional arguments
    translate_parser.add_argument(
        'module', choices=stix_shifter.MODULES, help='what translation module to use')
    translate_parser.add_argument('translate_type', choices=[
        stix_shifter.RESULTS, stix_shifter.QUERY], help='what translation action to perform')
    translate_parser.add_argument(
        'data_source', help='data source uuid')
    translate_parser.add_argument(
        'data', type=str, help='the data to be translated')
    # optional arguments
    translate_parser.add_argument('-x', '--stix-validator', action='store_true',
                                  help='run stix2 validator against the converted results')

    args = parser.parse_args()

    if args.command is None:
        parser.print_help(sys.stderr)
        sys.exit(1)

    options = {}
    if args.stix_validator:
        options['stix_validator'] = args.stix_validator

    shifter = stix_shifter.StixShifter()
    result = shifter.translate(
        args.module, args.translate_type, args.data_source, args.data, options=options)

    print(result)
    exit(0)


if __name__ == "__main__":
    __main__()
