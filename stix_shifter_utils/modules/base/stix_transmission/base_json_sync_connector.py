from .base_json_connector import BaseJsonConnector


class BaseJsonSyncConnector(BaseJsonConnector):
    async def create_query_connection(self, query):
        return {"success": True, "search_id": query}

    async def create_status_connection(self, search_id):
        return {"success": True, "status": "COMPLETED", "progress": 100}

    async def delete_query_connection(self, search_id):
        return {"success": True}

