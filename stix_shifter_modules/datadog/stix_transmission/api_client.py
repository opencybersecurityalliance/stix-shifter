import json
import os
from datadog_api_client.v1 import ApiClient, ApiException, Configuration
from datadog_api_client.v1.api import events_api, authentication_api
from datadog_api_client.v1.models import *


class APIClient:

    def __init__(self, connection, configuration):
        auth = configuration.get('auth')
        os.environ["DD_SITE"] = connection["host"]
        os.environ["DD_API_KEY"] = auth["api_key"]
        os.environ["DD_APP_KEY"] = auth["app_key"]
        self.configuration = Configuration()

    def ping_data_source(self):
        # Enter a context with an instance of the API client
        with ApiClient(self.configuration) as api_client:
            # Create an instance of the API class
            api_instance = authentication_api.AuthenticationApi(api_client)
            # Validate API key
            api_response = api_instance.validate()
        return api_response

    def get_search_results(self, search_id, range_start=None, range_end=None):
        search_id = json.loads(search_id)
        with ApiClient(self.configuration) as api_client:
            api_instance = events_api.EventsApi(api_client)
            api_response = api_instance.list_events(start=search_id.get("start"), end=search_id.get("end"))
        return api_response

    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}
