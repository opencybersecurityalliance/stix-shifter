import requests
from requests.models import Response
import json
import sys, argparse, traceback
import hashlib
import datetime, re
import base64
#from car_framework.context import context
#from car_framework.util import IncrementalImportNotPossible, RecoverableFailure, UnrecoverableFailure


class GuardUtil(object):

    def __init__ (self,client_id, url, secret, user, password):
        super().__init__()
    
        # now = get_report_time()
        # self.source = {'_key': context().source, 'name': context().args.server, 'description': 'Reference Guardium server'}
        # self.report = {'_key': str(now), 'timestamp' : now, 'type': 'Reference Guardium server', 'description': 'Reference Guardium server'}
        # self.source_report = [{'active': True, '_from': 'source/' + self.source['_key'], '_to': 'report/' + self.report['_key'], 'timestamp': self.report['timestamp']}]


        self.url = url
        self.secret = secret
        self.user = user
        self.password = password
        self.client_id=client_id
        self.token_target = '/oauth/token'
        self.report_target = '/restAPI/online_report'
        self.qs_target = '/restAPI/quick_search'
        
        self.get_token()

        # -------------------------------------------------------------------------------
        # REPORT parameters
        # -------------------------------------------------------------------------------
        # TBD dates
        #self.set_call_dates()
        #self.QUERY_FROM_DATE = "Now -60 DAY"
        #self.QUERY_TO_DATE = "Now"
        # -------------------------------------------------------------------------------
        # QS parameters
        # -------------------------------------------------------------------------------
        # TBD dates
        #self.qs_startTime = "20200616 10:00:00"
        #self.qs_endTime = "20200616 21:00:00"
    
    def set_call_dates(self):
        # look for last_run file - if file exist read last run date from it
        # if file does not exist or date older then x days set from dates to now -1 Day
        # otherwise set from date = last run date
        self.now = datetime.datetime.now()
        self.qs_endTime = self.now.strftime("%Y-%m-%d %H:%M:%S")
        self.QUERY_TO_DATE = self.now.strftime("%Y-%m-%d %H:%M:%S")
        from_file = None
        try:
            file = open("./last_run", "r")
            try:
                text = file.read()
                from_file = json.loads(text)
            finally:
                file.close() 
        except:
            pass

        
        if from_file and self.url in from_file:
                period_start = datetime.datetime.strptime(from_file[self.url],"%Y/%m/%d %H:%M:%S")
                if self.now - period_start > datetime.timedelta(days=2):
                    period_start = self.now - datetime.timedelta(days=1)
        else:
            period_start = self.now - datetime.timedelta(days=1) 
        self.from_file = from_file    
        self.QUERY_FROM_DATE = period_start.strftime("%Y-%m-%d %H:%M:%S")
        self.qs_startTime = period_start.strftime("%Y-%m-%d %H:%M:%S")

    def save_last_run_date(self):
        try:
            if self.from_file:
                output = self.from_file
                output[self.url] = self.now.strftime("%Y/%m/%d %H:%M:%S")
            else:
                output = {self.url : self.now.strftime("%Y/%m/%d %H:%M:%S")}
            file = open("./last_run", "w")
            file.write(json.dumps(output))
        finally:
            file.close()     

    def get_token(self):
        # -------------------------------------------------------------------------------
        # Authentication
        # -------------------------------------------------------------------------------
        #curl -k -X POST -d 'client_id=stix-shifter&grant_type=password&client_secret=2de4e437-73f1-445e-b6eb-a87c62a8e4cb&username=admin&password=!QAZ2wsx' https://hgai-srv05.haifa.ibm.com:8443/oauth/token
        #{"access_token":"619f4340-4f22-4ae0-9fda-9c5e0e8e8091","token_type":"bearer","expires_in":10799,"scope":"read write"}
        print("client_id="+self.client_id)
        #self.client_id="stix-shifter"
        print("secret="+self.secret)
        #self.secret="2de4e437-73f1-445e-b6eb-a87c62a8e4cb"
        print("user="+self.user)
        #self.user="admin"
        print("password="+self.password)
        #self.password="%21QAZ2wsx"
        self.token_data = 'client_id={0}&grant_type=password&client_secret={1}&username={2}&password={3}'.format(self.client_id,self.secret,self.user, self.password)
        #self.token_data = 'client_id=stix-shifter&grant_type=password&client_secret=2de4e437-73f1-445e-b6eb-a87c62a8e4cb&username=admin&password=!QAZ2wsx'
        #try:
        response = requests.post(self.url+self.token_target, params=self.token_data,verify=False)
        #except Exception as e:
              #e = sys.exc_info()[0]
              #context().logger.exception(e)
              #raise RecoverableFailure("token request faild {0}".format(e.args))
        if self.validate_response(response, "token ", True):
            self.access_token = response.json()['access_token']
            print("token="+ self.access_token)
            self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {0}'.format(self.access_token)}
    
    def validate_response(self, p_response, prefix, abort=False):
        if p_response.status_code != 200:
            #context().logger.error(prefix+"request faild "+str(p_response.status_code)+"-"+p_response.reason) 
            #context().logger.error(p_response.content)
            if abort :
                raise Exception(prefix+"request faild "+str(p_response.status_code)+"-"+p_response.reason)
            return False
        return True    
    
    def create_search(self, query_expression):
        respObj = Response()
        respObj.code = "401"
        respObj.error_type = ""
        respObj.status_code = 401
        print("query="+query_expression)
        if (self.access_token):
            self.query = query_expression
            response = self.build_searchId()
            if (response != None):
                respObj.code = "200"
                respObj.error_type = ""
                respObj.status_code = 200
                content = '{"search_id": "' + \
                    str(response) + \
                    '", "data": {"message":  "Search id generated."}}'
                respObj._content = bytes(content, 'utf-8')
            else:
                respObj.code = "404"
                respObj.error_type = "Not found"
                respObj.status_code = 404
                respObj.message = "Could not generate search id."
        else:
            respObj.error_type = "Unauthorized: Access token could not be generated."
            respObj.message = "Unauthorized: Access token could not be generated."
#
        return ResponseWrapper(respObj)
        
    def build_searchId(self):
        #       It should be called only ONCE when transmit query is called
        # Structure of the search id is
        # '{"query": ' + json.dumps(self.query) + ', "credential" : ' + json.dumps(self.credential) + '}'
        s_id = None
#
        if(self.query is None):
            raise IOError(3001, 
            "Could not generate search id because 'query' or 'authorization token' or 'credential info' is not available.")
#
        else:
            id_str = '{"query": ' + json.dumps(self.query) + ', "target" : "' + self.url + '", "user":"'+self.user+'"}'
            #print(id_str)
            id_byt = id_str.encode('utf-8')
            s_id = base64.b64encode(id_byt).decode()
            self.search_id=s_id
#
        print(s_id)
        return s_id

    def handle_report(self, report_name, params, index_from, fetch_size):
        # -------------------------------------------------------------------------------
        # REPORT
        # -------------------------------------------------------------------------------
        results = ""
        #context().logger.debug('-------------------  ' + report_name + ' ----------------------')
        params_set = {"reportName":"{0}".format(report_name), "indexFrom": "{0}".format(index_from), "fetchSize": "{0}".format(fetch_size), "reportParameter":params}
        json_dump = json.dumps(params_set)
        rest_data = str(json.loads(json_dump))

        response = requests.post(self.url+self.report_target, data=rest_data,headers=self.headers,verify=False)
        if self.validate_response(response, report_name):
            print(response.json())
            # print("TEXT")
            # print(response.text)
            
            results=response.json()
            
            check_list = isinstance(results, list)
        
            if check_list == False:
                try:
                    errorCode = results["ErrorCode"]
                    errorMsg = results["ErrorMessage"]
                except Exception as e:
                    try:
                        errorCode = results["ID"]
                        errorMsg = results["Message"]
                    except Exception as e:
                        errorCode = "1"
                        errorMsg = "Unknow exception"
                        #context().logger.exception(e)
                results = ""
               # context().logger.error("ERROR:" + str(errorCode) + "  " + errorMsg)
        return results

    def handle_qs(self, category, params, filters, index_from, fetch_size):
        # -------------------------------------------------------------------------------
        # QS
        # -------------------------------------------------------------------------------
        # print("filters:" +filters)
        results = ""
        params_set = {"category":"{0}".format(category), "startTime": "{0}".format(self.qs_startTime), "endTime": "{0}".format(self.qs_endTime), \
             "fetchSize": "{0}".format(fetch_size), "firstPosition": "{0}".format(index_from)}
        if filters:
            params_set["filters"] = "{0}".format(filters)

        all_params = {**params_set, **params}
        json_dump = json.dumps(all_params)
        rest_data = str(json.loads(json_dump))
        
        # print(rest_data)

        response = requests.post(self.url+self.qs_target, data=rest_data,headers=self.headers,verify=False)
        if self.validate_response(response, "QS -"+category):
            # print(response.json())
            # print("TEXT")
            # print(response.text)
            
            results=response.json()
            check_list = isinstance(results, list)
        
            if check_list == False:
                try:
                    errorCode = results["ErrorCode"]
                    errorMsg = results["ErrorMessage"]
                except Exception as e:
                    try:
                        errorCode = results["ID"]
                        errorMsg = results["Message"]
                    except Exception as e:
                        #context().logger.exception(e)
                        raise e
               #context().logger.error("ERROR:" + str(errorCode) + "  " + errorMsg)
                results = ""
        return results       

'''
    def get_hash(self, keys, values):
        hash_val = hashlib.sha1()
        #concat_str = ""
        if values and keys:
           keys1 =list(keys)
           keys1.sort()
           for key in keys1 : 
               hash_val.update(str(values[key]).encode('utf-8'))

        context().logger.debug("----------------------")               
        context().logger.debug(hash_val.hexdigest())               
        context().logger.debug("----------------------")               
        return hash_val.hexdigest()
'''
class ResponseWrapper:
    def __init__(self, response):
        self.response = response

    def read(self):
        return self.response.content

    @property
    def bytes(self):
        return self.response.content

    @property
    def code(self):
        return self.response.status_code

