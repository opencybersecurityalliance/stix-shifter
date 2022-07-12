from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient
import json


class APIClient:
    """API Client to handle all calls."""

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        headers = dict()
        auth = configuration.get('auth')
        workspace_id = connection.get('workspaceId')
        self.host = connection.get('host')
        self.timeout = connection['options'].get('timeout')
        self.endpoint = 'v1/workspaces/{workspace_id}/query'.format(workspace_id=workspace_id)

        if auth:
            if 'access_token' in auth:
                headers['Authorization'] = "Bearer " + auth['access_token']

        self.client = RestApiClient(self.host,
                                    connection.get('port', None),
                                    headers,
                                    cert_verify=connection.get('selfSignedCert', True),
                                    sni=connection.get('sni', None)
                                    )

    def ping_box(self):
        """Ping the endpoint."""
        return self.client.call_api(self.endpoint, 'GET', timeout=self.timeout)

    def run_search(self, query_expression, length):
        """get the response from azure_sentinel endpoints
        :param query_expression: str, search_id
        :param length: int,length value
        :return: response, json object"""
        headers = dict()
        payload = json.dumps({"query": query_expression})
        return self.client.call_api(self.endpoint, 'POST', headers, data=payload, timeout=self.timeout)
