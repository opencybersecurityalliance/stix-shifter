from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
from azure.monitor.query.aio import LogsQueryClient
from azure.identity.aio import ClientSecretCredential
import logging


class APIClient:
    """API Client to handle all calls."""

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        self.connection = connection
        self.configuration = configuration
        logger = logging.getLogger("azure")
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
                                    cert_verify=self.connection.get('selfSignedCert')
                                    )

    async def ping_box(self):
        """Ping the endpoint."""
        try:
            await self.init_async_client()
            resp = await self.client.call_api(self.endpoint, 'GET', timeout=self.timeout)
            return resp
        except Exception as e:
            raise e
        finally:
            if hasattr(self, 'credential'):
                await self.credential.close()

    async def run_search(self, query_expression, start, stop):
        """get the response from log analytics endpoints
        :param query_expression: str, search_id
        :return: response, json object"""
        try:
            await self.init_async_client()
            client = LogsQueryClient(self.credential)
            async with client:
                response = await client.query_workspace(
                    workspace_id=self.workspace_id,
                    query=query_expression,
                    timespan=(start, stop)
                )
            return {'success': True, "response": response}
        except Exception as e:
            raise e
        finally:
            if hasattr(self, 'credential'):
                await self.credential.close()

