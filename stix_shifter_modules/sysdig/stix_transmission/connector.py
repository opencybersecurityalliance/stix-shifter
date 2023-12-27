import json
from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from .api_client import APIClient


class InvalidMetadataException(Exception):
    pass


class Connector(BaseJsonSyncConnector):
    SYSDIG_MAX_PAGE_SIZE = 999

    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def create_results_connection(self, query, offset, length, metadata=None):
        """
        Fetching the results using query, offset and length
        :param query: str, Data Source query
        :param offset: str, Offset value
        :param length: str, Length value
        :param metadata: dict
        :return: return_obj, dict
        """
        return_obj = {}
        response_dict = {}
        data = []
        local_result_count = 0
        # Using 'prev' cursor instead of 'next' cursor in Sysdig since the records are returned in desc order by last
        # modified timestamp. The 'prev' is not None when all the results are returned in the first api call itself
        # and there are no more records.
        # Hence, checking for result_count returned from API call with the limit. When the result_count is less than
        # the limit, setting prev_page_token to None. This is to overcome Sysdig behaviour.
        try:
            if metadata:
                if isinstance(metadata, dict) and metadata.get('result_count') and metadata.get('prev_page_token'):
                    result_count, prev_page_token = metadata['result_count'], metadata['prev_page_token']
                    result_count = int(result_count)
                    total_records = int(length)
                    if abs(self.api_client.result_limit - result_count) < total_records:
                        total_records = abs(self.api_client.result_limit - result_count)

                else:
                    # Raise exception when metadata doesnt contain result count or next page token.
                    raise InvalidMetadataException(metadata)
            else:
                result_count, prev_page_token = 0, '0'
                total_records = int(offset) + int(length)
                if total_records > int(self.api_client.result_limit):
                    total_records = int(self.api_client.result_limit)
            if total_records <= Connector.SYSDIG_MAX_PAGE_SIZE:
                limit = total_records
            else:
                limit = Connector.SYSDIG_MAX_PAGE_SIZE
            query_limit = limit
            limit = f'&limit={limit}'
            if (result_count == 0 and prev_page_token == '0') or (prev_page_token != '0' and result_count <
                                                                  self.api_client.result_limit):
                """api call for searching alert based on query"""
                split_query = query.split('&filter=')
                if metadata:
                    response_wrapper = await self.api_client.get_search_results(
                        f'&cursor={prev_page_token}&filter={split_query[1]}{limit}')
                else:
                    response_wrapper = await self.api_client.get_search_results(query + limit)
                response_code = response_wrapper.code
                if response_code == 200:
                    response_dict = json.loads(response_wrapper.read())
                    return_obj['success'] = True
                    result_count += len(response_dict['data'])
                    local_result_count += len(response_dict['data'])
                    prev_page_token = response_dict['page'].get('prev')
                    if len(response_dict['data']) < query_limit:
                        prev_page_token = None
                    data += response_dict['data']
                    # Loop until if there is next page and records fetched is less than total records.
                    while prev_page_token:
                        if not metadata and result_count < total_records:
                            remaining_records = total_records - result_count
                        elif metadata and local_result_count < total_records:
                            remaining_records = total_records - local_result_count
                        else:
                            break
                        if remaining_records > Connector.SYSDIG_MAX_PAGE_SIZE:
                            limit = Connector.SYSDIG_MAX_PAGE_SIZE
                        else:
                            limit = remaining_records
                        query_limit = limit
                        limit = f'&limit={limit}'
                        prev_response_wrapper = await self.api_client.get_search_results(
                            f'&cursor={prev_page_token}&filter={split_query[1]}{limit}')
                        prev_response_code = prev_response_wrapper.code
                        prev_response_dict = json.loads(prev_response_wrapper.read())
                        if prev_response_code == 200:
                            result_count += len(prev_response_dict['data'])
                            local_result_count += len(response_dict['data'])
                            prev_page_token = prev_response_dict['page'].get('prev')
                            if len(prev_response_dict['data']) < query_limit:
                                prev_page_token = None
                            data += prev_response_dict['data']
                        else:
                            return_obj = self.exception_response(prev_response_wrapper.code,
                                                                 prev_response_dict.get('error'))
                            data = []
                            break
                    if data:
                        self.update_event(data)

                        if metadata:
                            return_obj['data'] = data if data else []
                        else:
                            return_obj['data'] = data[int(offset):total_records] if data else []

                        if prev_page_token and result_count < self.api_client.result_limit:
                            return_obj['metadata'] = {"result_count": result_count,
                                                      "prev_page_token": str(prev_page_token)}
                    else:
                        if not return_obj.get('error') and return_obj.get('success') is not False:
                            return_obj['success'] = True
                            return_obj['data'] = []
                else:
                    if response_code == 401:
                        message = 'cannot verify credentials'
                    else:
                        response_dict = json.loads(response_wrapper.read())
                        message = response_dict.get('message')
                    return_obj = self.exception_response(response_wrapper.code, message)
            else:
                return_obj['success'] = True
                return_obj['data'] = []

        except InvalidMetadataException as ex:
            response_dict['code'] = 100
            response_dict['message'] = f'Invalid metadata: {str(ex)}'
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except Exception as ex:
            if "timeout_error" in str(ex):
                response_dict['code'] = 408
            response_dict['message'] = str(ex)
            self.logger.error('error when getting search results: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'],
                                      connector=self.connector)
        return return_obj

    @staticmethod
    def update_event(data):
        """
        Set the finding_type as 'threat' for the event.
        Replace invalid <NA> tag with empty string.
        Parse the fd.name and set the fields for network-traffic in the event.
        """
        for event in data:
            fields = event["content"]["fields"]
            # replace unsupported field value <NA> with empty string
            for f in fields:
                if fields[f] == '<NA>':
                    fields[f] = ''

            # Setting the finding_type for the event as 'threat'
            event["finding_type"] = "threat"
            # Parsing network fields from event data
            if fields.get("evt.type") and fields["evt.type"] == "connect":
                if "->" in fields["fd.name"]:
                    source, destination = fields["fd.name"].split('->')
                    event["direction"] = "out"
                    event["clientIpv4"], event["clientPort"] = source.split(":")
                    event["serverIpv4"], event["serverPort"] = destination.split(":")
                elif "<-" in fields["fd.name"]:
                    destination, source = fields["fd.name"].split('<-')
                    event["direction"] = "in"
                    event["clientIpv4"], event["clientPort"] = source.split(":")
                    event["serverIpv4"], event["serverPort"] = destination.split(":")
                if fields.get('fd.l4proto'):
                    event["l4protocol"] = fields['fd.l4proto']
                else:
                    event["l4protocol"] = "tcp"

            # Adding ancestor names in list
            fields["proc.anames"] = [val for key, val in fields.items() if 'proc.aname' in key and len(val) > 0]

    async def ping_connection(self):
        """
        Ping the endpoint
        :return: dict
        """
        return_obj = {}
        response_dict = {}
        try:
            response = await self.api_client.ping_data_source()
            response_code = response.code
            if response_code == 200:
                return_obj['success'] = True
            else:
                return_obj = self.exception_response(response_code, 'cannot verify credentials')
        except Exception as ex:
            response_dict['message'] = ex
            self.logger.error('error while pinging: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'],
                                      connector=self.connector)
        return return_obj

    def exception_response(self, code, response_txt):
        """
        create the exception response
        :param code, int
        :param response_txt, dict
        :return: return_obj, dict
        """
        return_obj = {}
        response_dict = {'code': code, 'message': str(response_txt)}
        ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj
