import json
from stix_shifter_utils.modules.base.stix_transmission.base_query_connector \
    import BaseQueryConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from aiohttp.client_exceptions import ClientConnectionError

class BadRequestQueryError(Exception):
    pass

class LimitOutOfRangeError(Exception):
    pass

class QueryConnector(BaseQueryConnector):
    """ Query connector base class """
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def create_query_connection(self, query):
        """
        init query
        :param query
        :return:queryId
        """
        try:
            # Construct a response object
            return_obj = {}
            response_dict = {}

            response = await self.api_client.create_search(query)
            if isinstance(response, dict):
                return response
            response_code = response.code

            response_txt = response.read().decode('utf-8')
            response_dict = json.loads(response_txt)

            if response_code == 200:
                return_obj['success'] = True
                return_obj['search_id'] = response_dict['data']['queryId']
            elif response_code == 401:
                return_obj['success'] = False
                response_code = response_dict.get("errors")[0].get("code")
                if response_code == 4010010:
                    return_obj['error'] = "Authentication failed"
            elif response_code == 400:
                return_obj['success'] = False
                response_code = response_dict.get("errors")[0].get("code")
                if response_code == 4000040:
                    raise BadRequestQueryError

                if response_code == 4000010:
                    raise LimitOutOfRangeError
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except ClientConnectionError:
            response_dict['type'] = "ConnectionError"
            response_dict['message'] = "Invalid Host"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except LimitOutOfRangeError:
            response_dict['type'] = "LimitOutOfRangeError"
            response_dict['message'] = "Limit must be greater than or equal to 1 " \
                                       "and less than or equal to 100000"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except BadRequestQueryError:
            response_dict['type'] = "BadRequestQueryError"
            response_dict['message'] = response_dict.get("errors")[0].get("detail")
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except Exception as ex:
            response_dict['type'] = "unknown"
            response_dict['message'] = ex
            self.logger.error('error when creating search: %s', str(ex))
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj