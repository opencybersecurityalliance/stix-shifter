from stix_shifter_utils.modules.base.stix_transmission.base_delete_connector import BaseDeleteConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger

class DeleteConnector(BaseDeleteConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def delete_query_connection(self, search_id):
        """
        Detete the search id
        :param search_id: str
        :return: return_obj, dict
        """
        return_obj = {}
        try:
            search_id = search_id.split(":")[0]
            response = await self.api_client.delete_search(search_id)
            response_code = response.code
            response_content = response.read().decode('utf-8')
            if response_code == 204:
                return_obj['success'] = True
            else:
                return_obj = self.handle_api_exception(response_code, response_content)

        except Exception as ex:
            self.logger.error('error while Deleting Query Job Id in Crowdstrike Falcon Logscale: %s', ex)
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
        if code == 404 and str(response_txt) == "":
            response_txt = "Search Id not found"
        response_dict = {'code': code, 'message': str(response_txt)} if code else {'message': str(response_txt)}
        ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj


