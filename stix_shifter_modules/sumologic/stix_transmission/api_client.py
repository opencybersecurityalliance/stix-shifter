from datetime import datetime,timedelta
import time
from sumologic import SumoLogic


class APIClient():

    def __init__(self, connection, configuration):
        self.endpoint = "https://api.%s.sumologic.com/api" % (connection.get("region"))
        self.auth = configuration.get('auth')
        self.client = SumoLogic(self.auth.get("username"), self.auth.get("password"), endpoint=self.endpoint)
        self.search_job = None

    def ping_data_source(self):
        # Pings the data source
        self.client.collectors()
        return {"code": 200, "success": True}

    def create_search(self, query_expression):
        # Queries the data source
        toTime = datetime.utcnow()
        fromTime = (toTime- timedelta(minutes=15))
        # self.search_job = self.client.search_job(query_expression, fromTime, toTime, timeZone, byReceiptTime)
        self.search_job = self.client.search_job(query_expression,fromTime.strftime("%Y%m%dT%H%M%S"),
                                                 toTime.strftime("%Y%m%dT%H%M%S"))
        return {"code": 200, "query_id": self.search_job['id']}

    def get_search_status(self, search_id):
        # Check the current status of the search
        print(search_id)
        status = self.client.search_job_status(self.search_job)
        while status['state'] != 'DONE GATHERING RESULTS':
            if status['state'] == 'CANCELLED':
                break
            time.sleep(5)
            status = self.client.search_job_status(self.search_job)
        return {"code": 200, "status": status['state']}

    def get_search_results(self, search_id, range_start=None, range_end=None):
        # Return the search results. Results must be in JSON format before being translated into STIX
        return {"code": 200, "data": "Results from search"}

    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        self.client.delete_search_job(self.search_job)
        return {"code": 200, "success": True}
