from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient
from azure.identity import ClientSecretCredential
import logging
import json


class APIClient:
    """API Client to handle all calls."""

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        headers = dict()
        logger = logging.getLogger("azure.core.pipeline.policies.http_logging_policy")
        logger.setLevel(logging.WARNING)
        self.host = connection.get('host')
        self.client_id = configuration['auth']['clientId']
        self.tenant_id = configuration['auth']['tenant']
        self.client_secret = configuration['auth']['clientSecret']
        self.credential = ClientSecretCredential(tenant_id=self.tenant_id,
                                                 client_id=self.client_id,
                                                 client_secret=self.client_secret)
        self.token = self.credential.get_token("https://{host}/.default".format(host=self.host))
        headers["Authorization"] = 'Bearer {token}'.format(token=self.token[0])
        headers['Accept'] = 'application/json'
        self.tenant_id = configuration['auth']['tenant']
        self.timeout = connection['options'].get('timeout')
        auth = configuration.get('auth')
        if auth:
            if 'access_token' in auth:
                headers['Authorization'] = "Bearer " + auth['access_token']
        self.client = RestApiClient(self.host,
                                    connection.get('port', None),
                                    headers,
                                    cert_verify=connection.get('selfSignedCert', True),
                                    sni=connection.get('sni', None)
                                    )
        workspace_id = connection.get('workspaceId')
        self.endpoint = 'v1/workspaces/{workspace_id}/query'.format(workspace_id=workspace_id)

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
        headers['Accept'] = 'application/json'
        headers["Authorization"] = 'Bearer {token}'.format(token=self.token[0])
        return self.client.call_api(self.endpoint, 'POST', headers, data=payload, timeout=self.timeout)
