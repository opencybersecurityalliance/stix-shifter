from .base_ping_connector import BasePingConnector
from .base_query_connector import BaseQueryConnector
from .base_status_connector import BaseStatusConnector
from .base_delete_connector import BaseDeleteConnector
from .base_results_connector import BaseResultsConnector
from .base_connector import BaseConnector
from asyncio import sleep


class BaseSyncConnector(BaseConnector):
    async def create_query_connection(self, query):
        # await sleep(0)
        return {"success": True, "search_id": query}

    async def create_status_connection(self, search_id):
        await sleep(0)
        return {"success": True, "status": "COMPLETED", "progress": 100}

