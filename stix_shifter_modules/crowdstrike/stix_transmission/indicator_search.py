import requests
import json
from requests.auth import HTTPBasicAuth

USERNAME = 'Z091VW22DJF53YA5TUIY'
PASSWORD = 'szZJKJGTHRndmOZbRpUcoRObeP8X5r'
URL = 'https://falconapi.crowdstrike.com/threatgraph/combined/ran-on/v1'

params = {'value': '643ec58e82e0272c97c2a59f6020970d881af19c0ad5029db9c958c13b6558c7',
          'type': 'sha256',
          'limit': '4'}


def run_indicator_search_request():
    try:
        response = requests.get(URL, auth=HTTPBasicAuth(USERNAME, PASSWORD), params=params)
        response_code = response.status_code
        response_dict = json.loads(response.text)
        return_obj = dict()

        if 200 <= response_code < 300:
            return_obj['success'] = True
            return_obj['meta'] = response_dict['meta']
            return_obj['resources'] = response_dict['resources']
            return return_obj
        else:
            raise requests.exceptions.RequestException(f'response code: {response_code}')

    except requests.exceptions.RequestException as e:
        print('Error. Reason: {}'.format(e))


def get_path_values():
    paths = list()
    return_obj = run_indicator_search_request()
    resources = return_obj['resources']
    for resource in resources:
        paths.append(resource['path'])
    return paths


def run_vertex_summary_request(url_lst):
    results = dict()
    results['data'] = list()

    for url in url_lst:
        try:
            response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
            response_code = response.status_code
            response_dict = json.loads(response.text)
            return_obj = dict()

            if 200 <= response_code < 300:
                return_obj['success'] = True
                return_obj['meta'] = response_dict['meta']
                return_obj['data'] = response_dict['resources']
                for obj in return_obj['data']:
                    results['data'].append(obj)

            else:
                raise requests.exceptions.RequestException(f'response code: {response_code}')

        except requests.exceptions.RequestException as e:
            print('Error. Reason: {}'.format(e))
            continue

    return results


if __name__ == '__main__':
    paths = get_path_values()
    results = run_vertex_summary_request(paths)
    print(results)
