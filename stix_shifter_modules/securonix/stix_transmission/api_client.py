import json
import requests
from datetime import datetime, timedelta
from stix_shifter_utils.utils import logger
import re


class APIResponseException(Exception):
    def __init__(self, error_code, error_message, content_header_type, response):
        self.error_code = error_code
        self.error_message = error_message
        self.content_header_type = content_header_type
        self.response = response


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
        self._token = None

    async def get_securonix_data(self, query, client, base_url, auth_headers, headers, timeout, queryId=None,
                                 nextCursorMarker=None):
        token = await self.get_token(client, base_url, auth_headers, timeout)
        headers['token'] = token
        headers['Accept'] = '*/*'
        headers['Content-Type'] = 'application/json'

        # Extract eventtime parameters from the query string using regex
        eventtime_from_match = re.search(r'eventtime>="([^"]+)"', query)
        eventtime_to_match = re.search(r'eventtime<="([^"]+)"', query)

        eventtime_from = eventtime_from_match.group(1) if eventtime_from_match else None
        eventtime_to = eventtime_to_match.group(1) if eventtime_to_match else None

        # Clean the query by removing eventtime conditions
        clean_query = re.sub(r'AND\s+eventtime>="\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2}"', '', query)
        clean_query = re.sub(r'AND\s+eventtime<="\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2}"', '', clean_query)

        # If no eventtime parameters found, use default 24-hour window
        if not eventtime_from or not eventtime_to:
            now = datetime.now()
            past_24_hours = now - timedelta(hours=24)
            eventtime_from = past_24_hours.strftime('%m/%d/%Y %H:%M:%S')
            eventtime_to = now.strftime('%m/%d/%Y %H:%M:%S')

        params = {
            "query": clean_query,
            "eventtime_from": eventtime_from,
            "eventtime_to": eventtime_to
        }

        if queryId:
            params["queryId"] = queryId
        if nextCursorMarker:
            params["nextCursorMarker"] = nextCursorMarker

        base_url = base_url.rstrip('/')
        full_url = f"{base_url}{self.SEARCH_ENDPOINT}"

        try:
            response = requests.get(
                full_url,
                headers=headers,
                params=params,
                timeout=timeout,
                verify=False
            )

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
        base_url = base_url.rstrip('/')
        if self._token is None or (datetime.now() - self._token_time) >= timedelta(minutes=30):
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