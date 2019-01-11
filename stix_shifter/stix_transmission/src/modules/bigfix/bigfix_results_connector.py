from ..base.base_results_connector import BaseResultsConnector
import json


class BigFixResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_results_connection(self, search_id, offset, length):
        try:
            response = self.api_client.get_search_results(search_id, offset, length)
            response_code = response.code
            return_obj = {}
            if 199 < response_code < 300:
                response_results = response.read()
                response_json = json.loads(response_results)
                return_obj['success'] = True
                return_obj['data'] = []
                for computer_obj in response_json['results']:
                    is_failure = computer_obj['isFailure']
                    if is_failure == False:
                        formatted_result_obj = self.format_computer_obj(computer_obj)
                        return_obj['data'].append(formatted_result_obj)
            else:
                return_obj['success'] = False
                return_obj['error'] = 'error when getting results'
            return json.dumps(return_obj)
        except Exception as err:
            return_obj = dict()
            return_obj['success'] = False
            return_obj['error'] = 'error when getting results: {}'.format(err)
            return return_obj
    
    @staticmethod
    def format_computer_obj(computer_obj):
        # {"computerID": 12369754, "computerName": "bigdata4545.canlab.ibm.com", "subQueryID": 1, "isFailure": false, "result": "file, .X0-lock, sha256, 7236f966f07259a1de3ee0d48a3ef0ee47c4a551af7f0d76dcabbbb9d6e00940, sha1, 8b5e953be1db90172af66631132f6f27dda402d2, md5, e5307d27f0eb9a27af8597a1ddc51e89, /tmp/.X0-lock, 1541424894", "ResponseTime": 0}

        result = computer_obj['result']
        obj_list = result.split(',')
        formatted_obj = {}

        formatted_obj['computerID'] = computer_obj['computerID']
        formatted_obj['computerName'] = computer_obj['computerName']
        formatted_obj['subQueryID'] = computer_obj['subQueryID']
        if result.startswith('process'):
            formatted_obj['start_time'] = obj_list[10].strip()
            formatted_obj['type'] = obj_list[0].strip()
            formatted_obj['process_name'] = obj_list[1].strip()
            formatted_obj['process_id'] = obj_list[2].strip()
            formatted_obj['sha256hash'] = obj_list[4].strip()
            formatted_obj['sha1hash'] = obj_list[6].strip()
            formatted_obj['md5hash'] = obj_list[8].strip()
            formatted_obj['file_path'] = obj_list[9].strip()
        elif result.startswith('file'):
            formatted_obj['type'] = obj_list[0].strip()
            formatted_obj['file_name'] = obj_list[1].strip()
            formatted_obj['sha256hash'] = obj_list[3].strip()
            formatted_obj['sha1hash'] = obj_list[5].strip()
            formatted_obj['md5hash'] = obj_list[7].strip()
            formatted_obj['file_path'] = obj_list[8].strip()
            formatted_obj['modified_time'] = obj_list[9].strip()
        else:
            print('Unknown result')

        return formatted_obj
