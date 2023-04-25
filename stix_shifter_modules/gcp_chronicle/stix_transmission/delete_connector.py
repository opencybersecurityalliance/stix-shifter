from stix_shifter_utils.modules.base.stix_transmission.base_delete_connector import BaseDeleteConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json
from aiogoogle.excs import HTTPError
from aiohttp.client_exceptions import ClientConnectionError
from asyncio.exceptions import TimeoutError


class DeleteConnector(BaseDeleteConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def delete_query_connection(self, search_id):

        """
        Deletes the search id.
        :param search_id:str
        :return dict
        """
        return_obj = {}
        response_dict = {}
        try:

            response = await self.api_client.delete_search(search_id)
            response_code = response.status_code
            response_text = response.content

            if response_code == 200:
                return_obj['success'] = True
            else:
                response_dict['code'] = response_code
                response_dict['message'] = response_text['error']['message']
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except ClientConnectionError:
            response_dict['code'] = 1010
            response_dict['message'] = "Invalid Host"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except HTTPError as ex:
            if 'invalid_grant' in str(ex):
                response_dict['code'] = 1015
                response_dict['message'] = "Invalid Client Email"
            elif "not_found" in str(ex):
                response_dict['code'] = 1002
                response_dict['message'] = "Could not find search id {}".format(search_id)
            else:
                response_dict['message'] = str(ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except ValueError as d_ex:
            if 'Could not deserialize key data' in str(d_ex):
                response_dict['message'] = d_ex
                response_dict['code'] = 1015
            else:
                response_dict['message'] = f'cannot parse {d_ex}'
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except TimeoutError as ex:
            response_dict['code'] = 120
            response_dict['message'] = 'TimeoutError ' + str(ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except Exception as d_err:
            response_dict['message'] = d_err
            self.logger.error('error when getting search results: %s', d_err)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        return return_obj
