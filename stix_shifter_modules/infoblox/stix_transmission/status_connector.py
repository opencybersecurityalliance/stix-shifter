"""
Status Connector
NOTE: Infoblox connector only supports a synchronous transmission module, so this connector is a template.
See: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/adapter-guide/develop-transmission-module.md
"""

from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import BaseStatusConnector


class StatusConnector(BaseStatusConnector):
    def create_status_connection(self, search_id):
        return {"success": True, "status": "COMPLETED", "progress": 100}
