import json


class SplunkAuth():
    def __init__(self, api_client):
        self.api_client = api_client

    async def get_auth_token(self, auth):
        response = await self.api_client.get_auth_token(auth)
        return response
