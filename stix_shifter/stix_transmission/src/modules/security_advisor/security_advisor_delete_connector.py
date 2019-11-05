from ..base.base_delete_connector import BaseDeleteConnector
import json


class SecurityAdvisorDeleteConnector(BaseDeleteConnector):
    def __init__(self, host, auth ):
        self.host = host
        self.auth = auth

    def delete_query_connection(self, search_id):

        dict = { "success" : True}
        return dict