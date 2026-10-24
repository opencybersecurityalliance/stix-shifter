import json
import requests
from urllib.parse import urlencode
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
from datetime import datetime, timedelta
from stix_shifter_utils.utils import logger
import time
import re


class APIResponseException(Exception):
    def __init__(self, error_code, error_message, content_header_type, response):
        self.error_code = error_code
        self.error_message = error_message
        self.content_header_type = content_header_type
        self.response = response

    pass


class APIClient:
    TOKEN_ENDPOINT = '/Snypr/ws/token/generate'
    SEARCH_ENDPOINT = '/Snypr/ws/spotter/index/search'
    logger = logger.set_logger(__name__)

    def __init__(self):
        self.timeout = 60
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'user-agent': 'oca_stixshifter_1.0'
        }
        self.auth_headers = {
            'Content-Type': 'application/json',
            'user-agent': 'oca_stixshifter_1.0'
        }
        self._token_time = datetime.now() - timedelta(days=7)

    async def ping_box(self, client, base_url, auth_headers, headers, timeout):
        token = await self.get_token(client, base_url, auth_headers, timeout)
        headers['token'] = token
        params = {"query": "index=violation"}

        try:
            response = requests.get(
                f"{base_url}{self.SEARCH_ENDPOINT}",
                headers=headers,
                params=params,
                timeout=timeout,
                verify=False
            )
            response_data = response.json()
            self.logger.info(f"Ping Response: {response_data}")

            response_obj = type('response_obj', (), {
                'code': response.status_code,
                'content': json.dumps(response_data),
                'headers': response.headers
            })()
            return response_obj

        except Exception as e:
            self.logger.error(f"Error during ping box: {e}")
            raise e

    async def get_securonix_data(self, query, client, base_url, auth_headers, headers, timeout, queryId=None):
        token = await self.get_token(client, base_url, auth_headers, timeout)
        headers['token'] = token
        headers['Accept'] = '*/*'
        headers['Content-Type'] = 'application/json'

        # Extract IP and resourcegroup from query
        ip_match = re.search(r"sourceaddress = '([^']+)'", query)
        resource_match = re.search(r"resourcegroupname = '([^']+)'", query)

        ip = ip_match.group(1) if ip_match else None
        resourcegroup = resource_match.group(1) if resource_match else None

        now = datetime.now()
        past_24_hours = now - timedelta(hours=24)

        params = {
            "query": f"index=activity AND resourcegroupname=\"{resourcegroup}\"",
            "eventtime_from": past_24_hours.strftime('%m/%d/%Y %H:%M:%S'),
            "eventtime_to": now.strftime('%m/%d/%Y %H:%M:%S'),
            "sourceaddress": ip
        }

        base_url = base_url.rstrip('/')
        full_url = f"{base_url}/Snypr/ws/spotter/index/search"

        try:
            response = requests.get(
                full_url,
                headers=headers,
                params=params,
                timeout=timeout,
                verify=False
            )


            # Check if response is not empty
            if response.text:
                response_data = response.json()
            else:
                response_data = {"events": [], "message": "Empty response received"}

            response_obj = type('response_obj', (), {
                'code': response.status_code,
                'content': json.dumps(response_data),
                'headers': response.headers
            })()
            return response_obj

        except Exception as e:
            raise e

    async def get_token(self, client, base_url, auth_headers, timeout) -> str:
        if (datetime.now() - self._token_time) >= timedelta(minutes=30):
            try:
                response = requests.get(
                    f"{base_url}{self.TOKEN_ENDPOINT}",
                    headers=auth_headers,
                    timeout=timeout,
                    verify=False
                )
                if 200 <= response.status_code < 300:
                    token = response.text.strip('"')
                    self._token = token
                    self._token_time = datetime.now()
                    return token
                else:
                    raise APIResponseException(
                        response.status_code,
                        response.text,
                        response.headers.get('Content-Type'),
                        response
                    )
            except Exception as e:
                self.logger.error(f"Error getting token: {e}")
                raise e
        return self._token
