"""
Results Connector

See: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/adapter-guide/develop-transmission-module.md
"""
from stix_shifter_utils.modules.base.stix_transmission.base_json_results_connector import BaseJsonResultsConnector
from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.error_response import ErrorResponder

class ResultsConnector(BaseJsonResultsConnector):
    """
    Class that handles results connector integration.

    NOTE: This connector performs the actual query execution (of the query parsed in query_constructor). Response is the raw
    native payload response. The response would then be translated into a STIX object.

    :param api_client: api_client for connecting with Infoblox APIs
    :type api_client: api_client

    Attributes:
        api_client (ApiClient): Infoblox API client
        logger (logger): Internal logger
    """
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def create_results_connection(self, search_id, offset, length):
        """
        Creates a synchronous results connection (executing a single query and returning the response).

        :param search_id: query string
        :type search_id: str
        :param offset: results offset
        :type offset: int
        :param length: number of results to return
        :type length: int
        :return: response object (includes success and data fields)
        :rtype: object
        """
        try:
            min_range = int(offset)
            max_range = int(offset) + int(length)

            # Grab the response, extract the response code, and convert it to readable json
            response_dict = await self.api_client.get_search_results(search_id, min_range, max_range)
            response_code = response_dict["code"]

            # Construct a response object
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
                return_obj['data'] = response_dict['data']
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

            return return_obj
        except Exception as err:
            self.logger.error('error when getting search results: %s', err)
            raise
