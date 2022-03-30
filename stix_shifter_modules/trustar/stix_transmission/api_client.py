from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient
from stix_shifter_utils.utils.error_response import ErrorResponder
# from .error_mapper import ErrorMapper
# import requests
# import requests.auth
import json
import base64
from stix_shifter_utils.utils import logger


class APIClient():

    def __init__(self, connection, configuration):
        self.base_url = "https://{}".format(connection['host'])
        self.headers = dict()
        self.auth = configuration["auth"]
        self.client = RestApiClient(connection['host'])
        self.search_query = ""
        self.headers["Content-Type"] = "application/json"
        self.report_limit = connection['report_limit']
        self.max_number_pages = connection['max_number_pages']
        self.results_code = 200
        self.success = True
        self.generate_token = self.get_token()

    def ping_data_source(self):
        # Pings the data source
        response = self.get_token()
        return response
        # if response['code'] == 200:
        #     self.token = json.loads(response['data'])['access_token']
        # else:
        #     return response
        #
        # self.headers["Authorization"] = "Bearer {}".format(self.token)
        #
        # ping_result = self.ping_trustar()
        # return ping_result

    def get_search_results(self, search_id, range_start=None, range_end=None):
        # Return the search results. Results must be in JSON format before being translated into STIX
        response = {}
        try:
            # query = json.loads(search_id)
            # if 'valid' in query and query['valid'] is False:
            #    response = { "success": False, "code": 2000, "data": []}
            #    ErrorResponder.fill_error(response, message="Query Not Supported")
            # else:
            response = self._get_results(search_id, range_start, range_end)
        except Exception as e:
            logger.error("Error while converting query", e)
        return response

    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}

    def _check_searchTerm(self, searchTerm):
        return len(searchTerm) <= 3 and searchTerm != ""

    def _get_results(self, search_id, range_start, range_end):

        response = dict()
        response_data = []
        resp = self.get_token()

        if resp['code'] == 200:
            self.token = json.loads(resp['data'])['access_token']
        else:
            return response

        self.headers["Authorization"] = "Bearer {}".format(self.token)
        try:
            json_query = json.loads(search_id)
            if json_query.get('searchTerm') == ' ':
                json_query['searchTerm'] = ''
        except ValueError as e:
            return "Invalid query parameters"

        if "reportId" in json_query:
            response_data.append(self.get_report_details(json_query['reportId']))
            del json_query['reportId']
        if "reportIds" in json_query:
            response_data.extend(self.get_all_reports(json_query['reportIds']))
            del json_query['reportIds']
        if "searchTerm" in json_query or "tags" in json_query or "excludeTags" in json_query or "entityTypes" in json_query or "title" in json_query\
                or "indicator" in json_query:
            if "searchTerm" in json_query and (json_query['searchTerm'] is "" or json_query['searchTerm'] is "*"):
                del json_query['searchTerm']

            query = json.dumps(json_query)

            response_data.extend(self.search_indicators(query, range_start, range_end))
            response_data.extend(self.search_reports(query))

        response['code'] = self.results_code
        response['success'] = self.success
        response['data'] = response_data

        return response

    def get_token(self):

        response = ""
        data = {'grant_type': 'client_credentials'}
        creds = self.auth['clientId'] + ":" + self.auth['clientSecret']
        en_auth = base64.b64encode(creds.encode())

        headers = dict()
        headers['Authorization'] = "Basic %s" % en_auth.decode()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        response = self.client.call_api("oauth/token", 'POST', headers=headers, data=data)
        resp = self._handle_errors(response)

        return resp

    def search_indicators(self, query, range_start, range_end):
        indicatorMeta = []
        indicatorSummaries = []
        data = {}

        maxPSize = 1000
        endpoint = "api/1.3/indicators/search"
        json_query = json.loads(query)

        if "searchTerm" in json_query:
            data.update({"searchTerm": json_query.pop('searchTerm')})
            data = json.dumps(data)

        response = self.get_all_pages(endpoint, query, maxPSize)

        if len(response["items"]) == 0:
            return response["items"]

        summaries = []
        metadata = []

        for item in response["items"]:
            # Create new response field [“indicatorType”] : response[‘value’]
            indicatorType = item["indicatorType"]
            indicatorValue = item["value"]
            item[indicatorType] = indicatorValue
            # Ignore duplicate entries
            if indicatorValue not in indicatorSummaries:
                indicatorSummaries.append(indicatorValue)
                indicatorMeta.append({"value": indicatorValue})
            # Max list size to datasource is 100, every 100 entries -> get metadata/summeries, reset metadata/summaries array ids
            if len(indicatorSummaries) % 100 == 0:
                summaries.extend(self.get_indicator_summaries(indicatorSummaries))
                metadata.extend(self.get_indicator_metadata(indicatorMeta))
                indicatorSummaries = []
                indicatorMeta = []

        # Make sure any left over entries left in summaries/metadata list are searched
        if len(indicatorSummaries) > 0:
            summaries.extend(self.get_indicator_summaries(indicatorSummaries))
            metadata.extend(self.get_indicator_metadata(indicatorMeta))

        merged_data = response["items"]
        merged_data = self.merge(metadata, summaries, response["items"])

        return merged_data

    def get_indicator_summaries(self, searchIds):

        # Subroto added - modified
        maxPSize = 100
        thisPageNumber = 0
        endpoint = "api/1.3/indicators/summaries"
        urlData = {"pageSize": maxPSize, "pageNumber": thisPageNumber}

        str_data = json.dumps(searchIds)
        resp = self.client.call_api(endpoint, "POST", headers=self.headers, urldata=urlData, data=str_data)
        response = self._handle_errors(resp)

        if response['code'] != 200:
            return response

        summaries = json.loads(response['data'])['items']
        return summaries

    def get_indicator_metadata(self, data):

        str_data = json.dumps(data)
        resp = self.client.call_api("api/1.3/indicators/metadata", "POST", headers=self.headers, data=str_data)
        response = self._handle_errors(resp)

        if response['code'] != 200:
            return response

        metadata = json.loads(response['data'])
        return metadata

    def search_reports(self, query):
        # Subroto added - modified
        maxPSize = 100
        endpoint = "api/1.3/reports/search"

        response = self.get_all_pages(endpoint, query, maxPSize)

        if len(response["items"]) == 0:
            return response["items"]

        if len(response['items']) < self.report_limit:
            for report in response['items']:
                report['tags'] = self.get_report_tags(report['id'])
                report['indicators'] = self.get_report_indicators(report['id'])

        return response['items']

    def get_all_reports(self, reportIds):
        # check if ids  1 < ids < report_limit
        # List structure "id, id2, id3, id4, ...."
        response = []
        try:
            ids = reportIds.split(',')
        except Exception as e:
            return response
        if len(ids) > self.report_limit or len(ids) < 2:
            ErrorResponder.fill_error(response, message="More than 1 and less than {} report ids required".format(
                self.report_limit), error="More than 1 and less than {} report ids required".format(self.report_limit))

        for id in ids:
            id = id.strip()
            response.append(self.get_report_details(id))

        return response

    def get_report_details(self, reportId):

        response = {}

        resp = self.client.call_api("api/1.3/reports/{}".format(reportId), "GET", headers=self.headers)
        response = self._handle_errors(resp)

        if response['code'] != 200:
            return response

        response_data = json.loads(response['data'])
        response['report'] = response_data

        response['report']['tags'] = self.get_report_tags(reportId)
        response['report']['indicators'] = self.get_report_indicators(reportId)

        return response

    def get_report_indicators(self, reportId):

        maxPSize = 1000
        thisPageNumber = 0
        urlData = {"pageSize": maxPSize, "pageNumber": thisPageNumber}

        resp = self.client.call_api("api/1.3/reports/{}/indicators".format(reportId), "GET", headers=self.headers,
                                    urldata=urlData)
        response = self._handle_errors(resp)

        if response['code'] != 200:
            return response

        response_data = json.loads(response['data'])['items']

        return response_data

    def get_report_tags(self, reportId):

        resp = self.client.call_api("api/1.3/reports/{}/tags".format(reportId), "GET", headers=self.headers)
        response = self._handle_errors(resp)

        if response['code'] != 200:
            return response

        response_data = json.loads(response['data'])

        return response_data

    # Request all data by looping over trustar api response pages
    def get_all_pages(self, endpoint, query, maxPSize, data={}):

        all_items = []
        json_query = json.loads(query)

        From = json_query["from"] if "from" in json_query else ""
        To = json_query["to"] if "to" in json_query else ""

        if "searchTerm" in json_query:
            data.update({"searchTerm": json_query.pop('searchTerm')})
            query = json.dumps(json_query)
            data = json.dumps(data)

        for thisPageNumber in range(self.max_number_pages):

            urlData = {"pageSize": maxPSize, "pageNumber": thisPageNumber, "from": From, "to": To}

            resp = self.client.call_api(endpoint, "POST", headers=self.headers, urldata=urlData, data=data)
            response = self._handle_errors(resp, query)

            if response['code'] != 200:
                return response

            response_data = json.loads(response['data'])
            all_items.extend(response_data['items'])

            if "hasNext" in response_data:
                if response_data["hasNext"] == False:
                    break

        response_data['items'] = all_items

        return response_data

    def ping_trustar(self):

        resp = dict()
        response = self.client.call_api("api/1.3/ping", "GET", headers=self.headers)
        resp = self._handle_errors(response)

        return resp

    # Merge base Indicator object with each indicators metadata and summaries if provided
    def merge(self, meta, summaries, base):

        summary_dict = dict()
        meta_dict = dict()
        return_obj = base

        # Test for empty metadata/summaries
        if meta is [] and summaries is []:
            return base

        try:

            for item in meta:
                data = {'meta': item}
                meta_dict[item['guid']] = data

            for item in summaries:
                guid = "{}|{}".format(item['type'], item['value'])
                data = {'indicatorSummary': item}
                summary_dict[guid] = data

            for item in return_obj:

                if 'guid' in item:
                    base_guid = item['guid']
                else:
                    continue

                # Subroto changed
                if summaries and base_guid in summary_dict:
                    item['indicatorSummary'] = summary_dict[base_guid]['indicatorSummary'] if 'indicatorSummary' in \
                                                                                              summary_dict[
                                                                                                  base_guid] else []
                if meta and base_guid in meta_dict:
                    if 'meta' in meta_dict[base_guid]:
                        item['meta'] = meta_dict[base_guid]['meta']
        except Exception as e:
            return_obj['error'] = e

        return return_obj

    # Returns the following object:  {'code': 200, 'data': 'SOME STRING' }
    def _handle_errors(self, response, query=None):
        return_obj = dict()
        response_txt = response.read().decode('utf-8')
        if response.code == 200:
            return_obj['code'] = 200
            return_obj['success'] = True
            return_obj['data'] = response_txt
        elif response.code == 401:
            return_obj['code'] = 401
            return_obj['success'] = False
            return_obj['data'] = "Authentication Failed"
            # ErrorResponder.fill_error(return_obj, message=return_obj['data'], error="Authentication Failure")
        elif response.code == 404:
            return_obj['code'] = 404
            return_obj['success'] = False
            return_obj['data'] = "Error Querying Data Source.  Search Query: {}".format(query)
            ErrorResponder.fill_error(return_obj, message=return_obj['data'],
                                      error="Bad Request - Invalid Query {}".format(query))
        elif response.code == 400:
            return_obj['code'] = 400
            return_obj['success'] = False
            return_obj['data'] = "Error Querying Data Source.  Search Query: {}".format(query)
            ErrorResponder.fill_error(return_obj, message=return_obj['data'], error="Bad Request")
        elif response.code == 429:
            return_obj['code'] = 429
            return_obj['success'] = False
            return_obj['data'] = "Request Limit Exceeded, contact Trustar Administrator "
            ErrorResponder.fill_error(return_obj, message=return_obj['data'], error="Request Limit Exceeded")
        else:
            return_obj['code'] == 2000
            return_obj['success'] = False
            return_obj['data'] == "Unknown Error"
            ErrorResponder.fill_error(return_obj, message=return_obj['data'], error="Unknown Error")

        self.results_code = return_obj['code']
        self.success = return_obj['success']

        return return_obj
