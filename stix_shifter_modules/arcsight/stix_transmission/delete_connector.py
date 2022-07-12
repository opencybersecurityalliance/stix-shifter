import json
from stix_shifter_utils.modules.base.stix_transmission.base_delete_connector import BaseDeleteConnector
from stix_shifter_utils.utils.error_response import ErrorResponder


class DeleteConnector(BaseDeleteConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.connector = __name__.split('.')[1]

    async def delete_query_connection(self, search_id):
        """
        Function to delete search id if the status in Running
        :param search_id: str, search id
        :return: dict
        """
        return_obj = dict()
        try:
            search_id_length = len(search_id.split(':'))
            search_id_values = search_id.split(':')
            if search_id_length in [2, 3]:
                search_session_id, user_session_id = search_id_values[0], search_id_values[1]
            else:
                raise SyntaxError("Invalid search_id format : " + str(search_id))

            response = await self.api_client.delete_search(search_session_id, user_session_id)
            raw_response = response.read()
            response_code = response.code

            if 199 < response_code < 300:
                return_obj['success'] = True
            # arcsight logger error codes - currently unavailable state
            elif response_code in [500, 503]:
                response_string = raw_response.decode()
                ErrorResponder.fill_error(return_obj, response_string, ['message'], connector=self.connector)
            elif json.loads(raw_response):
                raw_response = json.loads(raw_response)
                response_dict = raw_response['errors'][0]
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            else:
                raise Exception(raw_response)
        except Exception as err:
            return_obj = dict()
            response_error = err
            ErrorResponder.fill_error(return_obj, response_error, ['message'], connector=self.connector)

        return return_obj
