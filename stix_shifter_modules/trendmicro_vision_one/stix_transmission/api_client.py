import datetime
import json

from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
from stix_shifter_utils.utils import logger

_USER_AGENT = 'TMV1StixShifter/1.0'


class APIClient:

    def __init__(self, connection, configuration):
        self.logger = logger.set_logger(__name__)
        self.endpoint_start = 'v2.0/xdr/'
        headers = dict()
        host_port = connection.get('host') + ':' + str(connection.get('port', ''))
        headers['accept'] = 'application/json'
        auth = configuration.get('auth')
        if auth is not None and auth.get('token', None) is not None:
            headers['Authorization'] = 'Bearer {}'.format(auth.get('token'))
        url_modifier_function = None
        headers['user-agent'] = _USER_AGENT

        self.timeout = connection['options'].get('timeout')

        self.client = RestApiClientAsync(host_port,
                                    None,
                                    headers,
                                    url_modifier_function,
                                    cert_verify=connection.get('selfSignedCert', True),
                                    sni=connection.get('sni', None)
                                    )

    async def ping_data_source(self):
        # Pings the data source
        endpoint = 'v2.0/siem/events'
        now = datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z"
        resp = await self.client.call_api(endpoint, 'GET', timeout=self.timeout, urldata={"startDateTime": now, "endDateTime": now})
        return {"code": resp.code}

    async def get_search_results(self, search_id, range_start=None, range_end=None):
        # Return the search results. Results must be in JSON format before being translated into STIX
        endpoint = self.endpoint_start + 'search/data'
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
            code, response = await self._fetch(endpoint, headers, payload, offset)
            resp_dict["code"] = code
            if code == 200:
                logs = response["data"]['logs']

                if "offset" not in response["data"]:
                    # not support offset
                    if len(logs) > range_start:
                        all_data += logs[range_start:range_end]
                    break
                if not logs:
                    break
                elif end and len(all_data) + len(logs) >= end - start:
                    offset += len(logs)
                    all_data += logs[0:end - start - len(all_data)]
                    break
                else:
                    offset += len(logs)
                    all_data += logs
            else:
                resp_dict["message"] = response["error"]["message"]
                del resp_dict["data"]
                break
            if i == max_fetch_count - 1:
                self.logger.warning("Reach max fetch count %s, stop loop", max_fetch_count)
        if resp_dict.get("code") == 200:
            self.logger.debug("The log count is %s", len(resp_dict["data"]["logs"]))
        return resp_dict

    async def _fetch(self, endpoint, headers, payload, offset):
        payload["offset"] = offset
        resp = await self.client.call_api(endpoint, 'POST', headers=headers, data=json.dumps(payload), timeout=self.timeout)
        payload_dict = json.loads(resp.read())
        return resp.code, payload_dict
