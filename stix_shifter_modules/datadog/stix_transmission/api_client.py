from datadog_api_client.v1 import ApiClient, ApiException, Configuration
from datadog_api_client.v1.api import events_api, authentication_api


class APIClient:

    def __init__(self, connection, configuration):
        auth = configuration.get('auth')
        self.configuration = Configuration(host=connection["site_url"])
        self.configuration.api_key["apiKeyAuth"] = auth["api_key"]
        self.configuration.api_key["appKeyAuth"] = auth["application_key"]

    def ping_data_source(self):
        # Enter a context with an instance of the API client
        return_obj = {"code": 200}
        with ApiClient(self.configuration) as api_client:
            # Create an instance of the API class
            api_instance = authentication_api.AuthenticationApi(api_client)
            try:
                # Validate API key
                api_instance.validate()
            except ApiException as e:
                return_obj.update({"code": e.status, "message": e.reason})
        return return_obj

    def get_search_results(self, search_id, page=None):
        return_obj = {"code": 200}
        if page:
            search_id.update({"exclude_aggregate": True, "page": page})
        with ApiClient(self.configuration) as api_client:
            api_instance = events_api.EventsApi(api_client)
            try:
                api_response = api_instance.list_events(**search_id)
                return_obj.update({"data": api_response})
            except ApiException as e:
                return_obj.update({"code": e.status, "message": e.reason})
        return return_obj

