from stix_shifter_utils.modules.base.stix_transmission.base_json_results_connector import BaseJsonResultsConnector
from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.error_response import ErrorResponder


class ResultsConnector(BaseJsonResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def create_results_connection(self, search_id, offset, length):
        response_dict = dict()
        return_obj = dict()
        try:
            offset_i = int(offset)
            len_i = int(length)
            min_range = offset_i
            if len_i > 1000:
                self.logger.warning("The length exceeds length limit. Use default length: 1000")
            max_range = offset_i + len_i if len_i <= 1000 else offset_i + 1000
            # Grab the response, extract the response code, and convert it to readable json
            response_dict = await self.api_client.get_search_results(search_id, min_range, max_range)
            response_code = response_dict["code"]

            # # Construct a response object
            if response_code == 200:
                return_obj['success'] = True
                data = response_dict['data']['logs']
                ResultsConnector.modify_result(data)
                return_obj['data'] = data
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            return return_obj
        except Exception as err:
            self.logger.error('error when getting search results: %s', err, exc_info=True)
            return_obj['success'] = False
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], error=err)
            return return_obj

    @classmethod
    def modify_result(cls, data):
        for log in data:
            registry_value = log.get("objectRegistryValue")
            if registry_value:
                registry_value_type = {"name": registry_value}
                registry_data = log.get("objectRegistryData")
                if registry_data:
                    registry_value_type["data"] = registry_data
                log["objectRegistryValueType"] = [registry_value_type]
            
            message_id = log.get("mail_message_id")
            if message_id:
                headers = log.get("mail_internet_headers")
                if headers:
                    headers.append({"HeaderName": "Message-ID", "Value": message_id})
                else:
                    log["mail_internet_headers"] = [{"HeaderName": "Message-ID", "Value": message_id}]