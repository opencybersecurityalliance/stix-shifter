from stix_shifter_utils.modules.base.stix_transmission.base_query_connector import BaseQueryConnector
import re
import json
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class UnexpectedResponseException(Exception):
    pass


class QueryConnector(BaseQueryConnector):

    PATTERN = '<ID>(.*)</ID>'
    DEFAULT_ID = 'UNKNOWN'

    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def create_query_connection(self, query):
        response_txt = None
        return_obj = dict()
        try:
            response = await self.api_client.create_search(query)
            response_code = response.code
            response_txt = response.read().decode('utf-8')
            search_id = self.DEFAULT_ID
            search = re.search(self.PATTERN, response_txt, re.IGNORECASE)

            if search:
                search_id = search.group(1)
            
            return_obj['search_id'] = search_id
            if 199 < response_code < 300 and search_id != self.DEFAULT_ID:
                return_obj['success'] = True
            elif ErrorResponder.is_plain_string(response_txt):
                ErrorResponder.fill_error(return_obj, message=response_txt, connector=self.connector)
            elif ErrorResponder.is_json_string(response_txt):
                response_json = json.loads(response_txt)
                ErrorResponder.fill_error(return_obj, response_json, ['arguments'], connector=self.connector)
            else:
                raise UnexpectedResponseException
        except Exception as e:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise e
        return return_obj
