from stix_shifter_utils.modules.base.stix_transmission.base_query_connector import BaseQueryConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json

class QueryConnector(BaseQueryConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def create_query_connection(self, query):
        """
         Create the query Job for the input query
         :param query: dict
         :return: return_obj, dict
         """
        return_obj = {}
        try:
            if isinstance(query, str):
                query = json.loads(query)
            source = query.pop('source')
            response = await self.api_client.create_search(query)
            response_content = response.read().decode('utf-8')
            response_code = response.code
            if response_code == 200:
                return_obj['success'] = True
                response_content = json.loads(response_content)
                return_obj['search_id'] = f"{response_content['id']}:{source}"
            else:
                return_obj = self.handle_api_exception(response_code, response_content)

        except Exception as ex:
            self.logger.error('error while creating query in Crowdstrike Falcon Logscale: %s', ex)
            code = 408 if "timeout_error" in str(ex) else None
            return_obj = self.handle_api_exception(code, str(ex))

        return return_obj

    def handle_api_exception(self, code, response_txt):
        """
        create the exception response
        :param code, int
        :param response_txt, dict
        :return: return_obj, dict
        """
        return_obj = {}
        response_dict = {'code': code, 'message': str(response_txt)} if code else {'message': str(response_txt)}
        ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj
