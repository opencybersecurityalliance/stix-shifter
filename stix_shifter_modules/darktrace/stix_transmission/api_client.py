from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
from stix_shifter_utils.utils import logger
import hmac
import hashlib
import base64
import datetime

DEFAULT_LIMIT = 10000
DEFAULT_OFFSET = 0


class APIClient:
    QUERY_ENDPOINT = "advancedsearch/api/search/"
    PING_ENDPOINT = "status?includechildren=false&fast=false"

    def __init__(self, connection, configuration):
        self.logger = logger.set_logger(__name__)
        headers = {}
        url_modifier_function = None
        self.auth = configuration.get('auth')
        self.client = RestApiClientAsync(connection.get('host'), port=None,
                                    headers=headers, cert_verify=False,
                                    url_modifier_function=url_modifier_function
                                    )

    async def ping_box(self):
        """
            Ping the Data Source
            :return: Response object
        """
        encoded_query = self._encode_query("")
        headers = self.get_header(self.PING_ENDPOINT, encoded_query)
        return await self.client.call_api(self.PING_ENDPOINT, 'GET', headers=headers, data=None)

    async def get_search_results(self, query):
        """
        Get results from Data Source
        :param query: Data Source Query
        :return: Response Object
        """
        self.logger.debug("query: %s", query)
        encoded_query = self._encode_query(query)
        headers = self.get_header(self.QUERY_ENDPOINT, encoded_query)
        return await self.client.call_api(self.QUERY_ENDPOINT + encoded_query, 'GET', headers=headers, data=None)

    def get_header(self, endpoint,  query):
        query_url = "/" + endpoint + query
        time = datetime.datetime.utcnow()
        sig = hmac.new(self.auth["private_token"].encode("ASCII"),
                       msg=(query_url + "\n" + self.auth["public_token"] + "\n" +
                            time.isoformat(timespec="auto")).encode("ASCII"), digestmod=hashlib.sha1).hexdigest()
        header = {"DTAPI-Token": self.auth["public_token"], "DTAPI-Date": time.isoformat(timespec="auto"),
                  "DTAPI-Signature": sig}

        return header

    @staticmethod
    def _encode_query(_query):
        """
        Encode Query:
            - Encode query to base64 and convert to string.

        """
        _query_encode_bytes = base64.b64encode(bytes(_query, 'utf-8'))
        _query_encoded = str(_query_encode_bytes, 'utf-8')
        return _query_encoded
