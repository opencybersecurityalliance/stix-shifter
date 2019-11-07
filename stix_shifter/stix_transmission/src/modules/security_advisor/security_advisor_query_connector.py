from ..base.base_query_connector import BaseQueryConnector
import requests

import json

from flatten_json import flatten

class SecurityAdvisorQueryConnector(BaseQueryConnector):
    def __init__(self, host,auth):
        self.host = host
        self.auth = auth

    def create_query_connection(self, query):

        ret_obj = {}
        try : 
            ret_obj['success'] = True
            ret_obj['search_id'] = json.dumps(query)

        except Exception as e:
            ret_obj['success'] = False
            ret_obj['error'] = str(e)

        return ret_obj

