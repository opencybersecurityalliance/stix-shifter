from ..base.base_ping import BasePing
import json
from .....utils.error_response import ErrorResponder


class CloudIdentityPing(BaseQueryConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def ping(self):
        return
    