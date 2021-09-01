import json

from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient
from stix_shifter_utils.utils import logger

_USER_AGENT = 'IBV1StixShifter/1.0'
_MAX_RESULT = 10000

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
        self.result_limit = connection['options'].get('result_limit')
        if self.result_limit > _MAX_RESULT:
            self.logger.warning("The length exceeds length limit. Use default length: %s", _MAX_RESULT)
            self.result_limit = _MAX_RESULT

        self.client = RestApiClient(host_port,
                                    None,
                                    headers,
                                    url_modifier_function,
                                    cert_verify=connection.get('selfSignedCert', True),
                                    sni=connection.get('sni', None)
                                    )

    def ping_data_source(self):
        # Pings the data source
        endpoint = 'tide/api/data/threats/state'
        # now = datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z"
        # https://csp.infoblox.com:443/tide/api/data/threats/state?type=host&rlimit=1

        return self.client.call_api(endpoint, 'GET', timeout=self.timeout, urldata={"type": "host", "rlimit": "1"})

    def get_search_results(self, search_id, range_start=None, range_end=None):
        # Return the search results. Results must be in JSON format before being translated into STIX
        # endpoint = self.endpoint_start + '/api/dnsdata/v2/dns_event'

        payload = json.loads(search_id)
        if payload['source'] == 'dnsEventData':
            return self._get_dnseventdata_results(search_id, range_start, range_end)
        elif payload['source'] == 'dossierData':
            return self._get_dossierdata_results(search_id, range_start, range_end)
        elif payload['source'] == 'tideDbData':
            return self._get_tidedbdata_results(search_id, range_start, range_end)

        # default behavior
        raise RuntimeError("Unknown source provided source={}".format(payload['source']))

    def _get_dnseventdata_results(self, search_id, range_start=None, range_end=None):
        endpoint = 'api/dnsdata/v2/dns_event'
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        payload = json.loads(search_id)
        resp_dict = dict()
        resp_dict["data"] = []

        start = range_start if range_start else 0
        end = range_end if range_end else 0
        offset = start
        max_fetch_count = 10
        for fetch_iteration in range(0, max_fetch_count):
            params = {"_limit": self.result_limit,"_offset": offset}
            resp = self.client.call_api(endpoint + "?" + payload["query"], 'GET', urldata=params, headers=headers, timeout=self.timeout)
            resp_dict["code"] = resp.code
            if resp.code != 200:
                if resp.code == 401:
                    resp_dict["message"] = resp.read().decode("utf-8")
                else:
                    response_payload = json.loads(resp.read())
                    resp_dict["message"] = "\n".join([error["message"] for error in response_payload["error"]])

                del resp_dict["data"]
                return resp_dict

            # successful request, append data to collection and recalculate offset
            response_payload = json.loads(resp.read())
            if "result" not in response_payload or len(response_payload["result"]) == 0:
                self.logger.debug("No additional results found")
                break

            offset += len(response_payload["result"])
            for event in response_payload["result"]:
                resp_dict["data"].append({"dnsEventData": event})

            if len(resp_dict["data"]) > end - start:
                resp_dict["data"] = resp_dict["data"][0:end - start]
                break

            if fetch_iteration == max_fetch_count - 1:
                self.logger.warning("Reach max fetch count %s, stop loop", max_fetch_count)
                break

        if resp_dict.get("code") == 200:
            self.logger.debug("The DNS Event count is %s", len(resp_dict["data"]))

        return resp_dict

    def _get_dossierdata_results(self, search_id, range_start=0, range_end=None):
        endpoint = 'tide/api/services/intel/lookup/indicator'
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        payload = json.loads(search_id)
        resp_dict = dict()
        resp_dict["data"] = []
        start = range_start if range_start else 0
        end = range_end if range_end else 0

        params = {'wait': 'true','source': 'pdns'}

        # NOTE: Dossier does not support pagination via multiple requests. All results returned in the response.
        resp = self.client.call_api(endpoint + "/" + payload["threat_type"] + "?" + payload["query"], 'GET', urldata=params, headers=headers, timeout=self.timeout)
        resp_dict["code"] = resp.code
        if resp.code != 200:
            if resp.code == 401:
                resp_dict["message"] = resp.read().decode("utf-8")
            else:
                response_payload = json.loads(resp.read())
                resp_dict["message"] = response_payload["error"]
            del resp_dict["data"]
            return resp_dict

        response_payload = json.loads(resp.read())
        for i in response_payload["results"]:
            for j in i["data"]["items"]:
                restructure_payload = {'job': {'create_time': response_payload['job']['create_time']},'results': [{'data': {'items': [j]}}]}
                resp_dict["data"].append({"dossierData": restructure_payload})

        # Trim result set based on min/max range values
        end = end if end < len(resp_dict["data"]) else len(resp_dict["data"])
        num_results = end - start

        if len(resp_dict["data"]) > end - start:
            resp_dict["data"] = resp_dict["data"][start:end]

        if resp_dict.get("code") == 200:
            self.logger.debug("The Dossier count is %s", len(resp_dict["data"]))
        return resp_dict

    def _get_tidedbdata_results(self, search_id, range_start=0, range_end=None):
        endpoint = 'tide/api/data/threats/state'
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        payload = json.loads(search_id)
        resp_dict = dict()
        resp_dict["data"] = []

        start = range_start if range_start else 0
        end = range_end if range_end else 0

        params = {"rlimit": self.result_limit,}

        if "type=" not in search_id:
            params["type"] = payload["threat_type"]

        if payload["threat_type"] == "ip":
            params["include_ipv6"] = "true"

        # NOTE: Tide does not support pagination via multiple requests. All results returned in the response.
        resp = self.client.call_api(endpoint + "?" + payload["query"], 'GET', urldata=params, headers=headers, timeout=self.timeout)

        resp_dict["code"] = resp.code
        if resp.code != 200:
            if resp.code == 401:
                resp_dict["message"] = resp.read().decode("utf-8")
            else:
                response_payload = json.loads(resp.read())
                resp_dict["message"] = response_payload["error"]
            del resp_dict["data"]
            return resp_dict

        response_payload = json.loads(resp.read())
        for i in response_payload["threat"]:
            resp_dict["data"].append({"tideDbData": i})

        # Trim result set based on min/max range values
        end = end if end < len(resp_dict["data"]) else len(resp_dict["data"])
        num_results = end - start

        if len(resp_dict["data"]) > end - start:
            resp_dict["data"] = resp_dict["data"][start:end]

        if resp_dict.get("code") == 200:
            self.logger.debug("The TIDE count is %s", len(resp_dict["data"]))
        return resp_dict
