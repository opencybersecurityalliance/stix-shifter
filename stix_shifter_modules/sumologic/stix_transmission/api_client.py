import time
import json
from sumologic import SumoLogic


class APIClient:

    def __init__(self, connection, configuration):
        self.endpoint = "https://api.%s.sumologic.com/api" % (connection.get("region"))
        self.auth = configuration.get('auth')
        self.client = SumoLogic(self.auth.get("username"), self.auth.get("password"), endpoint=self.endpoint)

    def ping_data_source(self):
        # Pings the data source
        self.client.collectors()
        return {"code": 200, "success": True}

    def create_search(self, query_expression):
        # Queries the data source
        query_expression = json.loads(query_expression)
        search_job = self.client.search_job(query_expression['query'], query_expression['fromTime'],
                                            query_expression['toTime'])
        return {"code": 200, "query_id": search_job['id']}

    def get_search_status(self, search_id):
        # Check the current status of the search
        search_id = {"id": search_id}
        status = self.client.search_job_status(search_id)
        while status['state'] != 'DONE GATHERING RESULTS':
            if status['state'] == 'CANCELLED':
                break
            time.sleep(5)
            status = self.client.search_job_status(search_id)
        return {"code": 200, "status": status['state']}

    def get_search_results(self, search_id, offset, limit):
        # Return the search results. Results must be in JSON format before being translated into STIX
        status = self.get_search_status(search_id)
        if status['status'] == "DONE GATHERING RESULTS":
            search_id = {"id": search_id}
            result = self.client.search_job_messages(search_id, limit, offset)
        else:
            search_id = {"id": search_id}
            result = self.client.search_job_messages(search_id, limit, offset)

        results = [r['map'] for r in result['messages']]
        return {"code": 200, "data": results}

    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        # TODO: Test delete
        search_id = {"id": search_id}
        self.client.delete_search_job(search_id)
        return {"code": 200, "success": True}
