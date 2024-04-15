from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import BaseStatusConnector
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from enum import Enum
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json
class LogScaleStatus(Enum):
    EXECUTE = 'EXECUTE'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'

TAIL_MAXIMUM_LIMIT = 10000 # maximum tail limit of logscale


class StatusConnector(BaseStatusConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    @staticmethod
    def get_status( status):
        switcher = {
            LogScaleStatus.EXECUTE.value: Status.RUNNING,
            LogScaleStatus.COMPLETED.value: Status.COMPLETED,
            LogScaleStatus.CANCELED.value: Status.CANCELED
        }
        return switcher.get(status).value

    async def create_status_connection(self, search_id, metadata=None):
        """
         Poll the QueryJob to find the status of the query job
         :param search_id: str
         :param metadata: dict
         :return: return_obj, dict
         """
        return_obj = {}
        try:
            search_id = search_id.split(":")[0]

            response = await self.api_client.poll_query_job(search_id)
            response_code = response.code
            response_content = response.read().decode('utf-8')

            if response_code == 200:
                response_content = json.loads(response_content)
                return_obj['success'] = True

                if response_content.get('cancelled'):
                    return_obj['status'] = StatusConnector.get_status('CANCELED')
                    return_obj['progress'] = 0
                elif response_content.get('done'):
                    return_obj['status'] = StatusConnector.get_status('COMPLETED')
                    return_obj['progress'] = 100
                elif not response_content.get('done'):

                    return_obj['status'] = StatusConnector.get_status('EXECUTE')
                    event_count = response_content['metaData']['eventCount']
                    if metadata and metadata.get("length"):
                        progress_percent = int(event_count / metadata['length'] * 100)
                    else:
                        progress_percent = int(event_count/TAIL_MAXIMUM_LIMIT * 100)
                    return_obj['progress'] = progress_percent
            else:
                return_obj = self.handle_api_exception(response_code, response_content)

        except Exception as ex:
            self.logger.error('Error while fetching status from CrowdStrike Falcon Logscale API: %s', ex)
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
