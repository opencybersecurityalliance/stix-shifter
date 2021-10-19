from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient
from stix_shifter_utils.utils.error_response import ErrorResponder
from .error_mapper import ErrorMapper
import requests
import requests.auth
import json
import base64

class APIClient():

    def __init__(self, connection, configuration):
        self.base_url = "https://{}".format(connection['host'])
        self.headers = dict()
        self.auth = configuration["auth"]
        self.client = RestApiClient(connection['host'])
        self.search_query = ""
        self.headers["Content-Type"] = "application/json"
        self.report_limit = configuration['report_limit']
        self.max_number_pages = configuration['max_number_pages']

    def ping_data_source(self):
        # Pings the data source
        response = self.get_token()
        if response['code'] == 200:
            self.token = json.loads(response['data'])['access_token']
        else:
            return response
        
        self.headers["Authorization"] = "Bearer {}".format(self.token)

        ping_result = self.ping_trustar() 
        return ping_result 

    def get_search_results(self, search_id, range_start=None, range_end=None):
        # Return the search results. Results must be in JSON format before being translated into STIX
        try:
            resp = self._get_results(search_id, range_start, range_end)
            response = {'success':True, 'code': 200, 'data': resp}
        except Exception as e:
            response = {'success':False, 'code': 2000, 'data': []}
        return response

    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}
    
    def _check_searchTerm(self, searchTerm):
        return len(searchTerm) <= 3 and searchTerm != ""

    def _get_results(self, search_id, range_start, range_end):

        response = []
        resp = self.get_token()

        if resp['code'] == 200:
            self.token = json.loads(resp['data'])['access_token']
        else:
            return response

        self.headers["Authorization"] = "Bearer {}".format(self.token)

        # If query has report id, search for report -> delete report id -> preform other calls
        # if values are present
        json_query = json.loads(search_id)

        if "reportId" in json_query:
            response.append(self.get_report_details(json_query['reportId']))
            del json_query['reportId']
        if "reportIds" in json_query:
            response += self.get_all_reports(json_query['reportIds'])
            del json_query['reportIds']
        if "searchTerm" in json_query or "tags" in json_query or "excludeTags" in json_query or "entityTypes" in json_query:
            if "searchTerm" in json_query and (json_query['searchTerm'] is "" or json_query['searchTerm'] is "*"):
                del json_query['searchTerm']
                
            query = json.dumps(json_query)

            response += self.search_indicators(query, range_start, range_end)
            response += self.search_reports(query)
        
        return response


    def get_token(self):

        response = ""
        data = {'grant_type':'client_credentials'}
        creds = self.auth['clientId'] + ":" + self.auth['clientSecret']
        en_auth = base64.b64encode(creds.encode())

        headers = dict()
        headers['Authorization'] = "Basic %s" % en_auth.decode()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        
        response = self.client.call_api("oauth/token", 'POST', headers=headers, data=data)
        resp = self._handle_errors(response)
        
        return resp

#     def search_indicators(self, query, range_start, range_end):
#
#         indicatorMeta = []
#         indicatorSummaries = list()
# # Subroto added - modified
#         maxPSize = 1000
#         thisPageNumber = 0
#         json_query = json.loads(query)
#         # json_query.update({"pageSize": 1000})
#         query = json.dumps(json_query)
#         urlData = {"pageSize": maxPSize, "pageNumber": thisPageNumber}
#         #endpoint = "api/1.3/indicators/search" + "?" + "pageSize=" + \
#         #    str(maxPSize) + "&pageNumber=" + str(thisPageNumber)
#
#         print("urlData -- Search indicator")
#         print(urlData)
#         #print(endpoint)
#
#         resp = self.client.call_api("api/1.3/indicators/search", "POST", headers=self.headers, urldata=urlData, data=query)
#         #resp = self.client.call_api(endpoint, "POST", headers=self.headers, data=query)
#
#         response = self._handle_errors(resp, query)
#
#         if response['code'] != 200:
#             return response
#
#         response_data = json.loads(response['data'])
#
#         print("Number of Indicators: " + str(len(response_data['items'])))
#         #print(json.dumps(response_data, indent=2))
#
#         for item in response_data['items']:
#             #Create new response field ["indicatorType"] : response['value']
#             indicatorType = item['indicatorType']
#             indicatorValue = item['value']
#             item[indicatorType] = indicatorValue
#             indicatorMeta.append({"value": indicatorValue})
#             indicatorSummaries.append(indicatorValue)
#
#         summaries = self.get_indicator_summaries(indicatorSummaries)
#         metadata = self.get_indicator_metadata(indicatorMeta)
#         merged_data = response_data['items']
#
#         merged_data = self.merge(metadata, summaries, response_data['items'])
#         print("Returning - merged_data")
#         return merged_data

    def get_indicator_summaries(self, searchIds):

        # Subroto added - modified
        maxPSize = 100
        thisPageNumber = 0
        urlData = {"pageSize": maxPSize, "pageNumber": thisPageNumber}

        str_data = json.dumps(searchIds)
        resp = self.client.call_api("api/1.3/indicators/summaries", "POST", headers=self.headers, urldata=urlData, data=str_data)
        response = self._handle_errors(resp)

        if response['code'] != 200:
            return response
        elif response['data'] is None:
            return response

        summaries = json.loads(response['data'])['items']
        print("Exiting get Indicator Summaries")
        return summaries

    def get_indicator_metadata(self, data):

        str_data = json.dumps(data)
        resp = self.client.call_api("api/1.3/indicators/metadata", "POST", headers=self.headers, data=str_data)
        response = self._handle_errors(resp)

        if response['code'] != 200:
            return response

        metadata = json.loads(response['data'])
        print("Exiting get Indicator Metadata")
        return metadata
        
    def get_all_reports(self, reportIds):

        # check if ids  1 < ids < 400 
        # List structure "id, id2, id3, id4, ...."
        response = []
        try:
            ids = reportIds.split(',')
        except Exception as e:
            #ErrorResponder.fill_error(response,m,error=e)
            return response
        ##print(len(ids))
        if len(ids) > self.report_limit or len(ids) < 2:
            ErrorResponder.fill_error(response,message="More than 1 and less than {} report ids required".format(self.report_limit), error="More than 1 and less than {} report ids required".format(self.report_limit))
        
        for id in ids:
            id = id.strip()
            response.append(self.get_report_details(id))

        return response
            

    def get_report_details(self, reportId):
        
        response = {}

        resp = self.client.call_api("api/1.3/reports/{}".format(reportId),"GET", headers=self.headers)
        response = self._handle_errors(resp)

        if response['code'] != 200:
            return response

        response_data = json.loads(response['data'])
        response['report'] = response_data
        
        response['report']['tags'] = self.get_report_tags(reportId)
        response['report']['indicators'] = self.get_report_indicators(reportId)

        return response

    def search_reports(self, query):
        # Subroto added - modified
        maxPSize = 100
         # Add max page size
        json_query = json.loads(query)
        # json_query.update({"pageSize": 100})
        query = json.dumps(json_query)
            # Collated items
        all_items = []
        print("in search_reports: Max Number of Pages set to " + str(self.max_number_pages))
        for thisPageNumber in range(self.max_number_pages):
            urlData = {"pageSize": maxPSize, "pageNumber": thisPageNumber}
            From = json_query["from"]
            To = json_query["to"]
            urlData = {"pageSize": maxPSize, "pageNumber": thisPageNumber, "from": From, "to": To}
                # endpoint = "api/1.3/reports/search" + "?" + "pageSize=" + \
                # str(maxPSize) + "&pageNumber=" + str(thisPageNumber)
                # print(endpoint)
            resp = self.client.call_api("api/1.3/reports/search", "POST", headers=self.headers, urldata=urlData,
                                            data=query)
                # resp = self.client.call_api(endpoint, "POST", headers=self.headers, data=query)
            response = self._handle_errors(resp, query)

            if response['code'] != 200:
                return response

            response_data = json.loads(response['data'])
            if "hasNext" in response_data:
                if response_data["hasNext"]:
                    all_items.extend(response_data['items'])
                else:
                    if "empty" in response_data:
                        if not response_data["empty"]:
                            all_items.extend(response_data['items'])
                            response_data['items'] = all_items
                    break
            else:
                break

        if len(response_data['items']) < self.report_limit:
            for report in response_data['items']:
                report['tags'] = self.get_report_tags(report['id'])
                report['indicators'] = self.get_report_indicators(report['id'])

        return response_data['items']

    def search_indicators(self, query, range_start, range_end):

        indicatorMeta = []
        indicatorSummaries = list()
        # Subroto added - modified
        maxPSize = 1000
        thisPageNumber = 0
        json_query = json.loads(query)
        # json_query.update({"pageSize": 1000})
        query = json.dumps(json_query)
        From = json_query["from"]
        To = json_query["to"]
        urlData = {"pageSize": maxPSize, "pageNumber": thisPageNumber, "from": From, "to": To}
            # urlData = {"pageSize": maxPSize, "pageNumber": thisPageNumber}
            # endpoint = "api/1.3/indicators/search" + "?" + "pageSize=" + \
            #    str(maxPSize) + "&pageNumber=" + str(thisPageNumber)

        print("urlData -- Search indicator")
        print(urlData)
        # print(endpoint)

        resp = self.client.call_api("api/1.3/indicators/search", "POST", headers=self.headers, urldata=urlData,
                                        data=query)
        # resp = self.client.call_api(endpoint, "POST", headers=self.headers, data=query)

        response = self._handle_errors(resp, query)

        if response['code'] != 200:
            return response

        response_data = json.loads(response['data'])

        print("Number of Indicators: " + str(len(response_data['items'])))
            # print(json.dumps(response_data, indent=2))

        for item in response_data['items']:
                # Create new response field ["indicatorType"] : response['value']
            indicatorType = item['indicatorType']
            indicatorValue = item['value']
            item[indicatorType] = indicatorValue
            indicatorMeta.append({"value": indicatorValue})
            indicatorSummaries.append(indicatorValue)

        summaries = self.get_indicator_summaries(indicatorSummaries)
        metadata = self.get_indicator_metadata(indicatorMeta)
        merged_data = response_data['items']

        merged_data = self.merge(metadata, summaries, response_data['items'])
        print("Returning - merged_data")
        return merged_data

    #     def search_reports(self, query):
# # Subroto added - modified
#         maxPSize = 100
#         # Add max page size
#         json_query = json.loads(query)
# # json_query.update({"pageSize": 100})
#         query = json.dumps(json_query)
# # Collated items
#         all_items = []
#         print("in search_reports: Max Number of Pages set to " + str(self.max_number_pages))
# #
#         for thisPageNumber in range( self.max_number_pages ):
#             urlData = { "pageSize": maxPSize, "pageNumber": thisPageNumber}
#             #endpoint = "api/1.3/reports/search" + "?" + "pageSize=" + \
#             #str(maxPSize) + "&pageNumber=" + str(thisPageNumber)
#             #print(endpoint)
#             resp = self.client.call_api("api/1.3/reports/search", "POST", headers=self.headers, urldata=urlData, data=query)
#             #resp = self.client.call_api(endpoint, "POST", headers=self.headers, data=query)
#             response = self._handle_errors(resp, query)
#
#             if response['code'] != 200:
#                 return response
#
#             response_data = json.loads(response['data'])
#             if "hasNext" in response_data:
#                 if response_data["hasNext"]:
#                     all_items.extend( response_data['items'])
#                 else:
#                     if "empty" in response_data:
#                         if not response_data["empty"]:
#                             all_items.extend(response_data['items'])
#                             response_data['items'] = all_items
#                     break
#             else:
#                 break
#
#         if len(response_data['items']) < self.report_limit:
#             for report in response_data['items']:
#                 report['tags'] = self.get_report_tags(report['id'])
#                 report['indicators'] = self.get_report_indicators(report['id'])
#
#         return response_data['items']

    def get_report_indicators(self, reportId):

# Subroto 
        # Subroto added - modified
        maxPSize = 1000
        thisPageNumber = 0
        urlData = {"pageSize": maxPSize, "pageNumber": thisPageNumber}
        
        resp = self.client.call_api("api/1.3/reports/{}/indicators".format(reportId), "GET", headers=self.headers, urldata=urlData)
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
    
    def ping_trustar(self):

        resp = dict()
        response = self.client.call_api("api/1.3/ping","GET", headers=self.headers)
        resp = self._handle_errors(response)
        return resp
    
    def merge(self, meta, summaries, base):

#Subroto changed
        summary_dict = dict()
        meta_dict = dict()
        return_obj = base

        try:

            for item in meta:
                data = { 'meta' : item }
                meta_dict[item['guid']] = data

            print("In Merge: meta dictionary done")
            for item in summaries:
                guid = "{}|{}".format(item['type'],item['value'])
                data = { 'indicatorSummary': item }
                summary_dict[guid] = data

            print("In Merge: summary dictionary done")
            for item in return_obj:

                if 'guid' in item:
                    base_guid = item['guid']
                    print("processing guid: " + base_guid)
                else:
                    print("Guid issue - none found")
                    print(json.dumps(item, indent=2))
                    continue

# Subroto changed
                if summaries and base_guid in summary_dict:
            
                    print("indicator summary " + base_guid + " Inserted.")
                    item['indicatorSummary'] = summary_dict[base_guid]['indicatorSummary'] if 'indicatorSummary' in summary_dict[base_guid] else []
                else:
                    print("indicator summary " + base_guid +  " Not found in summary_dict")
                if meta and base_guid in meta_dict:
                    if 'meta' in meta_dict[base_guid]:
                        item['meta'] = meta_dict[base_guid]['meta']
                        print("meta " + base_guid + " Inserted.")
                else:
                    print("meta " + base_guid + " Not found in meta_dict")
                    
                    #item['meta'] = meta_dict[base_guid]['meta'] if 'meta' in meta_dict[base_guid] else []
                print(json.dumps(item, indent=2))

        except Exception as e:
            print(e)
            return_obj['error'] = e

        print("Return merge function")
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
            ErrorResponder.fill_error(return_obj, message=return_obj['data'], error="Authentication Failure")
        elif response.code == 404:
            return_obj['code'] = 404
            return_obj['success'] = False
            return_obj['data'] = "Error Querying Data Source.  Search Query: {}".format(query)
            ErrorResponder.fill_error(return_obj, message=return_obj['data'],error="Bad Request - Invalid Query {}".format(query))
        else:
            return_obj['code'] == 2000
            return_obj['data'] == "Unknown Error"
            ErrorResponder.fill_error(return_obj, message=return_obj['data'], error="Unknown Error")
        
        return return_obj
