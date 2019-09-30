from ..utils.RestApiClient import RestApiClient
from cortex4py.api import Api
import json

class APIClient():

    def __init__(self, connection, configuration):
        self.all_data_tlp = configuration.get('all_data_tlp')
        if self.all_data_tlp is None:
            self.all_data_tlp = 0

        cortex_instance = connection.get('host')+':'+connection.get('port')
        auth = configuration.get('auth')
        http_proxy = configuration.get('http_proxy')
        https_proxy = configuration.get('https_proxy')
        verify_cert = configuration.get('verify_cert')
        proxies = {}
        if http_proxy:
            proxies['http'] = http_proxy
        if https_proxy:
            proxies['https'] = https_proxy

        self.client = Api(cortex_instance, auth, proxies=proxies, verify_cert=verify_cert)

    def ping_data_source(self):
        # Pings the data source
        try:
            analyzers = self.client.analyzers.find_all({}, range='all')
        except:
            return {'success': False}
        return {'success': True}

    def create_search(self, query_expression):
        jobs = []
        queries = json.loads(query_expression)
        for q in queries:
            item = q.popitem()
            data_type = item[0]
            data = item[1]
            analyzers = self.client.analyzers.get_by_type(data_type)
            for analyzer in analyzers:
                job = self.client.analyzers.run_by_name(analyzer.name, {
                            'data': data,
                            'dataType': data_type,
                            'tlp': self.all_data_tlp
                        })
                jobs.append(job)

        return {
            "code": 200,
            "search_id": [job.id for job in jobs]
        }

    def _get_job_ids(self, search_id):
        job_ids = search_id.replace('[','').replace(']','')
        job_ids = job_ids.replace("'","")
        job_ids = job_ids.split(',')
        job_ids = (j.strip() for j in job_ids)
        return job_ids


    def get_search_status(self, search_id):
        for job_id in self._get_job_ids(search_id):
            job = self.client.jobs.get_by_id(job_id)
            if job.status != "Success":
                return {"code": 200, "search_id": search_id, "status": job.status}

        return {"code": 200, "search_id": search_id, "status": "COMPLETED"}

    def get_search_results(self, search_id, range_start=None, range_end=None):
        result = {"code": 200, "search_id": search_id}
        artifacts = []
        for job_id in self._get_job_ids(search_id):
            analyzer_name = self.client.jobs.get_by_id(job_id).analyzerName
            artifact = {"cortex_analyzer": analyzer_name}
            for a in self.client.jobs.get_artifacts(job_id):
                artifact[a.dataType] = a.data
            if artifact:
                artifacts.append(artifact)
        
        result["data"] = artifacts
        return result

    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return "Deleted query: {}".format(search_id)
