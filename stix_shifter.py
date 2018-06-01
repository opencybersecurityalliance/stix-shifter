# Main module to be called
from src import base_module
import sys
import argparse


class StixShifter:
    """
    StixShifter class - implements the features of qapputils
    """

    def __init__(self):
        self.args = []

    def translateResults(self):
        """
        Display the output of all of the data collected from the various services
            default is table format
            -j will return in json format
            -r (with -j) will return the additional raw data collected from the services)
        :param qapps: collection of QApp objects
        :type qapps: dict(string,Qapp)
        :return: exit code to exit with
        :rtype: integer
        """
        print('hi')

    def translateQuery(self):
        """
        Display the output of all of the data collected from the various services
            default is table format
            -j will return in json format
            -r (with -j) will return the additional raw data collected from the services)
        :param qapps: collection of QApp objects
        :type qapps: dict(string,Qapp)
        :return: exit code to exit with
        :rtype: integer
        """
        print('hi')

    def main(self):
        """
        Main function that sets up argument parsing then calls the proper command function
        In the case of converting a stix pattern to datasource query, arguments will take the form of...
        <data_source> <input_format> <stix_pattern>
        The data_source and input_format will determine what module and method gets called
        """

        # Process arguments
        parser = argparse.ArgumentParser(description='stix_shifter')
        subparsers = parser.add_subparsers(dest='command', help="sub-command help")

        # translate query command
        query_parser = subparsers.add_parser('translateQuery', help='Translate an input query to another format')
        query_parser.add_argument('format_out', help='What format should the query be translated to', choices=['qradar'])
        query_parser.add_argument('format_in', help='What format is the given query in',  choices=['sco'])
        query_parser.add_argument('query', help='The query string to be translated', type=str)
        query_parser.add_argument('-p', '--pretty', action="store_true", help='Optional Argument')

        # translate results command
        result_parser = subparsers.add_parser('translateResults', help="Translate a result set to another format")
        result_parser.add_argument('format_out', help='What format should the results be translated to', choices=['stix'])
        result_parser.add_argument('format_in', help='What format is the given results in',  choices=['qradar'])
        result_parser.add_argument('results', help='The results to be translated ', type=str)
        result_parser.add_argument('-p', '--pretty', action="store_true", help='Optional Argument')

        self.args = parser.parse_args()

        if self.args.command is None:
            parser.print_help(sys.stderr)
            sys.exit(1)

        methodToCall = getattr(self, "%s" % self.args.command)
        exit_code = methodToCall()
        exit(exit_code)


if __name__ == "__main__":
    Shifter = StixShifter()
    Shifter.main()
