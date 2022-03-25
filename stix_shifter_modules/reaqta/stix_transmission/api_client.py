from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient
import requests

class APIClient():
    AUTH_ENDPOINT = "/rqt-api/1/authenticate"
    EVENT_ENDPOINT = "/rqt-api/1/events/hunt"

    def __init__(self, connection, configuration):
        headers = dict()
        url_modifier_function = None
        auth = configuration.get('auth')
        self.host = connection.get('host')
        self.client = RestApiClient(connection.get('host'),
                                    connection.get('port', None),
                                    headers,
                                    url_modifier_function=url_modifier_function,
                                    cert_verify=connection.get('selfSignedCert', True),
                                    sni=connection.get('sni', None)
                                    )
        self.timeout = connection['options'].get('timeout')
        self.app_id = auth['app_id']
        self.secret_key = auth['secret_key']

    def ping_data_source(self):
        # Pings the data source
        auth_host = 'https://' + self.host + self.AUTH_ENDPOINT
        auth_data = {'id' : self.app_id, 'secret' : self.secret_key}
        return requests.post(auth_host, data=auth_data)
        # return self.client.call_api(auth_host, 'POST', data=auth_data, timeout=self.timeout)

    def get_search_results(self, search_id, range_start=None, range_end=None):
        # Return the search results. Results must be in JSON format before being translated into STIX
        return {"code": 200, "data": "Results from search"}

    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}
