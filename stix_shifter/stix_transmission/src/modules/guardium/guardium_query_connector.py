from ..base.base_query_connector import BaseQueryConnector
import json
import uuid
import logging
import datetime
from .....utils.error_response import ErrorResponder
from .guardium_error_mapper import ErrorMapper


class GuardiumQueryConnector(BaseQueryConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_query_connection(self, query):
        # Construct a response object
        return_obj = dict()
        #
        queryResultSync = True
        # Grab the response, extract the response code, and convert it to readable json
        logging.info("------------ Guardium Query Connector - calling create search --------")
        # Verify the input
        try:
            jQry  = json.loads(query)
            reportName = jQry.get("reportName",True)
            if( reportName is True or jQry.get("reportParameter") is True):
                errMsg = "Report Name or Report Parameter is missing from the query statement." + str(query)
                logging.info(errMsg)
                ErrorResponder.fill_error(return_obj, message_struct=None, message_path=None, message=errMsg, error=2000)
        except:
            errMsg = "The query string is not in the proper format: " + str(query)
            logging.info(errMsg)
            ErrorResponder.fill_error(return_obj, message_struct=None, message_path=None, message=errMsg, error=2000)

        response = self.api_client.create_search(query)
        logging.info("------------ Guardium Query Connector - returned --------")
        #response_code = response.code()
        response_code = response.code
        response_dict = json.loads(response.read())
        logging.debug("Response Code: " + str(response_code) + "\nContent:")
        logging.debug(response.read())
        # Check if data is null -- did not return records

        if response_code == 200:
            return_obj['success'] = True
            return_obj['search_id'] = response_dict['search_id']
            return_obj['data'] = response_dict['data']

        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['ErrorMessage'])

        logging.info("-----Guardium Query Connector - done ----")
        return return_obj
