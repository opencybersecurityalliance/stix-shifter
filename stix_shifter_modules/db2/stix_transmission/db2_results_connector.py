from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
# python main.py transmit mysql '{"host":"localhost", "port":"3306"}' '{"auth": {"mysql_username": "admin","mysql_password": "admin", "mysql_hostname": "localhost", "mysql_database": "sampledb", "mysql_table":"beeMovie"} }' results 3000 0 0

# a results call looks like This
# python main.py transmit mysql '{connection object}' '{authentication object}' results "search_id synch is nust query in native query language" <Offset Integer> <Length Integer>

class DB2ResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_results_connection(self, search_id, offset=None, length=None):
        try:
            # currently not implemented
            # will implement later TODO
            min_range = int(offset)
            max_range = min_range + int(length)

            response_dict = self.api_client.get_search_results(search_id, min_range, max_range)
            response_code = response_dict["code"]
            return_obj = dict()

            if response_code == 200:
                return_obj['success'] = True
                return_obj['data'] = response_dict['data']
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['message'])

            return return_obj


        except Exception as err:
            print('error when getting search results: {}'.format(err))
            import traceback
            print(traceback.print_stack())
            raise
