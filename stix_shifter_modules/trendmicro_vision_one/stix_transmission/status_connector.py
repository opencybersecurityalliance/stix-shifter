from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import BaseStatusConnector


class StatusConnector(BaseStatusConnector):
    async def create_status_connection(self, search_id):
        return {"success": True, "status": "COMPLETED", "progress": 100}
