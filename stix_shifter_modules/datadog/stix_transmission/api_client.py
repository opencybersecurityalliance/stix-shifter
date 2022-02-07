import time
import datadog_api_client.v1 
import datadog_api_client.v1.api 
from datadog_api_client.v1.api import events_api
from datadog_api_client.v2.api import processes_api
from urllib3.exceptions import MaxRetryError
import urllib3

class APIClient:

    def __init__(self, connection, configuration):
        self.connection = connection
        self.auth = configuration.get('auth')
        self.configuration = datadog_api_client.v1.Configuration(host=connection["site_url"])
        self.configuration.api_key["apiKeyAuth"] = self.auth["api_key"]
        self.configuration.api_key["appKeyAuth"] = self.auth["application_key"]
        if "selfSignedCert" in connection:
            self.configuration.ssl_ca_cert = connection["selfSignedCert"]
        else:
            self.configuration.verify_ssl = False
        urllib3.disable_warnings()

    def ping_data_source(self):
        """To Validate API key"""
        # Enter a context with an instance of the API client
        return_obj = {"code": 200}
        with datadog_api_client.v1.ApiClient(self.configuration) as api_client:
            # Create an instance of the API class
            api_instance = events_api.EventsApi(api_client)
            current_time = int(time.time())
            try:
                # There is no any specific Datadog endpoint which validate application key
                api_instance.list_events(start=current_time, end=current_time)
            except MaxRetryError as e:
                e.status = 1004
                return_obj.update({"code": e.status, "message": e.reason})
            except datadog_api_client.v1.ApiException as e:
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
        with datadog_api_client.v1.ApiClient(self.configuration) as api_client:
            api_instance = events_api.EventsApi(api_client)
            try:
                api_response = api_instance.list_events(**search_id)
                return_obj.update({"data": api_response})
            except datadog_api_client.v1.ApiException as e:
                return_obj.update({"code": e.status, "message": e.reason})
        return return_obj

    def get_processes_results(self):
        return_obj = {"code": 200}
        configuration = datadog_api_client.v2.Configuration(host=self.connection["site_url"])
        configuration.api_key["apiKeyAuth"] = self.auth["api_key"]
        configuration.api_key["appKeyAuth"] = self.auth["application_key"]
        if "selfSignedCert" in self.connection:
            configuration.ssl_ca_cert = self.connection["selfSignedCert"]
        else:
            configuration.verify_ssl = False
        with datadog_api_client.v2.ApiClient(configuration) as api_client:
            api_instance = processes_api.ProcessesApi(api_client)
            try:
                api_response = api_instance.list_processes()
                return_obj.update({"data": api_response})
            except datadog_api_client.v2.ApiException as e:
                return_obj.update({"code": e.status, "message": e.reason})
        return return_obj
