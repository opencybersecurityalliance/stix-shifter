import json


class SplunkAuth():
    def __init__(self, api_client):
        self.api_client = api_client

    def get_auth_token(self, auth):
        response = self.api_client.get_auth_token(auth)
        return response
