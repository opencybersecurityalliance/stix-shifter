"""
Query Connector
NOTE: Infoblox connector only supports a synchronous transmission module, so this connector is a template.
See: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/adapter-guide/develop-transmission-module.md
"""

from stix_shifter_utils.modules.base.stix_transmission.base_connector import BaseQueryConnector


class QueryConnector(BaseQueryConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_query_connection(self, query):
        return {"success": True, "search_id": query}
