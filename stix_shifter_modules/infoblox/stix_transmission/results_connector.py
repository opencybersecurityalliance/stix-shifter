from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.error_response import ErrorResponder


class ResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    def create_results_connection(self, search_id, offset, length):
        print("**************************** search_id")
        print(search_id)
        try:
            offset_i = int(offset)
            len_i = int(length)
            min_range = offset_i
            # TODO: evaluate this 1000 threshold, is it needed?

            if len_i > 1000:
                self.logger.warning("The length exceeds length limit. Use default length: 1000")
            max_range = offset_i + len_i if len_i <= 1000 else offset_i + 1000
            # Grab the response, extract the response code, and convert it to readable json
            response_dict = self.api_client.get_search_results(search_id, min_range, max_range)
            response_code = response_dict["code"]

            # # Construct a response object
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
                return_obj['data'] = response_dict['data']['logs']
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['message'])

            print("000000000000000000000000000000000000000000000000000000000000")
            print(return_obj)
            # return_obj['data'] = [{
            #     'status': 'success',
            #     'job_id': '0854de82-21ce-4e42-ae10-af5b21cec7c2',
            #     'job': {
            #         'id': '0854de82-21ce-4e42-ae10-af5b21cec7c2',
            #         'state': 'completed', 'status': 'success', 'create_ts': 1627550085198,
            #         'create_time': '2021-06-29T09:14:45.198Z', 'request_ttl': 0, 'result_ttl': 3600,
            #         'completed_tasks': ['2be44b3e-0ee0-4784-9d7a-cbb670101bea'], 'org': 'BLOXINT00000000264',
            #         'user': 'user.service.03283b68-bceb-49c6-b706-2a4ec650067f@infoblox.invalid', 'tasks_tbc': 0
            #     },
            #     'tasks': {'2be44b3e-0ee0-4784-9d7a-cbb670101bea': {
            #         'id': '2be44b3e-0ee0-4784-9d7a-cbb670101bea', 'state': 'completed', 'status': 'success',
            #         'create_ts': 1627550085198, 'create_time': '2021-07-29T09:14:45.198Z',
            #         'start_ts': 1627550086228, 'start_time': '2021-07-29T09:14:46.228Z',
            #         'end_ts': 1627550086502, 'end_time': '2021-07-29T09:14:46.502Z',
            #         'params': {'type': 'host', 'target': 'vm2052798.11ssd.had.wf', 'source': 'pdns'}, 'options': {}, 'results': None,
            #         'rl': False
            #     }},
            #     'results': [{
            #         'task_id': '2be44b3e-0ee0-4784-9d7a-cbb670101bea',
            #         'params': {'type': 'host', 'target': 'vm2052798.11ssd.had.wf', 'source': 'pdns'},
            #         'status': 'success',
            #         'time': 274, 'v': '3.0.0',
            #         'data': {
            #             'duration': 274393539,
            #             'items': [{
            #                 'Domain': '', 'Hostname': 'vm1941851.11ssd.had.wf', 'IP': '185.244.216.186',
            #                 'Last_Seen': 1627547780, 'NameServer': '', 'Record_Type': 'A'
            #             }],
            #             'status': 200,
            #             'total_results': 1
            #         }
            #     }]
            # }]
            return return_obj
        except Exception as err:
            self.logger.error('error when getting search results: %s', err, exc_info=True)
            raise
