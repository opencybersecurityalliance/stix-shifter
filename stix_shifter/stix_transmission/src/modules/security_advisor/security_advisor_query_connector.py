from ..base.base_query_connector import BaseQueryConnector
import requests
import json

class SecurityAdvisorQueryConnector(BaseQueryConnector):
    def __init__(self, host,auth):
        self.host = host
        self.auth = auth

    def create_query_connection(self, query):

        return_obj = {}
        try : 
            return_obj['success'] = True
            return_obj['search_id'] = json.dumps(query)

        except Exception as e:
            return_obj['success'] = False
            return_obj['error'] = str(e)

        return return_obj

