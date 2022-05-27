from distutils.log import debug
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
        self.token= self.credential.get_token("https://{host}/.default".format(host=self.host))
        headers["Authorization"] =  'Bearer {token}'.format(token=self.token[0])
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
        workspace_id= connection.get('workspaceId')
        self.endpoint = 'v1/workspaces/{workspace_id}/query'.format(workspace_id=workspace_id)

    
    def ping_box(self):
        """Ping the endpoint."""
        return self.client.call_api(self.endpoint, 'GET',  timeout=self.timeout)
    
    def run_search(self, query_expression, length):
        """get the response from azure_sentinel endpoints
        :param query_expression: str, search_id
        :param length: int,length value
        :return: response, json object"""
        headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6ImpTMVhvMU9XRGpfNTJ2YndHTmd2UU8yVnpNYyIsImtpZCI6ImpTMVhvMU9XRGpfNTJ2YndHTmd2UU8yVnpNYyJ9.eyJhdWQiOiJodHRwczovL2FwaS5sb2dhbmFseXRpY3MuaW8iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC85MjRmOGExMi1mNmJkLTRiOGQtOTNiZi05ZmE2ZTI2Y2JmOGIvIiwiaWF0IjoxNjUzNjUyNzg2LCJuYmYiOjE2NTM2NTI3ODYsImV4cCI6MTY1MzY1NjY4NiwiYWlvIjoiRTJaZ1lNZ3hNSlJjTk45UXBtVFAxczdMOGxOTUFBPT0iLCJhcHBpZCI6IjE1NTY2YmMxLTAwOTgtNGU3OS04MGExLTYzOTBiOTc0NDBlZSIsImFwcGlkYWNyIjoiMSIsImlkcCI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzkyNGY4YTEyLWY2YmQtNGI4ZC05M2JmLTlmYTZlMjZjYmY4Yi8iLCJvaWQiOiJiN2NiYmFiNS1mZmExLTQ0NWEtYWJkZS0xYWM4OGVlMGYwYTUiLCJyaCI6IjAuQVZVQUVvcFBrcjMyalV1VHY1LW00bXlfaXdzX2Y4cVJmU3hJamduRjJFRFE2c1dJQUFBLiIsInJvbGVzIjpbIkRhdGEuUmVhZCJdLCJzdWIiOiJiN2NiYmFiNS1mZmExLTQ0NWEtYWJkZS0xYWM4OGVlMGYwYTUiLCJ0aWQiOiI5MjRmOGExMi1mNmJkLTRiOGQtOTNiZi05ZmE2ZTI2Y2JmOGIiLCJ1dGkiOiJRbGlnVE5iLVJrcWJLcG12aFNCUEFBIiwidmVyIjoiMS4wIn0.d6HVy3OQsHA2Y5wYAONaXr_YqrTSgQ_RmYmdJpAjjPhxnSO6wLsKvG2zDT_Qt9mKK1Jh1K6Nxp9pMRrqF2L00cwNMpwhPREybGnPMD0x1d1VzOnE_Yd61Cp_8EHvLQ8Gy8k8ZiHTDSUHEwFy2b9X9VAhzvCBOMUJbgiTozxLdcaw4Jp7geqXcKNG-ywRoTSwnvpKnal5APrWPU_22z02-l9UkAtJ7HbdXa9N4iYCEH_OVEFkqVv9zqHarpvwY4HbROPehrKCM58sW7b8RqfZjJI46dhNGZGefIi10yfTIarM7YL8LM5-OeI6rr5qe352pXuLnM1YVr6W7u7u2wbGIQ'
}
        payload = json.dumps({"query":query_expression})
        print(payload)
        return self.client.call_api(self.endpoint, 'GET', headers, data=payload)