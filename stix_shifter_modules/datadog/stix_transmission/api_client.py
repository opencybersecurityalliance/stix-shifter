import time
from datadog_api_client.v1 import ApiClient, ApiException, Configuration
from datadog_api_client.v1.api import events_api
from datadog_api_client.v2 import ApiClient, ApiException, Configuration
from datadog_api_client.v2.api import processes_api

class APIClient:

    def __init__(self, connection, configuration):
        auth = configuration.get('auth')
        self.configuration = Configuration(host=connection["site_url"])
        self.configuration.api_key["apiKeyAuth"] = auth["api_key"]
        self.configuration.api_key["appKeyAuth"] = auth["application_key"]

    def ping_data_source(self):
        """To Validate API key"""
        # Enter a context with an instance of the API client
        return_obj = {"code": 200}
        with ApiClient(self.configuration) as api_client:
            # Create an instance of the API class
            api_instance = events_api.EventsApi(api_client)
            current_time = int(time.time())
            try:
                # There is no any specific Datadog endpoint which validate application key
                api_instance.list_events(start=current_time, end=current_time)
            except ApiException as e:
                return_obj.update({"code": e.status, "message": e.reason})
        return return_obj

    def get_search_results(self, search_id, page=None):
        """get the response from Datadog endpoints
        :param search_id: dict, filter parameters
        :param page: int,length value
        :return: response, json object"""
        return_obj = {"code": 200}
        if page:
            search_id.update({"exclude_aggregate": True, "page": page})
        if "source" in search_id:
            search_id["sources"] = search_id.pop("source")
        with ApiClient(self.configuration) as api_client:
            api_instance = events_api.EventsApi(api_client)
            try:
                api_response = api_instance.list_events(**search_id)
                return_obj.update({"data": api_response})
            except ApiException as e:
                return_obj.update({"code": e.status, "message": e.reason})
        return return_obj

    def get_processes_results(self):
        return_obj = {"code": 200}
        with APIClient(self.configuration) as api_client:
            api_instance = processes_api.ProcessesApi(api_client)
            try:
                api_response = api_instance.list_processes()
                return_obj.update({"data": api_response})
            except ApiException as e:
                return_obj.update({"code": e.status, "message": e.reason})
        return return_obj