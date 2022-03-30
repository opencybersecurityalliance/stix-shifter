from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient
from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.error_response import ErrorResponder
from .response_mapper import ResponseMapper
from datetime import datetime, timezone
import secrets
import string
import hashlib
import json
from requests.exceptions import ConnectionError


class MaxDailyQuotaException(Exception):
    pass


class APIClient:
    QUERY_ENDPOINT = 'public_api/v1/xql/start_xql_query/'
    RESULT_ENDPOINT = 'public_api/v1/xql/get_query_results/'
    STREAM_ENDPOINT = 'public_api/v1/xql/get_query_results_stream/'
    QUOTA_ENDPOINT = '/public_api/v1/xql/get_quota/'

    def __init__(self, connection, configuration):
        self.auth = configuration.get('auth')
        self.logger = logger.set_logger(__name__)
        nonce = "".join([secrets.choice(string.ascii_letters + string.digits) for _ in range(64)])
        timestamp = int(datetime.now(timezone.utc).timestamp()) * 1000
        self.auth = configuration.get('auth')
        auth_key = f"{self.auth['api_key']}{nonce}{timestamp}"
        auth_key = auth_key.encode("utf-8")
        api_key_hash = hashlib.sha256(auth_key).hexdigest()
        headers = {
            "x-xdr-timestamp": str(timestamp),
            "x-xdr-nonce": nonce,
            "x-xdr-auth-id": str(self.auth['api_key_id']),
            "Authorization": api_key_hash
        }
        self.client = RestApiClient(connection.get('host'),
                                    connection.get('port', None),
                                    headers,
                                    url_modifier_function=None,
                                    )
        self.result_limit = connection['options'].get('result_limit')
        self.timeout = connection['options']['timeout']
        self.quota_threshold = connection['quota_threshold']
        self.connector = __name__.split('.')[1]

    def ping_data_source(self):
        """
        Ping the Data Source
        :return: Response object
        """
        data = {
            "request_data": {}
        }

        return self.client.call_api(self.QUOTA_ENDPOINT, 'POST', headers=self.client.headers,
                                    data=json.dumps(data), timeout=self.timeout)

    def get_remaining_quota(self):
        """
        Pings the quota endpoint to fetch the remaining quota
        :return: Response object
        """
        return_obj = {}
        response_dict = {}
        data = {
            "request_data": {}
        }
        quota_wrapper = None

        try:
            quota_wrapper = self.client.call_api(self.QUOTA_ENDPOINT, 'POST', headers=self.client.headers,
                                                 data=json.dumps(data), timeout=self.timeout)
            quota_response_code = quota_wrapper.response.status_code
            quota_response_text = json.loads(quota_wrapper.read().decode('utf-8'))
            if quota_response_code == 200:
                if 'reply' in quota_response_text.keys():
                    # The daily quota unit for standard license is 5. additional units up to 10 can be added.
                    if quota_response_text['reply']['license_quota'] == 5 and \
                            quota_response_text['reply']['additional_purchased_quota'] == 0.0:
                        # For a Standard license,if the configured quota threshold is greater than 5,
                        # the threshold quota value is reset to 5.
                        self.quota_threshold = 5 if self.quota_threshold > 5 else self.quota_threshold
                        if quota_response_text['reply']['used_quota'] >= self.quota_threshold:
                            raise MaxDailyQuotaException
                    else:
                        if quota_response_text['reply']['used_quota'] >= self.quota_threshold:
                            raise MaxDailyQuotaException
                    return_obj['success'] = True
            else:
                return_obj = ResponseMapper().status_code_mapping(quota_response_code, quota_response_text)

        except ValueError as ex:
            if quota_wrapper is not None:
                self.logger.debug(quota_wrapper.read())
            raise Exception(f'Cannot parse response: {ex}') from ex
        except MaxDailyQuotaException:
            response_dict['type'] = "MaxDailyQuotaException"
            response_dict['message'] = "query usage exceeded max daily quota"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except ConnectionError:
            response_dict['type'] = "ConnectionError"
            response_dict['message'] = "Invalid Host"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except Exception as ex:
            if 'timeout_error' in str(ex):
                response_dict['type'] = 'TimeoutError'
            else:
                response_dict['type'] = ex.__class__.__name__
            response_dict['message'] = ex
            self.logger.error('error when getting search results: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        return return_obj

    def create_search(self, query):
        """
        Queries the data source
        :return: Response object
        """
        return_obj = self.get_remaining_quota()
        if return_obj['success']:
            if not isinstance(query, dict):
                query = json.loads(query)

            for dataset in query.keys():
                query[dataset]["tenants"] = self.auth['tenant'].split(",")
                data = {
                    "request_data":
                        query[dataset]
                }
                return self.client.call_api(self.QUERY_ENDPOINT, 'POST', headers=self.client.headers,
                                            data=json.dumps(data), timeout=self.timeout)
        return return_obj

    def get_search_status(self, search_id):
        """
        Queries the data source to fetch the status of api call
        :return: Response object
        """
        data = {
            "request_data": {
                "query_id": search_id,
                "pending_flag": True,
                "limit": self.result_limit,
                "format": "json"
            }
        }
        return self.client.call_api(self.RESULT_ENDPOINT, 'POST', headers=self.client.headers, data=json.dumps(data),
                                    timeout=self.timeout)

    def get_search_results(self, search_id):
        """
        Return the search results
        :param search_id:str
        :return: Response object
        """
        data = {
            "request_data": {
                "query_id": search_id,
                "pending_flag": False,
                "limit": self.result_limit,
                "format": "json"
            }
        }
        return self.client.call_api(self.RESULT_ENDPOINT, 'POST', headers=self.client.headers, data=json.dumps(data),
                                    timeout=self.timeout)

    @staticmethod
    def delete_search():
        """
        Delete operation of a search id is not supported in Palo Alto Cortex XDR
        :return dict
        """
        return {"code": 200, "success": True}

    def get_stream_results(self, stream_id):
        """
        Return the stream results
        :param stream_id: string
        :return: Raw Json data
        """
        data = {
            "request_data":
                {"stream_id": stream_id,
                 "is_gzip_compressed": False
                 }
            }
        return self.client.call_api(self.STREAM_ENDPOINT, 'POST', headers=self.client.headers, data=json.dumps(data),
                                    timeout=self.timeout)
