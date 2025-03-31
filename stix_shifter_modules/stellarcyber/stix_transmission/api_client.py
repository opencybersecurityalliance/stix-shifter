from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
from urllib.parse import urlunparse, urlencode
import json
import base64
import requests
import datetime

class APIClient():

    def __init__(self, connection, configuration):
        # Uncomment when implementing data source API client.
        auth = configuration.get('auth')
        self.api_key = auth.get('api_key')
        self.user_id = auth.get('user_id')
        self.host = connection.get('host')
        self.access_token = None
        self.token_expiry = None
        self.client = RestApiClientAsync(self.host)

        self.timeout = connection['options'].get('timeout')

    async def ping_data_source(self):
        # Pings the data source
        return {"code": 200, "success": True}
    
    async def get_jwt_token(self):
        auth = base64.b64encode(bytes(self.user_id + ":" + self.api_key, "utf-8")).decode("utf-8")
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        endpoint = "connect/api/v1/access_token"
        try:
            res = await self.client.call_api(endpoint, 'POST', headers=headers)
            res.raise_for_status()
            try:
                return json.loads(res.read())
            except (KeyError, json.JSONDecodeError) as e:
                raise Exception(f"Invalid response format: {e!s}. Response: {res.text}")
        except requests.RequestException as e:
            raise Exception(
                f"HTTP request failed: {e!s}. Status code: {e.response.status_code if e.response else 'N/A'}"
            )
        except Exception as e:
            raise Exception(f"Unexpected error fetching access token: {e!s}")
    
    async def get_access_token(self):
        if self.access_token is None or self.token_expiry < datetime.datetime.now().timestamp():
            token_response = await self.get_jwt_token()
            self.access_token = token_response["access_token"]
            self.token_expiry = token_response["exp"]
        return self.access_token
    
    async def parse_user_results(self, results):
        data = []
        for result in results.get('profile', []):
            result['last_seen'] = results.get('last_seen')
            result['risk_score'] = results.get('risk_score')
            result['user_id'] = result.get('id')
            del result['id']
            data.append(result)
        return data
    
    async def get_search_results(self, search_id, range_start=None, range_end=None):
        index_string, query = search_id.split("&")
        index = index_string.split("=")[1]
        endpoint = f"connect/api/data/{index}-*/_search"
        query = {"q": query}
        query_string = urlencode(query)
        endpoint = f"{endpoint}?{query_string}"

        jwt_token = await self.get_access_token()
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json",
        }
        response = await self.client.call_api(endpoint, 'GET', headers=headers)
        results = json.loads(response.read())
        data = []
        for result in results['hits']['hits']:
            if index == "aella-users":
                data.extend(await self.parse_user_results(result.get('_source')))
            else:
                data.append(result.get('_source'))
        # Return the search results. Results must be in JSON format before being translated into STIX
        return {"code": 200, "data": data}

    async def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}
