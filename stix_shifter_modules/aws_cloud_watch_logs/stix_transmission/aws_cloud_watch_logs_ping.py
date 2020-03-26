from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
from stix_shifter_utils.utils.error_response import ErrorResponder


class AWSCloudWatchLogsPing(BasePingConnector):

    def __init__(self, client):
        self.client = client

    def ping(self):
        """
        Ping the endpoint
        :return: dict
        """
        return_obj = dict()
        response_dict = dict()
        try:
            self.client.describe_log_groups(**{})
            return_obj['success'] = True
        except Exception as ex:
            response_dict['__type'] = ex.__class__.__name__
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'])

        return return_obj
