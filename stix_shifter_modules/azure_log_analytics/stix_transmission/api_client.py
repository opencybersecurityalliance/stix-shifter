from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
from azure.monitor.query.aio import LogsQueryClient
from azure.identity.aio import ClientSecretCredential
from azure.core.exceptions import HttpResponseError
import logging


class APIClient:
    """API Client to handle all calls."""

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        self.connection = connection
        self.configuration = configuration
        logger = logging.getLogger("azure.core.pipeline.policies.http_logging_policy")
        logger.setLevel(logging.WARNING)

    async def init_async_client(self):
        self.workspace_id = self.connection.get('workspaceId')
        self.host = self.connection.get('host')
        self.timeout = self.connection['options'].get('timeout')
        self.endpoint = 'v1/workspaces/{workspace_id}/query'.format(workspace_id=self.workspace_id)
        headers = dict()
        self.credential = ClientSecretCredential(tenant_id=self.configuration["auth"]["tenant"],
                                                 client_id=self.configuration["auth"]["clientId"],
                                                 client_secret=self.configuration["auth"]["clientSecret"])
        
        self.access_token = await self.credential.get_token("https://{host}/.default".format(host=self.host))
        headers['Authorization'] = "Bearer " + self.access_token.token
        self.client = RestApiClientAsync(self.host,
                                    self.connection.get('port', None),
                                    headers,
                                    cert_verify=self.connection.get('selfSignedCert', True),
                                    sni=self.connection.get('sni', None)
                                    )

    async def ping_box(self):
        """Ping the endpoint."""
        await self.init_async_client()
        resp = await self.client.call_api(self.endpoint, 'GET', timeout=self.timeout)
        await self.credential.close()
        return resp

    async def run_search(self, query_expression, start, stop, length):
        """get the response from azure_sentinel endpoints
        :param query_expression: str, search_id
        :param length: int,length value
        :return: response, json object"""
        await self.init_async_client()
        try:
            client = LogsQueryClient(self.credential)
            async with client:
                response = await client.query_workspace(
                    workspace_id=self.workspace_id,
                    query=query_expression,
                    timespan=(start, stop)
                )
            return {'success': True, "response": response}
        except HttpResponseError as er:
            return {'success': False, "error": er.error}
        except Exception as e:
            return {'success': False, "error": e}
        finally: 
            await self.credential.close()

    