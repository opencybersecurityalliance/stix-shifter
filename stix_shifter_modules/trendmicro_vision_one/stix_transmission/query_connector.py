from stix_shifter_utils.modules.base.stix_transmission.base_connector import BaseQueryConnector


class QueryConnector(BaseQueryConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    async def create_query_connection(self, query):
        return {"success": True, "search_id": query}
