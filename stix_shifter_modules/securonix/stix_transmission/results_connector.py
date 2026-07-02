import logging

logger = logging.getLogger(__name__)

class ResultsConnector():

    def __init__(self, api_client, connector):
        self.api_client = api_client
        self.connector = connector

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
                if 'events' in response_dict and response_dict['events']:
                    return_obj['data'] = response_dict['events']
                else:
                    return_obj['data'] = []
                    logger.warning(f"Response did not contain 'events' key or events list is empty. Assuming empty result. Full response: {response_dict}")
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

            return return_obj
        except Exception as err:
            self.logger.error('error when getting search results: %s', err)
