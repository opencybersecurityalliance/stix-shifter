from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient
from stix_shifter_modules.db2.utils.data_transform import Transformer
import ibm_db
import json
import random
import datetime

class DB2Client():

    def __init__(self, connection, configuration):
        # connection and configuration are passed in the arguments for transmit
        # ex: python main.py transmit db2 '{"host":"localhost", "port":"6603"}' '{"auth": {"mysql_username": "admin","mysql_password": "admin", "mysql_hostname": "localhost", "mysql_database": "sampledb" } }' pin
        self.transformer = Transformer()
        self.auth = configuration.get('auth')
        try:
            self.client = ibm_db.pconnect(
                "DATABASE=" + self.auth.get("mysql_database") +
                ";HOSTNAME=" + connection.get("host", "") +
                ";PORT=" + connection.get("port", "31490") +
                ";UID=" + self.auth.get("mysql_username") +
                ";PWD=" + self.auth.get("mysql_password"),
                "", "")

            self.state = ibm_db.active(self.client)

        # handle exceptions later TODO
        except Exception as e:
            raise e

    def ping_data_source(self):
        # Pings the data source
        if self.state:
            return {"code": 200, "success": True}
        return {"code": 400, "success": False}

    def get_query(self, query):
        # expected output is: {'success': True, 'search_id': '<some query UUID>'}
        # For Synchronous calls query does not execute
        # code here is left as simple as possible so that async can be created later
        return_obj = {"code": 200 , "search_id": query}
        return return_obj

    def get_search_results(self, search_id, range_start=None, range_end=None):
        # Return the search results. Results must be in JSON format before being translated into STIX
        # search_id == query in native query language
        # this could be turned into its own function to build out the JSON TODO
        # later to be refactored to return error codes as well
        # search_id is the sql statement for synchronus
        sql = search_id
        stmt = ibm_db.exec_immediate(self.client, sql)
        results_list = []
        result = ibm_db.fetch_assoc(stmt)
        num_rows = 0
        while result is not False:
                num_rows += 1
                # Format datetime objects into strings
                self.transformer.main(result)
                results_list.append(result)
                result = ibm_db.fetch_assoc(stmt)

        return_obj = dict()
        return_obj["code"] = 200
        return_obj["data"] = results_list
        # look at stix_shifter/scripts/stix_shifter.py line 227 stix_shifter/scripts/stix_shifter.py
        # expects a dict with sucess and data keys. that object is constructed in
        # db2_results_connector.py
        # return obj:
        # {
        #     "code": 200,
        #     "data": [
        #         {
        #             row data 1
        #         },
        #         {
        #             row data 2 etc......
        #         }
        #     ]
        # }

        return return_obj

    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}
