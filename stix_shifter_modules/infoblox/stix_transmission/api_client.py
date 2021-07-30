import datetime
import json

from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient
from stix_shifter_utils.utils import logger

_USER_AGENT = 'IBV1StixShifter/1.0'


class APIClient:

    def __init__(self, connection, configuration):
        self.logger = logger.set_logger(__name__)
        self.endpoint_start = ''
        headers = dict()
        host_port = connection.get('host') + ':' + str(connection.get('port', ''))
        headers['accept'] = 'application/json'
        auth = configuration.get('auth')
        if auth is not None and auth.get('token', None) is not None:
            headers['Authorization'] = 'token {}'.format(auth.get('token'))
        url_modifier_function = None
        headers['user-agent'] = _USER_AGENT

        self.timeout = connection['options'].get('timeout')

        self.client = RestApiClient(host_port,
                                    None,
                                    headers,
                                    url_modifier_function,
                                    cert_verify=connection.get('selfSignedCert', True),
                                    sni=connection.get('sni', None)
                                    )

    def ping_data_source(self):
        # Pings the data source
        endpoint = 'tide/api/data/threats/state?type=host&rlimit=1'
        # now = datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z"
        # https://csp.infoblox.com:443/tide/api/data/threats/state?type=host&rlimit=1
        # https://csp.infoblox.com    /tide/api/data/threats/state?type=host&rlimit=1

        resp = self.client.call_api(endpoint, 'GET', timeout=self.timeout, urldata={"type": "host", "rlimit": "1"})
        return {"code": resp.code}

    def get_search_results(self, search_id, range_start=None, range_end=None):
        # Return the search results. Results must be in JSON format before being translated into STIX
        # endpoint = self.endpoint_start + '/api/dnsdata/v2/dns_event'

        payload = json.loads(search_id)
        print("--------------------------------------------- serach payload")
        print(payload)
        if payload['source'] == 'dnsEventData':
            return self._get_dnseventdata_results(search_id, range_start, range_end)
        elif payload['source'] == 'dossierData':
            return self._get_dossierdata_results(search_id, range_start, range_end)
        elif payload['source'] == 'tideDbData':
            return self._get_tidedbdata_results(search_id, range_start, range_end)
        resp_dict = dict()
        resp_dict["code"] = 200
        resp_dict['data'] = dict()
        resp_dict['data']['logs'] = []


        print(resp_dict)
        print("pppppppppppppppppppppppppppppppppppppppppppp")

        return resp_dict

    def _get_dnseventdata_results(self, search_id, range_start=None, range_end=None):
        endpoint = 'api/dnsdata/v2/dns_event'
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        payload = json.loads(search_id)
        resp_dict = dict()
        all_data = list()
        resp_dict["data"] = {"logs": all_data}
        start = range_start if range_start else 0
        end = range_end if range_end else 0
        offset = start
        max_fetch_count = 10
        for i in range(0, max_fetch_count):
            payload["offset"] = 0
            resp = self.client.call_api(endpoint + "?" + payload["query"], 'GET', headers=headers, timeout=self.timeout)
            payload_dict = json.loads(resp.read())

            code = resp.code
            response = payload_dict

            # code, response = self._fetch(endpoint, headers, payload, offset)
            resp_dict["code"] = code
            if code != 200:
                # TODO test this
                resp_dict["message"] = response["status_detail"]
                break
            else:
                all_data += [response["result"][0]]
                break
        if resp_dict.get("code") == 200:
            self.logger.debug("The log count is %s", len(resp_dict["data"]["logs"]))
        return resp_dict

    def _get_dossierdata_results(self, search_id, range_start=None, range_end=None):
        # ip?value=45.14.13.25&wait=true&source=pdns
        # TODO: async
        endpoint = 'tide/api/services/intel/lookup/indicator'
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        payload = json.loads(search_id)
        resp_dict = dict()
        all_data = list()
        resp_dict["data"] = {"logs": all_data}
        start = range_start if range_start else 0
        end = range_end if range_end else 0
        offset = start
        max_fetch_count = 10

        params = {
            'wait': 'true',
            'source': 'pdns'
        }
        for i in range(0, max_fetch_count):
            payload["offset"] = 0
            resp = self.client.call_api(endpoint + "?" + payload["query"], 'GET', urldata=params, headers=headers, timeout=self.timeout)
            payload_dict = json.loads(resp.read())

            code = resp.code
            response = payload_dict

            # code, response = self._fetch(endpoint, headers, payload, offset)
            resp_dict["code"] = code
            if code != 200:
                # TODO test this
                resp_dict["message"] = response["status_detail"]
                break
            else:
                print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
                print(response)
                all_data += [response]
                break
        if resp_dict.get("code") == 200:
            # TODO: check this
            self.logger.debug("The log count is %s", len(resp_dict["data"]["logs"]))
        return resp_dict

    def _get_tidedbdata_results(self, search_id, range_start=None, range_end=None):
        endpoint = 'tide/api/data/threats/state'
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        payload = json.loads(search_id)
        resp_dict = dict()
        all_data = list()
        resp_dict["data"] = {"logs": all_data}
        start = range_start if range_start else 0
        end = range_end if range_end else 0
        offset = start
        max_fetch_count = 10
        for i in range(0, max_fetch_count):
            payload["offset"] = 0

            #TODO remove hard-coded 'type'
            #type must be one of type must be one of (host, ip, url, hash, email)
            resp = self.client.call_api(endpoint + "/ip?" + payload["query"], 'GET', headers=headers, timeout=self.timeout)
            response_string = resp.read()
            payload_dict = json.loads(resp.read())

            code = resp.code
            response = payload_dict

            # code, response = self._fetch(endpoint, headers, payload, offset)
            resp_dict["code"] = code
            if code != 200:
                # TODO test this
                resp_dict["message"] = response["status_detail"]
                break
            else:
                all_data += response["threat"]
                break
        if resp_dict.get("code") == 200:
            self.logger.debug("The log count is %s", len(resp_dict["data"]["logs"]))
        return resp_dict


    # def _fetch(self, endpoint, headers, payload, offset):
    #     payload["offset"] = offset
    #     resp = self.client.call_api(endpoint + "?" + payload["query"], 'GET', headers=headers, timeout=self.timeout)
    #     payload_dict = json.loads(resp.read())
    #     return resp.code, payload_dict
