from ..base.base_query_connector import BaseQueryConnector

# Note: This query connector is a bit abnormal because the carbonblack
# api is synchronous. Therefore to generate a search_id we return
# the actual query as the search_id which should then be passed to the
# results connector


class CarbonBlackQueryConnector(BaseQueryConnector):

    def create_query_connection(self, query):
        return {"success": True, "search_id": query}
