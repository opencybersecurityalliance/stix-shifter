from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector

class QueryConnector(BaseSyncConnector):
    def __init__(self, api_client):
        self.api_client = api_client