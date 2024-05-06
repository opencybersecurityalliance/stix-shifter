from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import BaseStatusConnector
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status


class StatusConnector(BaseStatusConnector):
    def __init__(self, host, auth):
        self.host = host
        self.auth = auth

    async def create_status_connection(self, search_id):
        
        return_obj = {}
        return_obj['success'] = True
        return_obj['status'] = 'COMPLETED'
        return_obj['progress']  = '100'

        return return_obj
        