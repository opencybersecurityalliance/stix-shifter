from ..base.base_results_connector import BaseResultsConnector
import json
import requests


from .utils.sa_occurence_finder import query_func
from .utils.sa_findings_api import get_all_occurences
from .utils.StixPatternParser import StixPatternParser

class SecurityAdvisorResultsConnector(BaseResultsConnector):
    def __init__(self, host, auth ):
        self.host = host
        self.auth = auth
        self.StixPatternParser = StixPatternParser()

    def create_results_connection(self, searchID , offset , length):

        query = json.loads(searchID)
        ret_obj = {}
        try :
            if( isinstance(query , str) ):
                query = eval(query)
            
            list_or =[]
            list_and = []

            accountID = self.auth["accountID"]
            accessToken = self.auth["authToken"]

            set_occ =  get_all_occurences(  accountID, accessToken , self.host)

        except Exception as e :
            ret_obj['success'] = False
            ret_obj['error'] = "Error in Getting all Occurences" + str(e)
            return ret_obj

        try :

            for elem in query :

                if( len(elem) ==1  ):
                    solved  = StixPatternParser().statement_parser.parser(elem[0])
                    output = query_func(solved , set_occ )
                    list_or.append(output)
        
                else :

                    for finding in elem:
                        solved  = StixPatternParser().statement_parser.parser(finding)

                        output = query_func(solved, set_occ)
                        list_and.append(output)

            big_list = []

            for elem in list_and:
                list_occ_ids = []

                for sub_elem in elem:

                    if( len(sub_elem) == 1 ):
                        list_occ_ids.append(sub_elem[0]["id"])
                    
                big_list.append(list_occ_ids)

            res =[]
            if( big_list != [] ):
                res = list(set.intersection(*map(set, big_list))) 

            l = []

            for elem in list_and:
                for sub_elem in elem:
                    if( len(sub_elem) == 1 ):

                        for resp in res:
                            if( resp == sub_elem[0]["id"] ):
                                l.append(sub_elem[0])
                            
            for elem_or in list_or:

                for sub_elem in elem_or:
                    for finding in sub_elem:
                        l.append(finding)

            
            ret_obj = {}
            if( len(l) == 0 ):
                ret_obj['success'] = False
                ret_obj['error'] = str(Exception("Query Failed!"))
            else:
                ret_obj['success'] = True
                ret_obj['data'] = l
            return ret_obj

        except Exception as e :
            ret_obj['success'] = False
            ret_obj['error'] = "Error in Evaluation" + str(e)

        return ret_obj