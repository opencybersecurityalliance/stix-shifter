import json
import re
from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder

MAX_LIMIT = 10000

# Static list, additional protocols can be added here in future
PROTOCOLS_LIST = ["transportProtocol", "applicationProtocol"]
FILE_HASHES = ["MD5", "SHA256", "SHA1"]


class ResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.connector = __name__.split('.')[1]

    async def create_results_connection(self, search_id, offset, length):
        """
        Fetching the results using search id, offset and length
        :param search_id: str, search id generated in transmit query
        :param offset: str, offset value
        :param length: str, length value
        :return: dict
        """
        return_obj = dict()
        try:
            min_range = int(offset)
            max_range = int(length)
            max_range = max_range if max_range <= MAX_LIMIT else MAX_LIMIT
            search_id_length = len(search_id.split(':'))
            search_id_values = search_id.split(':')
            if search_id_length in [2, 3]:
                search_session_id, user_session_id = search_id_values[0], search_id_values[1]
            else:
                raise SyntaxError("Invalid search_id format : " + str(search_id))

            response = await self.api_client.get_search_results(search_session_id, user_session_id, min_range, max_range)
            raw_response = response.read()
            response_code = response.code

            if 199 < response_code < 300:
                return_obj['success'] = True
                response_dict = json.loads(raw_response)
                if response_dict:
                    final_response = list(map(lambda mapping: dict(zip(list(map(lambda schema: schema['name'],
                                                                                response_dict['fields'])), mapping)),
                                              response_dict['results']))
                    event_data = list()
                    for log in final_response:
                        self.format_results(log, event_data)
                    return_obj['data'] = event_data
                else:
                    return_obj['data'] = response_dict
            # arcsight logger error codes - currently unavailable state
            elif response_code in [500, 503]:
                response_string = raw_response.decode()
                ErrorResponder.fill_error(return_obj, response_string, ['message'], connector=self.connector)
            elif isinstance(json.loads(raw_response), dict):
                response_error = json.loads(raw_response)
                response_dict = response_error['errors'][0]
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            else:
                raise Exception(raw_response)

        except Exception as err:
            return_obj = dict()
            response_error = err
            ErrorResponder.fill_error(return_obj, response_error, ['message'], connector=self.connector)

        return return_obj

    def format_results(self, log, event_data):
        """
        Formatting the results
        :param log: dict
        :param event_data: list, results
        """
        protocols = list()
        default = 'unknown'
        # building list of protocols
        for protocol in PROTOCOLS_LIST:
            if log.get(protocol):
                protocols.append(log[protocol])
        if protocols:
            log['protocols'] = protocols

        # formatting file hash values
        if log.get('fileHash'):
            temp = log.get('fileHash').split(',')
            for values in temp:
                for hashes in FILE_HASHES:
                    if values.__contains__(hashes):
                        log[hashes] = values.split('=')[1]

        # default finding type for custom cybox object
        if not log.get('categorySignificance'):
            log['categorySignificance'] = default

        # fetching  process id for linux based smart connectors
        if log.get('message'):
            self.fetch_linux_pid(log)

        # custom check for stix object creation
        self.object_creation_check(log, event_data)

    def object_creation_check(self, log, event_data):
        """
        Stix object creation check, to prevent Stix validation error
        :param log: dict
        :param event_data: list, results
        """
        build_data = dict()
        registry_connector = 'Sysmon'
        # custom check for registry object creation
        if log.get('filePath'):
            if log.get('deviceAction') and log.get('deviceProduct') == registry_connector and \
                    log.get('deviceAction').__contains__("Registry"):
                self.registry_format(log)
                del log['filePath']
            # custom check for file object creation
            elif not log.get('fileName') or [hashes for hashes in FILE_HASHES if hashes in log]:
                del log['filePath']

        # custom check for network object creation
        if log.get('protocols') and (log.get('sourceAddress') or log.get('destinationAddress')):
            build_data['network_events'] = log
            event_data.append(build_data)
        else:
            build_data['other_events'] = log
            event_data.append(build_data)

    @staticmethod
    def registry_format(log):
        """
        Formatting registry values for Sysmon smart connector
        :param log: dict
        """
        registry_data = dict()
        if log.get('deviceCustomString4'):
            registry_data['registry_string'] = log['deviceCustomString4']
        registry_data['name'] = log['filePath'].split('\\')[-1]
        log['registry_key'] = log['filePath']
        log['registry_data'] = [registry_data]

    @staticmethod
    def fetch_linux_pid(log):
        """
        getting pid and ppid for linux based smart connectors from message field
        :param log: dict
        """
        pid_response = re.search(r'\spid=(\d+)', log['message'])
        ppid_response = re.search(r'ppid=(\d+)', log['message'])
        if pid_response:
            log['dpid'] = pid_response.group(1)
            if log.get('spid'):
                del log['spid']
        if ppid_response:
            log['spid'] = ppid_response.group(1)
