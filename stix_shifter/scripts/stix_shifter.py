import argparse
import sys
import json
import time
import importlib
from flask import Flask
import logging
import copy
from stix_shifter.stix_translation import stix_translation
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_utils.utils.proxy_host import ProxyHost
from stix_shifter_utils.utils.module_discovery import process_dialects, modules_list
from stix_shifter_utils.utils import logger as utils_logger
from stix_shifter_utils.utils.logger import exception_to_string

TRANSLATE = 'translate'
TRANSMIT = 'transmit'
EXECUTE = 'execute'
HOST = 'host'
MAPPING = 'mapping'
MODULES = 'modules'


def main():
    """
    Stix-shifter can either be called to either translate or transmit.
    In the case of translation, stix-shifter either translates a stix pattern to a datasource query,
    or converts data source query results into JSON of STIX observations.
    Arguments will take the form of...
    "translate" <module> <translate_type (query or results)> <data (STIX pattern or query results)> <options>
    The module and translate_type will determine what module and method gets executed.
    Option arguments comes in as:
      "{
          "mapping": <mapping hash for stix pattern to datasource and data results to stix observation objects>,
          "resultSizeLimit": <integer limit number for max results in the data source query>,
          "timeRange": <integer time range for LAST x MINUTES used in the data source query when START STOP qualifiers are absent>
       }"
    In the case of transmission, stix-shifter connects to a datasource to execute queries, status updates, and result retrieval.
    Arguments will take the form of...
    "transmit" <module> '{"host": <host IP>, "port": <port>, "cert": <certificate>}', '{"auth": <authentication>}',
        <
            query <query string>,
            status <search id>,
            results <search id> <offset> <length>,
            ping,
            is_async
        >
    """

    # process arguments
    parent_parser = argparse.ArgumentParser(description='stix_shifter')
    parent_parser.add_argument('-d', '--debug', action='store_true',
                                  help='Print detail logs for debugging')
    parent_subparsers = parent_parser.add_subparsers(dest='command')

    # translate parser
    translate_parser = parent_subparsers.add_parser(
        TRANSLATE, help='Translate a query or result set using a specific translation module')

    # positional arguments
    translate_parser.add_argument(
        'module',
         help='The translation module to use')
    translate_parser.add_argument('translate_type', choices=[
        stix_translation.RESULTS, stix_translation.QUERY, stix_translation.PARSE], help='The translation action to perform')
    translate_parser.add_argument(
        'data_source', help='STIX identity object representing a datasource')
    translate_parser.add_argument(
        'data', type=str, help='The STIX pattern or JSON results to be translated')
    translate_parser.add_argument('options', nargs='?', help='Options dictionary')
    translate_parser.add_argument('recursion_limit', type=int, nargs='?', help='Maximum depth of Python interpreter stack')

    # optional arguments
    translate_parser.add_argument('-x', '--stix-validator', action='store_true',
                                  help='Run the STIX 2 validator against the translated results')
    # modules parser
    parent_subparsers.add_parser(MODULES, help='Get modules list')

    # mapping parser
    mapping_parser = parent_subparsers.add_parser(
        MAPPING, help='Get module mapping')
    # positional arguments
    mapping_parser.add_argument('module', help='The translation module to use')

    # transmit parser
    transmit_parser = parent_subparsers.add_parser(
        TRANSMIT, help='Connect to a datasource and exectue a query...')

    # positional arguments
    transmit_parser.add_argument(
        'module', 
        help='Choose which connection module to use'
    )
    transmit_parser.add_argument(
        'connection',
        type=str,
        help='Data source connection with host, port, and certificate'
    )
    transmit_parser.add_argument(
        'configuration',
        type=str,
        help='Data source authentication'
    )

    # operation subparser
    operation_subparser = transmit_parser.add_subparsers(title="operation", dest="operation_command")
    operation_subparser.add_parser(stix_transmission.PING, help="Pings the data source")
    query_operation_parser = operation_subparser.add_parser(stix_transmission.QUERY, help="Executes a query on the data source")
    query_operation_parser.add_argument('query_string', help='native datasource query string')
    results_operation_parser = operation_subparser.add_parser(stix_transmission.RESULTS, help="Fetches the results of the data source query")
    results_operation_parser.add_argument('search_id', help='uuid of executed query')
    results_operation_parser.add_argument('offset', help='offset of results')
    results_operation_parser.add_argument('length', help='length of results')
    resultsstix_operation_parser = operation_subparser.add_parser(stix_transmission.RESULTS_STIX, help="Fetches the results of the data source query, response is translated in STIX")
    resultsstix_operation_parser.add_argument('search_id', help='uuid of executed query')
    resultsstix_operation_parser.add_argument('offset', help='offset of results')
    resultsstix_operation_parser.add_argument('length', help='length of results')
    resultsstix_operation_parser.add_argument('data_source', help='STIX identity object representing a datasource')
    status_operation_parser = operation_subparser.add_parser(stix_transmission.STATUS, help="Gets the current status of the query")
    status_operation_parser.add_argument('search_id', help='uuid of executed query')
    delete_operation_parser = operation_subparser.add_parser(stix_transmission.DELETE, help="Delete a running query on the data source")
    delete_operation_parser.add_argument('search_id', help='id of query to remove')
    operation_subparser.add_parser(stix_transmission.IS_ASYNC, help='Checks if the query operation is asynchronous')

    execute_parser = parent_subparsers.add_parser(EXECUTE, help='Translate and fully execute a query')
    # positional arguments
    execute_parser.add_argument(
        'transmission_module',
        help='Which connection module to use'
    )
    execute_parser.add_argument(
        'module',
        help='Which translation module to use for translation'
    )
    execute_parser.add_argument(
        'data_source',
        type=str,
        help='STIX Identity object for the data source'
    )
    execute_parser.add_argument(
        'connection',
        type=str,
        help='Data source connection with host, port, and certificate'
    )
    execute_parser.add_argument(
        'configuration',
        type=str,
        help='Data source authentication'
    )
    execute_parser.add_argument(
        'query',
        type=str,
        help='Query String'
    )
    execute_parser.add_argument('-r', '--results', type=int, default=10,
                                help='Maximum number of returned results (default 10)')

    host_parser = parent_subparsers.add_parser(HOST, help='Host a local query service, for testing and development')
    host_parser.add_argument(
        'data_source',
        type=str,
        help='STIX Identity object for the data source'
    )
    host_parser.add_argument(
        'host_address',
        type=str,
        help='Proxy Host:Port'
    )
    host_parser.add_argument(
        'ssl_cert',
        type=str,
        help='SSL certificate filename'
    )
    host_parser.add_argument(
        'ssl_key',
        type=str,
        help='SSL key filename'
    )

    args = parent_parser.parse_args()

    help_and_exit = args.command is None

    if 'debug' in args and args.debug:
        utils_logger.init(logging.DEBUG)
    else:
        utils_logger.init(logging.INFO)

    log = utils_logger.set_logger(__name__)

    if 'module' in args:
        args_module_dialects = args.module

        options = {}
        if 'options' in args and args.options:
            options = json.loads(args.options)

        module = process_dialects(args_module_dialects, options)[0]

        try:
            importlib.import_module("stix_shifter_modules." + module + ".entry_point")
        except Exception as ex:
            log.debug(exception_to_string(ex))
            log.error('Module {} not found'.format(module))
            log.debug(exception_to_string(ex))
            help_and_exit = True

    if help_and_exit:
        parent_parser.print_help(sys.stderr)
        sys.exit(1)
    elif args.command == HOST:
        # Host means to start a local web service for STIX shifter, to use in combination with the proxy data source
        # module. This combination allows one to run and debug their stix-shifter code locally, while interacting with
        # it inside a service provider such as IBM Security Connect
        app = Flask("stix-shifter")

        @app.route('/transform_query', methods=['POST'])
        def transform_query():
            host = ProxyHost()
            return host.transform_query()

        @app.route('/translate_results', methods=['POST'])
        def translate_results():
            data_source_identity_object = args.data_source
            host = ProxyHost()
            return host.translate_results(data_source_identity_object)

        @app.route('/create_query_connection', methods=['POST'])
        def create_query_connection():
            host = ProxyHost()
            return host.create_query_connection()

        @app.route('/create_status_connection', methods=['POST'])
        def create_status_connection():
            host = ProxyHost()
            return host.create_status_connection()

        @app.route('/create_results_connection', methods=['POST'])
        def create_results_connection():
            host = ProxyHost()
            return host.create_results_connection()

        @app.route('/delete_query_connection', methods=['POST'])
        def delete_query_connection():
            host = ProxyHost()
            return host.delete_query_connection()

        @app.route('/ping', methods=['POST'])
        def ping_connection():
            host = ProxyHost()
            return host.ping_connection()

        @app.route('/is_async', methods=['POST'])
        def is_async():
            host = ProxyHost()
            return host.is_async()

        host_address = args.host_address.split(":")
        app.run(debug=True, port=int(host_address[1]), host=host_address[0], ssl_context=(args.ssl_cert, args.ssl_key))

    elif args.command == EXECUTE:
        # Execute means take the STIX SCO pattern as input, execute query, and return STIX as output
        
        translation = stix_translation.StixTranslation()
        connection_dict = json.loads(args.connection)
        configuration_dict = json.loads(args.configuration)
        translation_options = copy.deepcopy(connection_dict.get('options', {}))
        options['validate_pattern'] = True
        dsl = translation.translate(args.module, 'query', args.data_source, args.query, translation_options)
        transmission = stix_transmission.StixTransmission(args.transmission_module, connection_dict, configuration_dict)
        results = []
        log.info('Translated Queries: \n' + json.dumps(dsl, indent=4))
        if 'queries' not in dsl:
            exit(1)
        for query in dsl['queries']:
            search_result = transmission.query(query)
            if search_result["success"]:
                search_id = search_result["search_id"]

                if transmission.is_async():
                    time.sleep(1)
                    status = transmission.status(search_id)
                    if status['success']:
                        while status['progress'] < 100 and status['status'] == 'RUNNING':
                            log.debug(status)
                            status = transmission.status(search_id)
                        log.debug(status)
                    else:
                        raise RuntimeError("Fetching status failed")               
                result = transmission.results(search_id, 0, args.results - 1)
                if result["success"]:
                    log.debug("Search {} results is:\n{}".format(search_id, result["data"]))

                    # Collect all results
                    results += result["data"]
                else:
                    raise RuntimeError("Fetching results failed; see log for details" + str(result))
            else:
                log.error(str(search_result))
                exit(0)

        # Translate results to STIX
        translation_options = copy.deepcopy(connection_dict.get('options', {}))
        options['validate_pattern'] = True
        result = translation.translate(args.module, 'results', args.data_source, json.dumps(results), translation_options)
        log.info('STIX Results (written to stdout):\n')
        print(json.dumps(result, indent=4, sort_keys=False))
        exit(0)

    elif args.command == TRANSLATE:
        data = args.data
        if not data:
            data_lines = []
            for line in sys.stdin:
                data_lines.append(line)
            data = '\n'.join(data_lines)
        if args.stix_validator:
            options['stix_validator'] = args.stix_validator
        recursion_limit = args.recursion_limit if args.recursion_limit else 1000
        translation = stix_translation.StixTranslation()
        result = translation.translate(
            args.module, args.translate_type, args.data_source, data, options=options, recursion_limit=recursion_limit)
    elif args.command == MAPPING:
        translation = stix_translation.StixTranslation()
        result = translation.translate(args.module, stix_translation.MAPPING, None, None, options=options)
    elif args.command == MODULES:
        translation = stix_translation.StixTranslation()
        result = {}
        all_modules = modules_list()
        for m in all_modules:
            result[m] = translation.translate(m, stix_translation.DIALECTS, None, None)
    elif args.command == TRANSMIT:
        result = transmit(args)  # stix_transmission

    print(json.dumps(result, indent=4, sort_keys=False))
    exit(0)


def transmit(args):
    """
    Connects to datasource and executes a query, grabs status update or query results
    :param args:
    args: <module> '{"host": <host IP>, "port": <port>, "selfSignedCert": <certificate>}', '{"auth": <authentication>}',
    <
        query <query string>,
        status <search id>,
        results <search id> <offset> <length>,
        results_stix <search id> <offset> <length> <data_source>
        ping,
        is_async
    >
    """
    connection_dict = json.loads(args.connection)
    configuration_dict = json.loads(args.configuration)
    transmission = stix_transmission.StixTransmission(args.module, connection_dict, configuration_dict)

    operation_command = args.operation_command

    if operation_command == stix_transmission.QUERY:
        query = args.query_string
        result = transmission.query(query)
    elif operation_command == stix_transmission.STATUS:
        search_id = args.search_id
        result = transmission.status(search_id)
    elif operation_command == stix_transmission.RESULTS:
        search_id = args.search_id
        offset = args.offset
        length = args.length
        result = transmission.results(search_id, offset, length)
    elif operation_command == stix_transmission.RESULTS_STIX:
        search_id = args.search_id
        offset = args.offset
        length = args.length
        data_source = args.data_source
        result = transmission.results_stix(search_id, offset, length, data_source)
    elif operation_command == stix_transmission.DELETE:
        search_id = args.search_id
        result = transmission.delete(search_id)
    elif operation_command == stix_transmission.PING:
        result = transmission.ping()
    elif operation_command == stix_transmission.IS_ASYNC:
        result = transmission.is_async()
    else:
        raise NotImplementedError("Unknown operation \"{}\"".format(operation_command))
    return result


if __name__ == "__main__":
    main()
