import json
from sumologic import SumoLogic


PROTOCOL = "https://"
URL = "api.%s.sumologic.com/"
ENDPOINT = "api"


class SumoLogicResponse:
    def __init__(self, response_code, response_object):
        self.code = response_code
        self.object = response_object


class APIClient:
    def __init__(self, connection, configuration):
        self.endpoint = (PROTOCOL + URL + ENDPOINT) % (connection.get("region"))
        self.auth = configuration.get('auth')
        self.client = SumoLogic(self.auth.get("access_id"), self.auth.get("access_key"), endpoint=self.endpoint)

    def ping_data_source(self):
        # Pings the data source
        self.client.collectors()
        return SumoLogicResponse(200, True)

    def create_search(self, query_expression):
        # Queries the data source
        query_expression = json.loads(query_expression)
        search_job = self.client.search_job(query_expression['query'], query_expression['fromTime'],
                                            query_expression['toTime'])
        return SumoLogicResponse(200, search_job['id'])

    def get_search_status(self, search_id):
        # Check the current status of the search
        search_id = {"id": search_id}
        status = self.client.search_job_status(search_id)
        return SumoLogicResponse(200, status['state'])

    def get_search_results(self, search_id, offset, limit):
        # Return the search results. Results must be in JSON format before being translated into STIX
        search_id = {"id": search_id}
        result = self.client.search_job_messages(search_id, limit, offset)

        response = (self.client.get("/users"))
        user_details = response.json()["data"][0]

        results = [r['map'] for r in result['messages']]
        for r in results:
            r.update(user_details)
            r["displayName"] = user_details["firstName"] + " " + user_details["lastName"]

        return SumoLogicResponse(200, results)

    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        search_id = {"id": search_id}
        x = self.client.delete_search_job(search_id)
        return SumoLogicResponse(200, x.json())
