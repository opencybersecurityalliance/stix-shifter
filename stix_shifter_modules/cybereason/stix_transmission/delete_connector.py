from stix_shifter_utils.modules.base.stix_transmission.base_delete_connector import BaseDeleteConnector
from stix_shifter_utils.utils import logger


class DeleteConnector(BaseDeleteConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    def delete_query_connection(self, query):
        """
        Delete query response
        :param query:
        :return:
        """
        return {"success": True, "search_id": query}
