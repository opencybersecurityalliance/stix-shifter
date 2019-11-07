from ..base.base_status_connector import BaseStatusConnector
from ..base.base_status_connector import Status

import requests


class SecurityAdvisorStatusConnector(BaseStatusConnector):
    def __init__(self, host, auth):
        self.host = host
        self.auth = auth

    def create_status_connection(self, search_id):
        
        ret_obj = {}
        ret_obj['success'] = True
        ret_obj['status'] = 'COMPLETED'

        ret_obj['progress']  = '100'

        return ret_obj
        