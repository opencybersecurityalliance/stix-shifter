from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient
from azure.monitor.query import LogsQueryClient
from azure.identity import ClientSecretCredential
from azure.core.exceptions import HttpResponseError
import logging


class APIClient:
    """API Client to handle all calls."""

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        headers = dict()
        self.workspace_id = connection.get('workspaceId')
        self.host = connection.get('host')
        self.timeout = connection['options'].get('timeout')
        self.endpoint = 'v1/workspaces/{workspace_id}/query'.format(workspace_id=self.workspace_id)
        logger = logging.getLogger("azure.core.pipeline.policies.http_logging_policy")
        logger.setLevel(logging.WARNING)

        self.credential = ClientSecretCredential(tenant_id=configuration["auth"]["tenant"],
                                                 client_id=configuration["auth"]["clientId"],
                                                 client_secret=configuration["auth"]["clientSecret"])
        
        self.access_token = self.credential.get_token("https://{host}/.default".format(host=self.host))

        headers['Authorization'] = "Bearer " + self.access_token.token

        self.client = RestApiClient(self.host,
                                    connection.get('port', None),
                                    headers,
                                    cert_verify=connection.get('selfSignedCert', True),
                                    sni=connection.get('sni', None)
                                    )

    def ping_box(self):
        """Ping the endpoint."""
        return self.client.call_api(self.endpoint, 'GET', timeout=self.timeout)

    def run_search(self, query_expression, start, stop, length):
        """get the response from azure_sentinel endpoints
        :param query_expression: str, search_id
        :param length: int,length value
        :return: response, json object"""
        try:
            client = LogsQueryClient(self.credential)
            response = client.query_workspace(
                workspace_id=self.workspace_id,
                query=query_expression,
                timespan=(start, stop)
            )
            return {'success': True, "response": response}
        except HttpResponseError as er:
            return {'success': False, "error": er.error}
        except Exception as e:
            return {'success': False, "error": e}

    