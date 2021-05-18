"""Apiclient for MSATP"""
import json
from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient

DEFAULT_LIMIT = 10000
DEFAULT_OFFSET = 0


class DetectionAPIClient:
    INCIDENTS_IDS_ENDPOINT = 'queries/incidents/v1'
    INCIDENTS_INFO_ENDPOINT = 'entities/incidents/GET/v1'
    """API Client to handle all calls."""

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""

        headers = dict()
        url_modifier_function = None
        auth = configuration.get('auth')
        self.endpoint_start = 'incidents/'
        self.host = connection.get('host')

        if auth:
            if 'access_token' in auth:
                headers['Authorization'] = "Bearer " + auth['access_token']

        self.client = RestApiClient(connection.get('host'),
                                    connection.get('port', None),
                                    headers,
                                    url_modifier_function=url_modifier_function,
                                    cert_verify=connection.get('selfSignedCert', True),
                                    sni=connection.get('sni', None)
                                    )
        self.timeout = connection['options'].get('timeout')

    def get_incidents_IDs(self, filter, sort):
        """get the response from MSatp endpoints
        :param filter: filter incidents by certain value
        :param sort: sort incidents according to sort value
        :return: response, json object"""
        headers = dict()
        params = dict()
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        endpoint = self.endpoint_start + self.INCIDENTS_IDS_ENDPOINT
        params['filter'] = filter
        params['sort'] = sort
        return self.client.call_api(endpoint, 'GET', headers=headers, params=params, timeout=self.timeout)

    def get_incidents_info(self, ids_lst, offset=DEFAULT_OFFSET, length=DEFAULT_LIMIT):
        """get the response from crowdstrike endpoints
        :param ids: Provide one or more incident IDs
        :return: response, json object"""
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        endpoint = self.endpoint_start + self.INCIDENTS_INFO_ENDPOINT
        ids_expression = json.dumps({'ids': ids_lst}).encode("utf-8")
        return self.client.call_api(endpoint, 'POST', headers=headers, data=ids_expression, timeout=self.timeout)

