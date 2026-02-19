from aiogoogle import Aiogoogle, auth
from aiogoogle.models import Request
from aiogoogle.excs import HTTPError
from aiohttp.client_exceptions import ClientConnectionError
from asyncio.exceptions import TimeoutError
import json
from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.error_response import ErrorResponder


class InvalidResponseException(Exception):
    pass


class APIClient:
    QUERY_ENDPOINT = 'v2/detect/rules'
    QUERY_SCOPES = ['https://www.googleapis.com/auth/chronicle-backstory']
    URI = "https://oauth2.googleapis.com/token"

    def __init__(self, connection, configuration):
        self.auth = configuration.get('auth')
        self.auth['private_key'] = self.auth.get('private_key').replace('\\n', '\n')
        self.auth['token_uri'] = self.URI
        self.host = "https://" + connection.get('host')
        self.result_limit = connection['options'].get('result_limit')
        self.timeout = connection['options'].get('timeout')
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]
        self.http_client = None

    async def ping_box(self):
        """
        Ping the Data Source
        :return: Response object
        """
        ping_endpoint = self.host + "/" + self.QUERY_ENDPOINT
        if not self.http_client:
            self.create_http_client()
        return await self.client_api(ping_endpoint, 'GET')

    async def create_search(self, query):
        """
        Create the rule and run the retrohunt for the rule
        :param query: string/dict
        :return: Response object
        """
        response_dict = {}
        return_obj = {}
        try:
            if isinstance(query, str):
                query = json.loads(query)

            rule_text = {"ruleText": query["ruleText"]}
            rule_response = await self.create_rule(rule_text)  # calls the api to create the rule
            parsed = rule_response.content
            if rule_response.status_code == 200:
                if 'ruleId' in parsed.keys():

                    run_retrohunt_endpoint = self.host + "/" + self.QUERY_ENDPOINT + "/" + parsed['ruleId'] + \
                                             ':runRetrohunt'

                    date = {"startTime": query["startTime"], "endTime": query["endTime"]}
                    # calls the api to run the retrohunt.
                    return await self.client_api(run_retrohunt_endpoint, 'POST', json.dumps(date))

                raise InvalidResponseException

            response_dict['code'] = rule_response.status_code
            response_dict['message'] = parsed['error'].get('message')
            ErrorResponder.fill_error(return_obj, response_dict, ['message'],
                                      connector=self.connector)

        except ClientConnectionError:
            response_dict['code'] = 1010
            response_dict['message'] = "Invalid Host"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except HTTPError as ex:
            if 'invalid_grant' in str(ex):
                response_dict['code'] = 1015
                response_dict['message'] = "Invalid Client Email"
            else:
                response_dict['message'] = str(ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except ValueError as val_ex:
            if 'Could not deserialize key data' in str(val_ex):
                response_dict['message'] = val_ex
                response_dict['code'] = 1015
            else:
                response_dict['message'] = f'cannot parse {val_ex}'
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except InvalidResponseException:
            response_dict['code'] = 100
            response_dict['message'] = "InvalidResponse"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except TimeoutError as ex:
            response_dict['code'] = 120
            response_dict['message'] = 'TimeoutError ' + str(ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except Exception as ex:
            response_dict['message'] = ex
            self.logger.error('error when getting search results: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        return return_obj

    async def create_rule(self, query):

        """
        Create the rule for the input query
        :param query: dict
        :return: rule id
        """

        create_rule_endpoint = self.host + "/" + self.QUERY_ENDPOINT
        if not self.http_client:
            self.create_http_client()
        return await self.client_api(create_rule_endpoint, 'POST', json.dumps(query))

    async def get_search_status(self, search_id):
        """
        Queries the datasource to fetch the retorohunt status
        :param search_id: str
        :return: response object
        """
        status_id = search_id.split(":")
        if not self.http_client:
            self.create_http_client()
        get_retrohunt_status = self.QUERY_ENDPOINT + "/" + status_id[1] + '/retrohunts/' + status_id[0]
        status_endpoint = self.host + "/" + get_retrohunt_status

        return await self.client_api(status_endpoint, 'GET')

    async def get_search_results(self, search_id, next_page_token, page_size):
        """
        Return the search results
        :param search_id:str
        :param next_page_token: str
        :param page_size: int
        :return: Response object
        """
        if not self.http_client:
            self.create_http_client()
        search_result = search_id.split(":")
        if next_page_token != '0':

            list_detection = f"{self.QUERY_ENDPOINT}/{search_result[1]}/detections?" \
                             f"page_size={page_size}&page_token={next_page_token}"
        else:
            list_detection = f"{self.QUERY_ENDPOINT}/{search_result[1]}/detections?page_size={page_size}"

        list_detection_endpoint = self.host + "/" + list_detection
        return await self.client_api(list_detection_endpoint, 'GET')

    async def delete_search(self, search_id):
        """
        Delete the search id.
        :param search_id:str
        :return: Response object
        """
        if not self.http_client:
            self.create_http_client()
        delete_id = search_id.split(":")

        delete = self.QUERY_ENDPOINT + "/" + delete_id[1]
        delete_endpoint = self.host + "/" + delete
        return await self.client_api(delete_endpoint, 'DELETE')

    def create_http_client(self):
        """
        Initialize the http client object using the credentials
        :return: None
        """
        credentials = auth.creds.ServiceAccountCreds(**self.auth, scopes=self.QUERY_SCOPES)
        self.http_client = Aiogoogle(service_account_creds=credentials)

    async def client_api(self, url, method, data=None):
        """
        make an api call using aiogoogle request module
        :params
        url(str) -> host url
        method(str) -> GET, POST
        data(json) -> query input
        :return: response
        """
        async with self.http_client as client:
            req = Request(url=url, method=method, data=data)
            return await client.as_service_account(req, full_res=True, timeout=self.timeout)
