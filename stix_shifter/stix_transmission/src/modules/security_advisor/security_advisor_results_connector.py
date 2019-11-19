from ..base.base_results_connector import BaseResultsConnector
import json
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
        return_obj = {}
        try :
            if( isinstance(query , str) ):
                query = eval(query)
            
            list_or =[]
            list_and = []

            accountID = self.auth["accountID"]
            accessToken = self.auth["authToken"]
            set_occurences =  get_all_occurences(accountID, accessToken , self.host)

        except Exception as e :
            return_obj['success'] = False
            return_obj['error'] = str(Exception("Error in Getting all Occurences" + str(e)))
            return return_obj

        try :
            for elem in query :
                if( len(elem) ==1):
                    solved  = StixPatternParser().statement_parser.parser(elem[0])
                    findings = query_func(solved, set_occurences)
                    list_or.append(findings)
        
                else :
                    for finding in elem:
                        solved  = StixPatternParser().statement_parser.parser(finding)
                        findings = query_func(solved, set_occurences)
                        list_and.append(findings)

            combined_list = []

            for elem in list_and:
                list_occ_ids = []

                for sub_elem in elem:

                    if( len(sub_elem) == 1 ):
                        list_occ_ids.append(sub_elem[0]["id"])
                    
                combined_list.append(list_occ_ids)

            common_elements =[]
            if( combined_list != [] ):
                common_elements = list(set.intersection(*map(set, combined_list))) 

            data = []
            for elem in list_and:
                for sub_elem in elem:
                    if( len(sub_elem) == 1 ):

                        for element in common_elements:
                            if(element == sub_elem[0]["id"]):
                                data.append(sub_elem[0])
                            
            for elem_or in list_or:

                for sub_elem in elem_or:
                    for finding in sub_elem:
                        data.append(finding)
            
            if(len(data) == 0):
                return_obj['success'] = False
                return_obj['error'] = str(Exception("Query Failed!"))
            else:
                return_obj['success'] = True
                return_obj['data'] = data
            return return_obj

        except Exception as e :
            return_obj['success'] = False
            return_obj['error'] = str(Exception("Error in Evaluation" + str(e)))

        return return_obj