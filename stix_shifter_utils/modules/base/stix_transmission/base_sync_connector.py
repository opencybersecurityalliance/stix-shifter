from .base_ping_connector import BasePingConnector
from .base_query_connector import BaseQueryConnector
from .base_status_connector import BaseStatusConnector
from .base_delete_connector import BaseDeleteConnector
from .base_results_connector import BaseResultsConnector
from .base_connector import BaseConnector


class BaseSyncConnector(BaseConnector):
    async def create_query_connection(self, query):
        return {"success": True, "search_id": query}

    async def create_status_connection(self, search_id):
        return {"success": True, "status": "COMPLETED", "progress": 100}

    async def delete_query_connection(self, search_id):
        return {"success": True}

