from stix_shifter_utils.modules.base.stix_transmission.base_delete_connector import BaseDeleteConnector


class DeleteConnector(BaseDeleteConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def delete_query_connection(self, search_id):
        return {"success": True}
