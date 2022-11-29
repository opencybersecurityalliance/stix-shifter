from google.oauth2 import service_account
from googleapiclient import _auth
from google.auth.exceptions import RefreshError
from httplib2 import ServerNotFoundError
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
        self.auth['private_key'] = connection.get('selfSignedCert').replace('\\n', '\n')
        self.auth['token_uri'] = self.URI
        self.host = "https://" + connection.get('host')
        self.result_limit = connection['options'].get('result_limit')
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
        return self.http_client.request(ping_endpoint, 'GET')

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
            rule_response = self.create_rule(rule_text)  # calls the api to create the rule
            parsed = json.loads(rule_response[1])
            if rule_response[0].status == 200:
                if 'ruleId' in parsed.keys():

                    run_retrohunt_endpoint = self.host + "/" + self.QUERY_ENDPOINT + "/" + parsed['ruleId'] + \
                                             ':runRetrohunt'

                    date = {"startTime": query["startTime"], "endTime": query["endTime"]}
                    # calls the api to run the retrohunt.
                    return self.http_client.request(run_retrohunt_endpoint, 'POST', body=json.dumps(date))

                raise InvalidResponseException

            response_dict['code'] = rule_response[0].status
            response_dict['message'] = parsed['error'].get('message')
            ErrorResponder.fill_error(return_obj, response_dict, ['message'],
                                      connector=self.connector)

        except ServerNotFoundError:
            response_dict['code'] = 1010
            response_dict['message'] = "Invalid Host"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except RefreshError:
            response_dict['code'] = 1015
            response_dict['message'] = "Invalid Client Email"
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

        except Exception as ex:
            if "timed out" in str(ex):
                response_dict['code'] = 120
                response_dict['message'] = str(ex)
            else:
                response_dict['message'] = ex
            self.logger.error('error when getting search results: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        return return_obj

    def create_rule(self, query):

        """
        Create the rule for the input query
        :param query: dict
        :return: rule id
        """

        create_rule_endpoint = self.host + "/" + self.QUERY_ENDPOINT
        if not self.http_client:
            self.create_http_client()
        return self.http_client.request(create_rule_endpoint, 'POST', body=json.dumps(query))

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

        return self.http_client.request(status_endpoint, 'GET')

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
        return self.http_client.request(list_detection_endpoint, 'GET')

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
        return self.http_client.request(delete_endpoint, 'DELETE')

    def create_http_client(self):
        """
        Initialize the http client object using the credentials
        :return: None
        """
        credentials = service_account.Credentials.from_service_account_info(self.auth, scopes=self.QUERY_SCOPES)
        self.http_client = _auth.authorized_http(credentials)
