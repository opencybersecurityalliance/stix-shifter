#!/usr/bin/python

""" OneLoginClient class

Copyright (c) 2021, OneLogin, Inc.
All rights reserved.

OneLoginClient class of the OneLogin's Python SDK.

"""

import datetime
from dateutil import tz
import requests

import base64
try:
    from urllib.parse import unquote_plus, parse_qsl
except ImportError:
    from urlparse import parse_qsl
    from urllib import unquote_plus

from onelogin.api.models.app import App
from onelogin.api.models.app_rule import AppRule
from onelogin.api.models.auth_factor import AuthFactor
from onelogin.api.models.assigned_user import AssignedUser
from onelogin.api.models.assigned_admin import AssignedAdmin
from onelogin.api.models.brand import Brand
from onelogin.api.models.connector import Connector
from onelogin.api.models.event import Event
from onelogin.api.models.embed_app import EmbedApp
from onelogin.api.models.event_type import EventType
from onelogin.api.models.factor_enrollment_response import FactorEnrollmentResponse
from onelogin.api.models.group import Group
from onelogin.api.models.mapping import Mapping
from onelogin.api.models.mfa_check_status import MFACheckStatus
from onelogin.api.models.mfa_token import MFAToken
from onelogin.api.models.onelogin_app import OneLoginApp
from onelogin.api.models.onelogin_token import OneLoginToken
from onelogin.api.models.otp_device import OTP_Device
from onelogin.api.models.privilege import Privilege
from onelogin.api.models.rate_limit import RateLimit
from onelogin.api.models.role import Role
from onelogin.api.models.smart_hook import SmartHook
from onelogin.api.models.smart_hook_log import SmartHookLog
from onelogin.api.models.smart_hook_env import SmartHookEnv
from onelogin.api.models.smart_mfa import SmartMFA
from onelogin.api.models.statement import Statement
from onelogin.api.models.risk_rule import RiskRule
from onelogin.api.models.risk_score import RiskScore
from onelogin.api.models.risk_score_insights import RiskScoreInsights
from onelogin.api.models.user import User
from onelogin.api.models.user_app import UserApp
from onelogin.api.util.constants import Constants
from onelogin.api.util.urlbuilder import UrlBuilder
from onelogin.api.util.exception_handlers import exception_handler, exception_handler_return_false
from onelogin.api.util.response_handlers import (extract_error_message_from_response, extract_error_attribute_from_response,
                                                 get_after_cursor, handle_operation_response, handle_session_token_response,
                                                 handle_saml_endpoint_response, get_resource_list, get_ids, retrieve_apps_from_xml,
                                                 get_resource_or_id, op_create_success, op_delete_success)

from onelogin.api.version import __version__


class OneLoginClient(object):
    '''

    The OneLoginClient makes the API calls to the Onelogin's platform described
    at https://developers.onelogin.com/api-docs/1/getting-started/dev-overview.

    '''

    client_id = None
    client_secret = None

    CUSTOM_USER_AGENT = "onelogin-python-sdk %s" % __version__

    api_configuration = {
        "user": 2,
        "connector": 2,
        "app": 1,
        "app_rule": 2,
        "role": 2,
        "event": 1,
        "group": 1,
        "custom_login": 1,
        "assertion": 2,
        "mfa": 2,
        "invite": 1,
        "privilege": 1,
        "branding": 2,
        "smarthook": 2,
        "smartmfa": 2,
        "risk": 2,
        "user_mapping": 2,
    }

    def __init__(self, client_id, client_secret, region='us', max_results=1000, default_timeout=(10, 60), subdomain=None, api_configuration={}):
        """

        Create a new instance of OneLoginClient.

        :param client_id: API Credentials client_id
        :type client_id: string
        :param client_secret: API Credentials client_secret
        :type client_secret: string
        :param region: OneLogin region, either us or eu
        :type region: string
        :param max_results: Maximum number of results returned by list operations
        :type max_results: int
        :param default_timeout: a request timeout
        See http://docs.python-requests.org/en/master/user/advanced/#timeouts
        :type default_timeout: (float, float)
        :param subdomain: If the subdomain is provided, API calls gonna be done using the subdomain instead the region
        :type subdomain: string
        :param api_configuration: allows to define the api endpoint version to be used
        :type api_configuration: dict

        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.max_results = max_results
        self.url_builder = UrlBuilder(region, subdomain)
        self.user_agent = self.CUSTOM_USER_AGENT
        self.access_token = self.refresh_token = self.expiration = None
        self.error = None
        self.error_description = None
        self.error_attribute = None
        self.requests_timeout = default_timeout
        if api_configuration:
            self.api_configuration.update(api_configuration)

    def set_timeout(self, timeout=None):
        """

        Changes the timeout used when placing requests with the execute_call method
        :param timeout: a request timeout
        See http://docs.python-requests.org/en/master/user/advanced/#timeouts

        """
        self.requests_timeout = timeout

    def clean_error(self):
        """

        Clean any previous error registered at the client.

        """
        self.error = None
        self.error_description = None
        self.error_attribute = None

    def get_version_id(self, base):
        return self.url_builder.get_version_id(self.api_configuration, base)

    def get_url(self, base, obj_id=None, extra_id=None, version_id=None):
        return self.url_builder.get_url(base, obj_id, extra_id, version_id)

    def set_error(self, response, include_attribute=False):
        self.error = str(response.status_code)
        self.error_description = extract_error_message_from_response(response)
        if include_attribute:
            self.error_attribute = extract_error_attribute_from_response(response)

    def retrieve_resources(self, resource_cls, url, query_parameters, max_results=None, version_id=1):
        if max_results is None:
            max_results = self.max_results

        if query_parameters is not None and type(query_parameters) is not dict:
            raise Exception("query_parameters needs to be a dict")

        resources = []
        response = None
        after_cursor = None
        while (not response) or (len(resources) < max_results and after_cursor):
            response = self.execute_call('get', url, params=query_parameters)
            if response.status_code == 200:
                json_data = response.json()
                if json_data:
                    data = []
                    if version_id == 1 and json_data.get('data', None):
                        data = json_data['data']
                    elif version_id == 2 and json_data:
                        data = json_data
                    for resource_data in data:
                        if resource_data and len(resources) < max_results:
                            resources.append(resource_cls(resource_data))
                        else:
                            return resources
                after_cursor = get_after_cursor(response, version_id)
                if after_cursor:
                    if not query_parameters:
                        query_parameters = {}
                    if version_id == 1:
                        query_parameters['after_cursor'] = after_cursor
                    else:
                        # TODO: Replace when cursor bug is gone
                        # query_parameters['cursor'] = after_cursor
                        data = base64.b64decode(unquote_plus(after_cursor))
                        page_params = parse_qsl(data)
                        for key, value in page_params:
                            query_parameters[key] = value
            else:
                self.set_error(response)
                return None
        return resources

    def retrieve_resource(self, resource_cls, url, version_id):
        response = self.execute_call('get', url)
        if response.status_code == 200:
            return get_resource_or_id(resource_cls, response.json(), version_id)
        else:
            self.set_error(response)

    def retrieve_resource_list(self, resource_cls, url, params, index, version_id):
        response = self.execute_call('get', url, params=params)
        if response.status_code == 200:
            return get_resource_list(resource_cls, response.json(), index, version_id)
        else:
            self.set_error(response)

    def retrieve_list(self, url, version_id):
        response = self.execute_call('get', url)
        if response.status_code == 200:
            data_list = []
            json_data = response.json()
            if version_id == 1:
                if json_data and json_data.get('data', None):
                    data_list = json_data['data'][0]
            else:
                data_list = json_data
            return data_list
        else:
            self.set_error(response)

    def create_resource(self, resource_cls, url, data, query_params, version_id):
        response = self.execute_call('post', url, json=data, params=query_params)
        if op_create_success(response.status_code):
            return get_resource_or_id(resource_cls, response.json(), version_id)
        else:
            self.set_error(response, True)

    def create_operation(self, url, data):
        response = self.execute_call('post', url, json=data)

        if op_create_success(response.status_code):
            return handle_operation_response(response)
        else:
            self.set_error(response, True)
        return False

    def submit_operation(self, url, data):
        response = self.execute_call('post', url, json=data)

        if op_create_success(response.status_code):
            return True
        else:
            self.set_error(response, True)
        return False

    def update_resource(self, resource_cls, url, data, query_params, version_id):
        response = self.execute_call('put', url, json=data, params=query_params)
        if response.status_code == 200:
            return get_resource_or_id(resource_cls, response.json(), version_id)
        else:
            self.set_error(response, True)

    def set_operation(self, url, ids, version_id):
        response = self.execute_call('put', url, json=ids)
        if response.status_code == 200:
            return get_ids(response.json())
        else:
            self.set_error(response, True)

    def add_to_resource_operation(self, url, ids, version_id):
        response = self.execute_call('post', url, json=ids)
        if response.status_code == 200:
            return get_ids(response.json())
        else:
            self.set_error(response, True)

    def remove_from_resource_operation(self, url, ids, version_id):
        response = self.execute_call('delete', url, json=ids)
        if response.status_code == 204:
            return True
        else:
            self.set_error(response, True)

    def update_operation(self, url, data):
        response = self.execute_call('put', url, json=data)

        if response.status_code == 200:
            return handle_operation_response(response)
        else:
            self.set_error(response, True)
        return False

    def delete_resource(self, url, version_id):
        response = self.execute_call('delete', url)

        if op_delete_success(response.status_code):
            if version_id == 1:
                return handle_operation_response(response)
            return True
        else:
            self.set_error(response, True)
        return False

    def process_login(self, url, headers, data):
        response = self.execute_call('post', url, headers=headers, json=data)

        if response.status_code == 200:
            return handle_session_token_response(response)
        else:
            self.set_error(response)

    def process_token_response(self, response):
        json_data = response.json()
        if 'status' in json_data:
            self.error = str(json_data['status']['code'])
            self.error_description = extract_error_message_from_response(response)
        else:
            token = OneLoginToken(json_data)
            self.access_token = token.access_token
            self.refresh_token = token.refresh_token
            self.expiration = token.created_at + datetime.timedelta(seconds=token.expires_in)
            return token

    def retrieve_saml_assertion(self, url, data, version_id):
        response = self.execute_call('post', url, json=data)

        if response.status_code == 200:
            return handle_saml_endpoint_response(response, version_id)
        else:
            self.set_error(response)

    def is_expired(self):
        return self.expiration is not None and datetime.datetime.now(tz.tzutc()) > self.expiration

    def prepare_token(self):
        if self.access_token is None:
            self.get_access_token()
        elif self.is_expired():
            self.regenerate_token()

    def remove_stored_token(self):
        self.access_token = None
        self.refresh_token = None
        self.expiration = None

    def get_headers(self, bearer=True):
        return {
            'Content-Type': 'application/json',
            'User-Agent': self.user_agent
        }

    def get_authorized_headers(self, bearer=True, headers=None):
        if bearer:
            # Removed the ":"
            authorization = "bearer %s" % self.access_token
        else:
            authorization = "client_id:%s, client_secret:%s" % (self.client_id, self.client_secret)

        if headers is None:
            headers = self.get_headers()

        headers.update({'Authorization': authorization})
        return headers

    # OAuth 2.0 Tokens Methods
    @exception_handler
    def get_access_token(self):
        """

        Generates an access token and refresh token that you may use to
        call Onelogin's API methods.

        Returns the generated OAuth Token info
        :return: OAuth Token info
        :rtype: OneLoginToken

        See https://developers.onelogin.com/api-docs/1/oauth20-tokens/generate-tokens Generate Tokens documentation.

        """
        self.clean_error()

        url = self.get_url(Constants.TOKEN_REQUEST_URL)

        data = {
            'grant_type': 'client_credentials'
        }

        headers = self.get_authorized_headers(bearer=False)

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return self.process_token_response(response)
        else:
            self.set_error(response)

    @exception_handler
    def regenerate_token(self):
        """

        Refreshing tokens provides a new set of access and refresh tokens.

        Returns the refreshed OAuth Token info
        :return: OAuth Token info
        :rtype: OneLoginToken

        See https://developers.onelogin.com/api-docs/1/oauth20-tokens/refresh-tokens Refresh Tokens documentation

        """
        self.clean_error()

        url = self.get_url(Constants.TOKEN_REQUEST_URL)
        headers = self.get_headers()

        data = {
            'grant_type': 'refresh_token',
            'access_token': self.access_token,
            'refresh_token': self.refresh_token
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return self.process_token_response(response)
        else:
            if response.status_code == 401:
                self.remove_stored_token()
            self.set_error(response)

    @exception_handler_return_false
    def revoke_token(self):
        """

        Revokes an access token and refresh token pair.

        See https://developers.onelogin.com/api-docs/1/oauth20-tokens/revoke-tokens Revoke Tokens documentation

        """
        self.clean_error()

        url = self.get_url(Constants.TOKEN_REVOKE_URL)
        headers = self.get_authorized_headers(bearer=False)

        data = {
            'access_token': self.access_token,
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            self.remove_stored_token()
            return True
        else:
            self.set_error(response)
        return False

    @exception_handler
    def get_rate_limits(self):
        """

        Gets current rate limit details about an access token.

        Returns the rate limit info
        :return: rate limit info
        :rtype: RateLimit

        See https://developers.onelogin.com/api-docs/1/oauth20-tokens/get-rate-limit Get Rate Limit documentation

        """
        self.clean_error()

        url = self.get_url(Constants.GET_RATE_URL)

        version_id = 1
        return self.retrieve_resource(RateLimit, url, version_id)

    # User Methods
    @exception_handler
    def get_users(self, query_parameters=None, max_results=None):
        """

        Gets a list of User resources.

        :param query_parameters: Parameters to filter the result of the list
        :type query_parameters: dict

        :param max_results: Limit the number of users returned (optional)
        :type max_results: int

        Returns the list of users
        :return: users list
        :rtype: list[User]

        See https://developers.onelogin.com/api-docs/1/users/get-users Get Users documentation
            https://developers.onelogin.com/api-docs/2/users/list-users
        """
        self.clean_error()

        version_id = self.get_version_id("GET_USERS_URL")
        url = self.get_url(Constants.GET_USERS_URL, version_id=version_id)
        return self.retrieve_resources(User, url, query_parameters, max_results, version_id)

    @exception_handler
    def get_user(self, user_id):
        """

        Gets User by ID.

        :param user_id: Id of the user
        :type user_id: int

        Returns the user identified by the id
        :return: user
        :rtype: User

        See https://developers.onelogin.com/api-docs/1/users/get-user-by-id Get User by ID documentation
            https://developers.onelogin.com/api-docs/2/users/get-user
        """
        self.clean_error()

        version_id = self.get_version_id("GET_USER_URL")
        url = self.get_url(Constants.GET_USER_URL, user_id, version_id=version_id)

        return self.retrieve_resource(User, url, version_id)

    @exception_handler
    def get_user_apps(self, user_id, ignore_visibility=None):
        """

        Gets a list of apps accessible by a user, not including personal apps.

        :param user_id: Id of the user
        :type user_id: int

        :param ignore_visibility Defaults to `false`. When `true` will all apps that are assigned to a user regardless of their portal visibility setting.
        :type ignore_visibility bool

        Returns the apps user identified by the id
        :return: App list of the user
        :rtype: list[UserApp]

        See https://developers.onelogin.com/api-docs/1/users/get-apps-for-user Get Apps for a User documentation
            https://developers.onelogin.com/api-docs/2/users/get-user-apps
        """
        self.clean_error()

        version_id = self.get_version_id("GET_APPS_FOR_USER_URL")
        url = self.get_url(Constants.GET_APPS_FOR_USER_URL, user_id, version_id=version_id)

        query_parameters = None
        if version_id == 1:
            if ignore_visibility is not None:
                raise Exception("ignore_visibility parameter not available on /1")
        else:
            if ignore_visibility:
                query_parameters = {"ignore_visibility": "true"}

        return self.retrieve_resource_list(UserApp, url, query_parameters, None, version_id)

    @exception_handler
    def get_user_roles(self, user_id):
        """

        Gets a list of role IDs that have been assigned to a user.

        :param user_id: Id of the user
        :type user_id: int

        Returns the role ids of the user identified by the id
        :return: role ids
        :rtype: list[int]

        See https://developers.onelogin.com/api-docs/1/users/get-roles-for-user Get Roles for a User documentation

        """
        self.clean_error()

        version_id = self.get_version_id("GET_ROLES_FOR_USER_URL")
        url = self.get_url(Constants.GET_ROLES_FOR_USER_URL, user_id, version_id=version_id)

        return self.retrieve_list(url, version_id)

    @exception_handler
    def get_custom_attributes(self):
        """

        Gets a list of all custom attribute fields (also known as custom user fields) that have been defined for OL account.

        Returns the custom attributes of the account
        :return: custom attribute list
        :rtype: list[str]

        See https://developers.onelogin.com/api-docs/1/users/get-custom-attributes Get Custom Attributes documentation

        """
        self.clean_error()

        version_id = self.get_version_id("GET_CUSTOM_ATTRIBUTES_URL")
        url = self.get_url(Constants.GET_CUSTOM_ATTRIBUTES_URL, version_id=version_id)

        return self.retrieve_list(url, version_id)

    @exception_handler
    def create_user(self, user_params, mappings=None, validate_policy=None):
        """

        Creates an user

        :param user_params: User data (firstname, lastname, email, username, company,
                                       department, directory_id, distinguished_name,
                                       external_id, group_id, invalid_login_attempts,
                                       locale_code, manager_ad_id, member_of,
                                       openid_name, phone, samaccountname, title,
                                       userprincipalname)
                                   v2 (password_confirmation, password_algorithm, salt, role_ids
                                       state, status, trusted_idp_id)
        :type user_params: dict

        :param mappings: Controls how mappings will be applied to the user on creation
                        [async, sync, disabled]
        :type mappings: string

        :param validate_policy: Validate password against user policy?
        :type validate_policy: bool

        Returns the created user
        :return: user
        :rtype: User

        See https://developers.onelogin.com/api-docs/1/users/create-user Create User documentation
            https://developers.onelogin.com/api-docs/2/users/create-user
        """
        self.clean_error()

        version_id = self.get_version_id("CREATE_USER_URL")
        url = self.get_url(Constants.CREATE_USER_URL, version_id=version_id)

        query_params = None

        if version_id == 1:
            if mappings is not None:
                raise Exception("mappings parameter not available on /1")
            if validate_policy is not None:
                raise Exception("validate_policy parameter not available on /1")
            for key in user_params.keys():
                if key in ["password_confirmation", "password_algorithm", "salt", "role_ids"
                           "state", "status", "trusted_idp_id"]:
                    raise Exception("%s parameter not available on /1" % key)
        else:
            query_params = {}
            if mappings is not None:
                query_params["mappings"] = mappings
            if validate_policy is False:
                query_params["validate_policy"] = "false"

        return self.create_resource(User, url, user_params, query_params, version_id)

    @exception_handler
    def update_user(self, user_id, user_params, mappings=None, validate_policy=None):
        """

        Updates an user

        :param user_id: Id of the user
        :type user_id: int

        :param user_params: User data (firstname, lastname, email, username, company,
                                       department, directory_id, distinguished_name,
                                       external_id, group_id, invalid_login_attempts,
                                       locale_code, manager_ad_id, member_of,
                                       openid_name, phone, samaccountname, title,
                                       userprincipalname)
                                   v2 (password_confirmation, password_algorithm, salt, role_ids
                                       state, status, trusted_idp_id)
        :type user_params: dict

        :param mappings: Controls how mappings will be applied to the user on creation
                        [async, sync, disabled]
        :type mappings: string

        :param validate_policy: Validate password against user policy?
        :type validate_policy: bool

        Returns the modified user
        :return: user
        :rtype: User

        See https://developers.onelogin.com/api-docs/1/users/update-user Update User by ID documentation
            https://developers.onelogin.com/api-docs/2/users/update-user
        """
        self.clean_error()

        version_id = self.get_version_id("UPDATE_USER_URL")
        url = self.get_url(Constants.UPDATE_USER_URL, user_id, version_id=version_id)

        query_parameters = None

        if version_id == 1:
            if mappings is not None:
                raise Exception("mappings parameter not available on /1")
            if validate_policy is not None:
                raise Exception("validate_policy parameter not available on /1")
            for key in user_params.keys():
                if key in ["password_confirmation", "password_algorithm", "salt", "role_ids"
                           "state", "status"]:
                    raise Exception("%s parameter not available on /1" % key)

        else:
            query_params = {}
            if mappings is not None:
                query_params["mappings"] = mappings
            if validate_policy is False:
                query_params["validate_policy"] = "false"

        return self.update_resource(User, url, user_params, query_parameters, version_id)

    @exception_handler_return_false
    def assign_role_to_user(self, user_id, role_ids):
        """

        Assigns Roles to User

        :param user_id: Id of the user
        :type user_id: int

        :param role_ids: List of role ids to be added
        :type user_params: integer array

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/users/assign-role-to-user Assign Role to User documentation

        """
        self.clean_error()

        version_id = self.get_version_id("ADD_ROLE_TO_USER_URL")
        url = self.get_url(Constants.ADD_ROLE_TO_USER_URL, user_id, version_id=version_id)

        data = {
            'role_id_array': role_ids
        }

        return self.update_operation(url, data)

    @exception_handler_return_false
    def remove_role_from_user(self, user_id, role_ids):
        """

        Remove Role from User

        :param user_id: Id of the user
        :type user_id: int

        :param role_ids: List of role ids to be removed
        :type role_ids: integer array

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/users/remove-role-from-user Remove Role from User documentation

        """
        self.clean_error()

        version_id = self.get_version_id("DELETE_ROLE_TO_USER_URL")
        url = self.get_url(Constants.DELETE_ROLE_TO_USER_URL, user_id, version_id=version_id)

        data = {
            'role_id_array': role_ids
        }

        return self.update_operation(url, data)

    @exception_handler_return_false
    def set_password_using_clear_text(self, user_id, password, password_confirmation, validate_policy=False):
        """

        Sets Password by ID Using Cleartext

        :param user_id: Id of the user
        :type user_id: int

        :param password: Set to the password value using cleartext.
        :type password: string

        :param password_confirmation: Ensure that this value matches the password value exactly.
        :type password_confirmation: string

        :param validate_policy: Defaults to false. This will validate the password against the users OneLogin password policy..
        :type validate_policy: boolean

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/users/set-password-in-cleartext Set Password by ID Using Cleartext documentation

        """
        self.clean_error()

        version_id = self.get_version_id("SET_PW_CLEARTEXT")
        url = self.get_url(Constants.SET_PW_CLEARTEXT, user_id, version_id=version_id)

        data = {
            'password': password,
            'password_confirmation': password_confirmation,
            'validate_policy': validate_policy
        }

        return self.update_operation(url, data)

    @exception_handler_return_false
    def set_password_using_hash_salt(self, user_id, password, password_confirmation, password_algorithm, password_salt=None):
        """

        Set Password by ID Using Salt and SHA-256

        :param user_id: Id of the user
        :type user_id: int

        :param password: Set to the password value using a SHA-256-encoded value.
        :type password: string

        :param password_confirmation: Ensure that this value matches the password value exactly.
        :type password_confirmation: string

        :param password_algorithm: Set to salt+sha256.
        :type password_algorithm: string

        :param password_salt: (Optional) To provide your own salt value.
        :type password_salt: string

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/users/set-password-using-sha-256 Set Password by ID Using Salt and SHA-256 documentation

        """
        self.clean_error()

        version_id = self.get_version_id("SET_PW_SALT")
        url = self.get_url(Constants.SET_PW_SALT, user_id, version_id=version_id)

        data = {
            'password': password,
            'password_confirmation': password_confirmation,
            'password_algorithm': password_algorithm
        }
        if password_salt:
            data["password_salt"] = password_salt

        return self.update_operation(url, data)

    @exception_handler_return_false
    def set_state_to_user(self, user_id, state):
        """

        Set the State for a user.

        :param user_id: Id of the user
        :type user_id: int

        :param state: Set to the state value. Valid values: 0-3
        :type state: int

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/users/set-state Set User State documentation

        """
        self.clean_error()

        version_id = self.get_version_id("SET_STATE_TO_USER_URL")
        url = self.get_url(Constants.SET_STATE_TO_USER_URL, user_id, version_id=version_id)

        data = {
            'state': state
        }

        return self.update_operation(url, data)

    @exception_handler_return_false
    def set_custom_attribute_to_user(self, user_id, custom_attributes):
        """

        Set Custom Attribute Value

        :param user_id: Id of the user
        :type user_id: int

        :param custom_attributes: Provide one or more key value pairs composed of the custom attribute field shortname and the value that you want to set the field to.
        :type custom_attributes: dict

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/users/set-custom-attribute Set Custom Attribute Value documentation

        """
        self.clean_error()

        version_id = self.get_version_id("SET_CUSTOM_ATTRIBUTE_TO_USER_URL")
        url = self.get_url(Constants.SET_CUSTOM_ATTRIBUTE_TO_USER_URL, user_id, version_id=version_id)

        data = {
            'custom_attributes': custom_attributes
        }

        return self.update_operation(url, data)

    @exception_handler_return_false
    def log_user_out(self, user_id):
        """

        Log a user out of any and all sessions.

        :param user_id: Id of the user to be logged out
        :type user_id: int

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/users/log-user-out Log User Out documentation

        """
        self.clean_error()

        version_id = self.get_version_id("LOG_USER_OUT_URL")
        url = self.get_url(Constants.LOG_USER_OUT_URL, user_id, version_id=version_id)

        return self.update_operation(url, None)

    @exception_handler_return_false
    def lock_user(self, user_id, minutes):
        """

        Use this call to lock a user's account based on the policy assigned to
        the user, for a specific time you define in the request, or until you
        unlock it.

        :param user_id: Id of the user to be locked.
        :type user_id: int

        :param minutes: Set to the number of minutes for which you want to lock the user account. (0 to delegate on policy)
        :type minutes: int

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/users/lock-user-account Lock User Account documentation

        """
        self.clean_error()

        version_id = self.get_version_id("LOCK_USER_URL")
        url = self.get_url(Constants.LOCK_USER_URL, user_id, version_id=version_id)

        data = {
            'locked_until': minutes
        }

        return self.update_operation(url, data)

    @exception_handler_return_false
    def delete_user(self, user_id):
        """

        Deletes an user

        :param user_id: Id of the user to be deleted
        :type user_id: int

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/users/delete-user Delete User by ID documentation

        """
        self.clean_error()

        version_id = self.get_version_id("DELETE_USER_URL")
        url = self.get_url(Constants.DELETE_USER_URL, user_id, version_id=version_id)

        return self.delete_resource(url, version_id)

    # Generate an access token for a user
    @exception_handler
    def generate_mfa_token(self, user_id, expires_in=259200, reusable=False):
        """
        Use to generate a temporary MFA token that can be used in place of other MFA tokens for a set time period.
        For example, use this token for account recovery.

        :param user_id: Id of the user
        :type user_id: int

        :param expires_in: Set the duration of the token in seconds.
                          (default: 259200 seconds = 72h) 72 hours is the max value.
        :type expires_in: int

        :param reusable: Defines if the token reusable. (default: false) If set to true, token can be used for multiple apps, until it expires.
        :type reusable: bool

        Returns a mfa token
        :return: return the object if success
        :rtype: MFAToken

        See https://developers.onelogin.com/api-docs/1/multi-factor-authentication/generate-mfa-token Generate MFA Token documentation

        """
        self.clean_error()

        version_id = self.get_version_id("GENERATE_MFA_TOKEN_URL")
        url = self.get_url(Constants.GENERATE_MFA_TOKEN_URL, user_id, version_id=version_id)

        data = {
            'expires_in': expires_in,
            'reusable': reusable
        }

        # It has version 2 result
        return self.create_resource(MFAToken, url, data, None, 2)

    # Custom Login Pages
    @exception_handler
    def create_session_login_token(self, query_params, allowed_origin=''):
        """

        Generates a session login token in scenarios in which MFA may or may not be required.
        A session login token expires two minutes after creation.

        :param query_params: Query Parameters (username_or_email, password, subdomain, return_to_url,
                                               ip_address, browser_id)
        :type query_params: dict

        :param allowed_origin: Custom-Allowed-Origin-Header. Required for CORS requests only.
                               Set to the Origin URI from which you are allowed to send a request
                               using CORS.
        :type allowed_origin: string

        Returns a session token
        :return: return the object if success
        :rtype: SessionTokenInfo/SessionTokenMFAInfo

        See https://developers.onelogin.com/api-docs/1/users/create-session-login-token Create Session Login Token documentation

        """
        self.clean_error()

        version_id = self.get_version_id("SESSION_LOGIN_TOKEN_URL")
        url = self.get_url(Constants.SESSION_LOGIN_TOKEN_URL, version_id=version_id)
        headers = self.get_authorized_headers()

        if allowed_origin:
            headers.update({'Custom-Allowed-Origin-Header-1': allowed_origin})

        return self.process_login(url, headers, query_params)

    @exception_handler
    def get_session_token_verified(self, device_id, state_token, otp_token=None, allowed_origin='', do_not_notify=False):
        """

        Verify a one-time password (OTP) value provided for multi-factor authentication (MFA).

        :param device_id: Provide the MFA device_id you are submitting for verification.
        :type device_id: string

        :param state_token: Provide the state_token associated with the MFA device_id you are submitting for verification.
        :type state_token: string

        :param otp_token: Provide the OTP value for the MFA factor you are submitting for verification.
        :type otp_token: string

        :param allowed_origin: Required for CORS requests only. Set to the Origin URI from which you are allowed to send a request using CORS.
        :type allowed_origin: string

        :param do_not_notify: When verifying MFA via Protect Push, set this to true to stop additional push notifications being sent to the OneLogin Protect device.
        :type do_not_notify: bool

        Returns a session token
        :return: return the object if success
        :rtype: SessionTokenInfo

        See https://developers.onelogin.com/api-docs/1/users/verify-factor Verify Factor documentation

        """
        self.clean_error()

        version_id = self.get_version_id("GET_TOKEN_VERIFY_FACTOR")
        url = self.get_url(Constants.GET_TOKEN_VERIFY_FACTOR, version_id=version_id)
        headers = self.get_authorized_headers()

        if allowed_origin:
            headers.update({'Custom-Allowed-Origin-Header-1': allowed_origin})

        data = {
            'device_id': str(device_id),
            'state_token': state_token,
            'do_not_notify': do_not_notify
        }
        if otp_token:
            data['otp_token'] = otp_token

        return self.process_login(url, headers, data)

    # Connector Methods
    @exception_handler
    def get_connectors(self, query_parameters=None, max_results=None):
        """

        Gets a list of all Connectors in a OneLogin account.

        :param query_parameters: Parameters to filter the result of the list
        :type query_parameters: dict

        :param max_results: Limit the number of connectors returned (optional)
        :type max_results: int

        Returns the list of connectors
        :return: conector list
        :rtype: list[Connector]

        See https://developers.onelogin.com/api-docs/2/connectors/list-connectors List Connectors documentation

        """
        self.clean_error()

        version_id = self.get_version_id("GET_CONNECTORS_URL")
        url = self.get_url(Constants.GET_CONNECTORS_URL, version_id=version_id)

        return self.retrieve_resources(Connector, url, query_parameters, max_results, version_id)

    # Onelogin Apps Methods
    @exception_handler
    def get_apps(self, query_parameters=None, max_results=None):
        """

        Gets a list of all Apps in a OneLogin account.

        :param query_parameters: Parameters to filter the result of the list
        :type query_parameters: dict

        :param max_results: Limit the number of apps returned (optional)
        :type max_results: int

        Returns the list of apps
        :return: app list
        :rtype: list[OneLoginApp]

        See https://developers.onelogin.com/api-docs/1/apps/get-apps Get Apps documentation
            https://developers.onelogin.com/api-docs/2/apps/list-apps
        """
        self.clean_error()

        version_id = self.get_version_id("GET_APPS_URL")
        url = self.get_url(Constants.GET_APPS_URL, version_id=version_id)

        return self.retrieve_resources(OneLoginApp, url, query_parameters, max_results, version_id)

    @exception_handler
    def get_app(self, app_id):
        """

        Gets App by ID.

        :param app_id: Id of the app
        :type app_id: int

        Returns the app identified by the id
        :return: app
        :rtype: OneLoginApp

        See https://developers.onelogin.com/api-docs/2/apps/get-app
        """
        self.clean_error()

        version_id = self.get_version_id("GET_APP_URL")
        url = self.get_url(Constants.GET_APP_URL, app_id, version_id=version_id)

        return self.retrieve_resource(OneLoginApp, url, version_id)

    @exception_handler
    def create_app(self, app_params):
        """

        Creates an app

        :param app_params: App data (connector_id, name, description, visible, policy_id, configuration,
                                     tab_id, visible, brand_id, role_ids, notes)
        :type app_params: dict

        Returns the created app
        :return: app
        :rtype: OneLoginApp

        See https://developers.onelogin.com/api-docs/2/apps/create-app Create App documentation
        """
        self.clean_error()

        version_id = self.get_version_id("CREATE_APP_URL")
        url = self.get_url(Constants.CREATE_APP_URL, version_id=version_id)

        return self.create_resource(OneLoginApp, url, app_params, None, version_id)

    @exception_handler
    def update_app(self, app_id, app_params):
        """

        Updates an app

        :param app_id: Id of the app
        :type app_id: int

        :param app_params: App data (connector_id, name, description, visible, policy_id, configuration,
                                     tab_id, visible, brand_id, role_ids, notes)
        :type app_params: dict

        Returns the modified app
        :return: app
        :rtype: OneLoginApp

        See https://developers.onelogin.com/api-docs/2/apps/update-app Update an App documentation
        """
        self.clean_error()

        version_id = self.get_version_id("UPDATE_APP_URL")
        url = self.get_url(Constants.UPDATE_APP_URL, app_id, version_id=version_id)

        return self.update_resource(OneLoginApp, url, app_params, None, version_id)

    @exception_handler_return_false
    def delete_app(self, app_id):
        """

        Deletes an app

        :param app_id: Id of the app to be deleted
        :type app_id: int

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/2/apps/delete-app Delete App documentation

        """
        self.clean_error()

        version_id = self.get_version_id("DELETE_APP_URL")
        url = self.get_url(Constants.DELETE_APP_URL, app_id, version_id=version_id)

        return self.delete_resource(url, version_id)

    @exception_handler_return_false
    def delete_app_parameter(self, app_id, parameter_id):
        """

        Deletes an App Parameter

        :param app_id: Id of the App
        :type app_id: int

        :param parameter_id: Id of the parameter to be deleted
        :type parameter_id: int

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/2/apps/delete-parameter Delete App Parameter documentation

        """
        self.clean_error()

        version_id = self.get_version_id("DELETE_APP_PARAMETER_URL")
        url = self.get_url(Constants.DELETE_APP_PARAMETER_URL, app_id, parameter_id, version_id=version_id)

        return self.delete_resource(url, version_id)

    @exception_handler
    def get_app_users(self, app_id, query_parameters=None, max_results=None):
        """

        Gets a list of all users related to an App.

        :param app_id: Id of the App
        :type app_id: int

        :param query_parameters: Parameters to filter the result of the list
        :type query_parameters: dict

        :param max_results: Limit the number of apps returned (optional)
        :type max_results: int

        Returns the list of users
        :return: user list
        :rtype: list[User]

        See https://developers.onelogin.com/api-docs/2/apps/list-users List App Users documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_APP_USERS_URL")
        url = self.get_url(Constants.GET_APP_USERS_URL, app_id, version_id=version_id)

        return self.retrieve_resources(User, url, query_parameters, max_results, version_id)

    # App Rule Methods
    @exception_handler
    def get_app_rules(self, app_id, query_parameters=None):
        """

        Gets a list of app rules.

        :param app_id: Id of the App
        :type app_id: int

        :param query_parameters: Parameters to filter the result of the list
                                 (enabled, has_condition, has_condition_type,
                                  has_action, has_action_type)
        :type query_parameters: dict

        Returns the list of app rules
        :return: app rules list
        :rtype: list[AppRule]

        See https://developers.onelogin.com/api-docs/2/app-rules/list-rules List Rules documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_APP_RULES_URL")
        url = self.get_url(Constants.GET_APP_RULES_URL, app_id, version_id=version_id)

        return self.retrieve_resource_list(AppRule, url, query_parameters, None, version_id)

    @exception_handler
    def get_app_rule(self, app_id, app_rule_id):
        """

        Gets App Rule by ID.

        :param app_id: Id of the app
        :type app_id: int

        :param app_rule_id: Id of the app rule
        :type app_rule_id: int

        Returns the app rule identified by the id
        :return: app_rule
        :rtype: AppRule

        See https://developers.onelogin.com/api-docs/2/app-rules/get-rule Get App Rule documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_APP_RULE_URL")
        url = self.get_url(Constants.GET_APP_RULE_URL, app_id, app_rule_id, version_id=version_id)

        return self.retrieve_resource(AppRule, url, version_id)

    @exception_handler
    def create_app_rule(self, app_id, app_rule_params):
        """

        Creates a app rule

        :param app_id: Id of the app
        :type app_id: int

        :param app_rule_params: App Rule data (name, enabled, match, position,
                                               conditions[source, operator, value],
                                               actions[action, value, expression,scriplet, macro])
        :type app_rule_params: dict

        Returns the created app rule
        :return: app_rule
        :rtype: AppRule

        See https://developers.onelogin.com/api-docs/2/app-rules/create-rule Create App Rule documentation
        """
        self.clean_error()

        version_id = self.get_version_id("CREATE_APP_RULE_URL")
        url = self.get_url(Constants.CREATE_APP_RULE_URL, app_id, version_id=version_id)

        if 'actions' in app_rule_params:
            for action in app_rule_params['actions']:
                if 'value' in action and not isinstance(action['value'], list):
                    self.error = "422"
                    self.error_description = "Validation Failed"
                    self.error_attribute = "Verify that the value of any action provided has the type array"
                    return

        return self.create_resource(AppRule, url, app_rule_params, None, version_id)

    @exception_handler
    def update_app_rule(self, app_id, app_rule_id, app_rule_params):
        """

        Updates an app rule

        :param app_id: Id of the app
        :type app_id: int

        :param app_rule_id: Id of the app rule
        :type app_rule_id: int

        :param app_rule_params: App Rule data (name, enabled, match, position,
                                               conditions[source, operator, value],
                                               actions[action, value, expression,scriplet, macro])
        :type app_rule_params: dict

        Returns the modified app rule
        :return: app_rule
        :rtype: AppRule

        See https://developers.onelogin.com/api-docs/2/app-rules/update-rule Update App Rule documentation
        """
        self.clean_error()

        version_id = self.get_version_id("UPDATE_APP_RULE_URL")
        url = self.get_url(Constants.UPDATE_APP_RULE_URL, app_id, app_rule_id, version_id=version_id)

        return self.update_resource(AppRule, url, app_rule_params, None, version_id)

    @exception_handler_return_false
    def delete_app_rule(self, app_id, app_rule_id):
        """

        Deletes a app rule

        :param app_id: Id of the app
        :type app_id: int

        :param app_rule_id: Id of the app rule
        :type app_rule_id: int

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/2/app-rules/delete-rule Delete App Rule documentation

        """
        self.clean_error()

        version_id = self.get_version_id("DELETE_APP_RULE_URL")
        url = self.get_url(Constants.DELETE_APP_RULE_URL, app_id, app_rule_id, version_id=version_id)

        return self.delete_resource(url, version_id)

    @exception_handler
    def get_app_conditions(self, app_id):
        """

        Gets a list of App Conditions types that can be used to match users when app rules are run.

        :param app_id: Id of the App
        :type app_id: int

        Returns the list of conditions
        :return: condition list
        :rtype: list[dict]

        See https://developers.onelogin.com/api-docs/2/app-rules/list-conditions List Conditions documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_APP_CONDITIONS_URL")
        url = self.get_url(Constants.GET_APP_CONDITIONS_URL, app_id, version_id=version_id)

        return self.retrieve_list(url, version_id)

    @exception_handler
    def get_app_condition_operators(self, app_id, condition_value):
        """

        Gets a list of possible operators for a given condition value.

        :param app_id: Id of the App
        :type app_id: int

        :param condition_value: Value for the selected condition (An App Condition).
        :type condition_value: string

        Returns the list of operators
        :return: operator list
        :rtype: list[dict]

        See https://developers.onelogin.com/api-docs/2/app-rules/list-condition-operators List Conditions Operators documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_APP_CONDITION_OPERATORS_URL")
        url = self.get_url(Constants.GET_APP_CONDITION_OPERATORS_URL, app_id, condition_value, version_id=version_id)

        return self.retrieve_list(url, version_id)

    @exception_handler
    def get_app_condition_values(self, app_id, condition_value):
        """

        Gets a list of possible values to compare to a condition type.

        :param app_id: Id of the App
        :type app_id: int

        :param condition_value: Value for the selected condition (An App Condition).
        :type condition_value: string

        Returns the list of values
        :return: value list
        :rtype: list[dict]

        See https://developers.onelogin.com/api-docs/2/app-rules/list-condition-values List Condition Values documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_APP_CONDITION_VALUES_URL")
        url = self.get_url(Constants.GET_APP_CONDITION_VALUES_URL, app_id, condition_value, version_id=version_id)

        return self.retrieve_list(url, version_id)

    @exception_handler
    def get_app_actions(self, app_id):
        """

        Gets a list of the actions that can be applied when an App Rule run

        :param app_id: Id of the App
        :type app_id: int

        Returns the list of actions
        :return: action list
        :rtype: list[dict]

        See https://developers.onelogin.com/api-docs/2/app-rules/list-actions List Actions documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_APP_ACTIONS_URL")
        url = self.get_url(Constants.GET_APP_ACTIONS_URL, app_id, version_id=version_id)

        return self.retrieve_list(url, version_id)

    @exception_handler
    def get_app_action_values(self, app_id, action_value):
        """

        Gets a list of possible values to set using a given action.

        :param app_id: Id of the App
        :type app_id: int

        :param action_value: Value for the selected action (A Mapping Action).
        :type action_value: string

        Returns the list of values
        :return: value list
        :rtype: list[dict]

        See https://developers.onelogin.com/api-docs/2/app-rules/list-action-values List Action values documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_APP_ACTION_VALUES_URL")
        url = self.get_url(Constants.GET_APP_ACTION_VALUES_URL, app_id, action_value, version_id=version_id)

        return self.retrieve_list(url, version_id)

    @exception_handler
    def app_rule_sort(self, app_id, app_rule_ids):
        """

        Update order of app rule

        :param app_id: Id of the App
        :type app_id: int

        :param app_rule_ids: ordered list of app_rule_ids
        :type app_rule_ids: list

        Returns the list of processed app rule ids
        :return: app_rule_id list
        :rtype: list[int]

        See https://developers.onelogin.com/api-docs/2/app-rules/bulk-sort Bulk Sort documentation
        """
        self.clean_error()

        version_id = self.get_version_id("APP_RULE_SORT_URL")
        url = self.get_url(Constants.APP_RULE_SORT_URL, app_id, version_id=version_id)

        return self.set_operation(url, app_rule_ids, version_id)

    # Role Methods
    @exception_handler
    def get_roles(self, query_parameters=None, max_results=None):
        """

        Gets a list of Role resources.

        :param query_parameters: Parameters to filter the result of the list
        :type query_parameters: dict

        :param max_results: Limit the number of roles returned (optional)
        :type max_results: int

        Returns the list of roles
        :return: role list
        :rtype: list[Role]

        See https://developers.onelogin.com/api-docs/1/roles/get-roles Get Roles documentation
            https://developers.onelogin.com/api-docs/2/roles/list-roles
        """
        self.clean_error()

        version_id = self.get_version_id("GET_ROLES_URL")
        url = self.get_url(Constants.GET_ROLES_URL, version_id=version_id)

        return self.retrieve_resources(Role, url, query_parameters, max_results, version_id)

    @exception_handler
    def create_role(self, role_params):
        """

        Create a role

        :param role_params: Role data (name, apps, users, admins)
        :type role_params: dict

        Returns the role id
        :return: role
        :rtype: int

        See https://developers.onelogin.com/api-docs/2/roles/create-role Create Role documentation
        """
        self.clean_error()

        version_id = self.get_version_id("CREATE_ROLE_URL")
        url = self.get_url(Constants.CREATE_ROLE_URL, version_id=version_id)

        return self.create_resource(Role, url, role_params, None, version_id)

    @exception_handler
    def get_role(self, role_id):
        """

        Gets Role by ID.

        :param role_id: Id of the Role
        :type role_id: int

        Returns the role identified by the id
        :return: role
        :rtype: Role

        See https://developers.onelogin.com/api-docs/1/roles/get-role-by-id Get Role by ID documentation
            https://developers.onelogin.com/api-docs/2/roles/get-role
        """
        self.clean_error()

        version_id = self.get_version_id("GET_ROLE_URL")
        url = self.get_url(Constants.GET_ROLE_URL, role_id, version_id=version_id)

        return self.retrieve_resource(Role, url, version_id)

    @exception_handler
    def update_role(self, role_id, role_params):
        """

        Updates a role

        :param role_id: Id of the role
        :type role_id: int

        :param role_params: Role data (name)
        :type role_params: dict

        Returns the role id of the modified role
        :return: role_id
        :rtype: int

        See https://developers.onelogin.com/api-docs/2/roles/update-role Update Role by ID documentation
        """
        self.clean_error()

        version_id = self.get_version_id("UPDATE_ROLE_URL")
        url = self.get_url(Constants.UPDATE_ROLE_URL, role_id, version_id=version_id)

        return self.update_resource(Role, url, role_params, None, version_id)

    @exception_handler
    def get_role_apps(self, role_id, assigned=True, max_results=None):
        """

        Gets a list of App assigned to a role.

        :param role_id: Id of the role
        :type role_id: int

        :param assigned: Defaults to true. Returns all apps assigned to the role, or the opposite (optional)
        :type assigned: bool

        :param max_results: Limit the number of apps returned (optional)
        :type max_results: int

        Returns a list of App assigned to a role.
        :return: app list
        :rtype: list[App]

        See https://developers.onelogin.com/api-docs/2/roles/get-role-apps Get Role Apps documentation

        """
        self.clean_error()

        version_id = self.get_version_id("GET_ROLE_APPS_URL")
        url = self.get_url(Constants.GET_ROLE_APPS_URL, role_id, version_id=version_id)

        query_parameters = None
        if assigned is False:
            query_parameters = {"assigned": False}

        return self.retrieve_resources(App, url, query_parameters, max_results, version_id)

    @exception_handler
    def set_role_apps(self, role_id, app_ids, max_results=None):
        """

        Assign applications to a role.

        :param role_id: Id of the role
        :type role_id: int

        :param app_ids: List of app ids
        :type app_ids: integer array

        Returns a list of App assigned to a role.
        :return: app id list
        :rtype: list[int]

        See https://developers.onelogin.com/api-docs/2/roles/set-role-apps Set Role Apps documentation

        """

        self.clean_error()

        version_id = self.get_version_id("SET_ROLE_APPS_URL")
        url = self.get_url(Constants.SET_ROLE_APPS_URL, role_id, version_id=version_id)

        return self.set_operation(url, app_ids, version_id)

    @exception_handler
    def get_role_users(self, role_id, name=None, include_unassigned=None, max_results=None):
        """

        Gets a list of role users.

        :param role_id: Id of the role
        :type role_id: int

        :param name: Filters on first name, last name, username, and email address. (optional)
        :type name: string

        :param include_unassigned: Include admins that aren't assigned to the role. (optional)
        :type include_unassigned: bool

        :param max_results: Limit the number of users returned (optional)
        :type max_results: int

        Returns a list of AssignedUser of a role.
        :return: app list
        :rtype: list[AssignedUser]

        See https://developers.onelogin.com/api-docs/2/roles/get-role-users Get Role Users documentation

        """
        self.clean_error()

        version_id = self.get_version_id("GET_ROLE_USERS_URL")
        url = self.get_url(Constants.GET_ROLE_USERS_URL, role_id, version_id=version_id)

        query_parameters = None
        if include_unassigned is True or name:
            query_parameters = {}
            if name:
                query_parameters["name"] = name

            if include_unassigned is True:
                query_parameters["include_unassigned"] = "true"

        return self.retrieve_resources(AssignedUser, url, query_parameters, max_results, version_id)

    @exception_handler
    def add_role_users(self, role_id, user_ids):
        """

        Add users to a role.

        :param role_id: Id of the role
        :type role_id: int

        :param user_ids: List of user ids
        :type user_ids: integer array

        Returns a list of ids of the assigned users to a role.
        :return: user id list
        :rtype: list[int]

        See https://developers.onelogin.com/api-docs/2/roles/add-role-users Add Role Users documentation

        """

        self.clean_error()

        version_id = self.get_version_id("ADD_ROLE_USERS_URL")
        url = self.get_url(Constants.ADD_ROLE_USERS_URL, role_id, version_id=version_id)

        return self.add_to_resource_operation(url, user_ids, version_id)

    @exception_handler
    def remove_role_users(self, role_id, user_ids):
        """

        Remove users from a role.

        :param role_id: Id of the role
        :type role_id: int

        :param user_ids: List of admin ids
        :type user_ids: integer array

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/2/roles/remove-role-users Remove Role Users documentation

        """

        self.clean_error()

        version_id = self.get_version_id("REMOVE_ROLE_USERS_URL")
        url = self.get_url(Constants.REMOVE_ROLE_USERS_URL, role_id, version_id=version_id)

        return self.remove_from_resource_operation(url, user_ids, version_id)

    @exception_handler
    def get_role_admins(self, role_id, name=None, include_unassigned=None, max_results=None):
        """

        Gets a list of role administrators.

        :param role_id: Id of the role
        :type role_id: int

        :param name: Filters on first name, last name, username, and email address. (optional)
        :type name: string

        :param include_unassigned: Include admins that aren't assigned to the role. (optional)
        :type include_unassigned: bool

        :param max_results: Limit the number of admins returned (optional)
        :type max_results: int

        Returns a list of AssignedAdmin of a role.
        :return: app list
        :rtype: list[AssignedAdmin]

        See https://developers.onelogin.com/api-docs/2/roles/get-role-admins Get Role Admins documentation

        """
        self.clean_error()

        version_id = self.get_version_id("GET_ROLE_ADMINS_URL")
        url = self.get_url(Constants.GET_ROLE_ADMINS_URL, role_id, version_id=version_id)

        query_parameters = None
        if include_unassigned is True or name:
            query_parameters = {}
            if name:
                query_parameters["name"] = name

            if include_unassigned is True:
                query_parameters["include_unassigned"] = "true"

        return self.retrieve_resources(AssignedAdmin, url, query_parameters, max_results, version_id)

    @exception_handler
    def add_role_admins(self, role_id, admin_ids):
        """

        Add admins to a role.

        :param role_id: Id of the role
        :type role_id: int

        :param admin_ids: List of admin ids
        :type admin_ids: integer array

        Returns a list of ids of the assigned admins to a role.
        :return: admin id list
        :rtype: list[int]

        See https://developers.onelogin.com/api-docs/2/roles/add-role-admins Add Role Admins documentation

        """

        self.clean_error()

        version_id = self.get_version_id("ADD_ROLE_ADMINS_URL")
        url = self.get_url(Constants.ADD_ROLE_ADMINS_URL, role_id, version_id=version_id)

        return self.add_to_resource_operation(url, admin_ids, version_id)

    @exception_handler
    def remove_role_admins(self, role_id, admin_ids):
        """

        Remove admins from a role.

        :param role_id: Id of the role
        :type role_id: int

        :param admin_ids: List of admin ids
        :type admin_ids: integer array

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/2/roles/remove-role-admins Remove Role Admins documentation

        """

        self.clean_error()

        version_id = self.get_version_id("REMOVE_ROLE_ADMINS_URL")
        url = self.get_url(Constants.REMOVE_ROLE_ADMINS_URL, role_id, version_id=version_id)

        return self.remove_from_resource_operation(url, admin_ids, version_id)

    @exception_handler_return_false
    def delete_role(self, role_id):
        """

        Deletes a role

        :param role_id: Id of the role to be deleted
        :type role_id: int

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/2/roles/update-role Delete Role by ID documentation

        """
        self.clean_error()

        version_id = self.get_version_id("DELETE_ROLE_URL")
        url = self.get_url(Constants.DELETE_ROLE_URL, role_id, version_id=version_id)

        return self.delete_resource(url, version_id)

    # Event Methods
    @exception_handler
    def get_event_types(self):
        """

        List of all OneLogin event types available to the Events API.

        Returns the list of event type
        :return: event type list
        :rtype: list[EventType]

        See https://developers.onelogin.com/api-docs/1/events/event-types Get Event Types documentation

        """
        self.clean_error()

        version_id = self.get_version_id("GET_EVENT_TYPES_URL")
        url = self.get_url(Constants.GET_EVENT_TYPES_URL, version_id=version_id)

        return self.retrieve_resource_list(EventType, url, None, None, version_id)

    @exception_handler
    def get_events(self, query_parameters=None, max_results=None):
        """

        Gets a list of Event resources.

        :param query_parameters: Parameters to filter the result of the list
        :type query_parameters: dict

        :param max_results: Limit the number of events returned (optional)
        :type max_results: int

        Returns the list of events
        :return: event list
        :rtype: list[Event]

        See https://developers.onelogin.com/api-docs/1/events/get-events Get Events documentation

        """
        self.clean_error()

        version_id = self.get_version_id("GET_EVENTS_URL")
        url = self.get_url(Constants.GET_EVENTS_URL, version_id=version_id)

        return self.retrieve_resources(Event, url, query_parameters, max_results, version_id)

    @exception_handler
    def get_event(self, event_id):
        """

        Gets Event by ID.

        :param role_id: Id of the Event
        :type role_id: int

        Returns the result of the operation
        :return: event
        :rtype: Event

        See https://developers.onelogin.com/api-docs/1/events/get-event-by-id Get Event by ID documentation

        """
        self.clean_error()

        version_id = self.get_version_id("GET_EVENT_URL")
        url = self.get_url(Constants.GET_EVENT_URL, event_id, version_id=version_id)

        return self.retrieve_resource(Event, url, version_id)

    @exception_handler_return_false
    def create_event(self, event_params):
        """

        Create an event in the OneLogin event log.

        :param event_params: Event data (event_type_id, account_id, actor_system,
                                         actor_user_id, actor_user_name, app_id,
                                         assuming_acting_user_id, custom_message,
                                         directory_sync_run_id, group_id, group_name,
                                         ipaddr, otp_device_id, otp_device_name,
                                         policy_id, policy_name, role_id, role_name,
                                         user_id, user_name)
        :type event_params: dict

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/events/create-event Create Event documentation

        """
        self.clean_error()
        self.prepare_token()

        version_id = self.get_version_id("CREATE_EVENT_URL")
        url = self.get_url(Constants.CREATE_EVENT_URL, version_id=version_id)

        return self.create_operation(url, event_params)

    # Group Methods
    @exception_handler
    def get_groups(self, max_results=None):
        """

        Gets a list of Group resources (element of groups limited with the max_results parameter, or client attribute).

        :param max_results: Limit the number of groups returned (optional)
        :type max_results: int

        Returns the list of groups
        :return: group list
        :rtype: list[Group]

        See https://developers.onelogin.com/api-docs/1/groups/get-groups Get Groups documentation

        """
        self.clean_error()

        version_id = self.get_version_id("GET_GROUPS_URL")
        url = self.get_url(Constants.GET_GROUPS_URL, version_id=version_id)

        return self.retrieve_resources(Group, url, None, max_results, version_id)

    @exception_handler
    def get_group(self, group_id):
        """

        Gets Group by ID.

        :param role_id: Id of the group
        :type role_id: int

        Returns the group identified by the id
        :return: group
        :rtype: Group

        See https://developers.onelogin.com/api-docs/1/groups/get-group-by-id Get Group by ID documentation

        """
        self.clean_error()

        version_id = self.get_version_id("GET_GROUP_URL")
        url = self.get_url(Constants.GET_GROUP_URL, group_id, version_id=version_id)

        return self.retrieve_resource(Group, url, version_id)

    # SAML Assertion Methods
    @exception_handler
    def get_saml_assertion(self, username_or_email, password, app_id, subdomain, ip_address=None):
        """

        Generates a SAML Assertion.

        :param username_or_email: username or email of the OneLogin user accessing the app
        :type username_or_email: string

        :param password: Password of the OneLogin user accessing the app
        :type password: string

        :param app_id: App ID of the app for which you want to generate a SAML token
        :type app_id: integer

        :param subdomain: subdomain of the OneLogin account related to the user/app
        :type subdomain: string

        :param ip_address: whitelisted IP address that needs to be bypassed (some MFA scenarios).
        :type ip_address: string

        Returns a SAMLEndpointResponse object with an encoded SAMLResponse
        :return: true if success
        :rtype: SAMLEndpointResponse

        See https://developers.onelogin.com/api-docs/1/saml-assertions/generate-saml-assertion Generate SAML Assertion documentation
            https://developers.onelogin.com/api-docs/2/saml-assertions/generate-saml-assertion
        """
        self.clean_error()

        version_id = self.get_version_id("GET_SAML_ASSERTION_URL")
        url = self.get_url(Constants.GET_SAML_ASSERTION_URL, version_id=version_id)

        data = {
            'username_or_email': username_or_email,
            'password': password,
            'app_id': app_id,
            'subdomain': subdomain,
        }

        if ip_address:
            data['ip_address'] = ip_address

        return self.retrieve_saml_assertion(url, data, version_id)

    @exception_handler
    def get_saml_assertion_verifying(self, app_id, device_id, state_token, otp_token=None, url_endpoint=None, do_not_notify=False):
        """

        Verify a one-time password (OTP) value provided for a second factor when multi-factor authentication (MFA) is required for SAML authentication.

        :param app_id: App ID of the app for which you want to generate a SAML token
        :type app_id: integer

        :param devide_id: Provide the MFA device_id you are submitting for verification.
        :type subdomain: integer

        :param state_token: Provide the state_token associated with the MFA device_id you are submitting for verification.
        :type state_token: string

        :param otp_token: Provide the OTP value for the MFA factor you are submitting for verification.
        :type otp_token: string

        :param url_endpoint: Specify an url where return the response.
        :type url_endpoint: string

        :param do_not_notify: When verifying MFA via Protect Push, set this to true to stop additional push notifications being sent to the OneLogin Protect device
        :type do_not_notify: bool

        Returns a SAMLEndpointResponse object with an encoded SAMLResponse
        :return: true if success
        :rtype: SAMLEndpointResponse

        See https://developers.onelogin.com/api-docs/1/saml-assertions/verify-factor Verify Factor documentation
            https://developers.onelogin.com/api-docs/2/saml-assertions/verify-factor
        """
        self.clean_error()

        if url_endpoint:
            url = url_endpoint
        else:
            version_id = self.get_version_id("GET_SAML_VERIFY_FACTOR")
            url = self.get_url(Constants.GET_SAML_VERIFY_FACTOR, version_id=version_id)

        data = {
            'app_id': int(app_id),
            'device_id': str(device_id),
            'state_token': str(state_token),
            'do_not_notify': do_not_notify
        }

        if otp_token:
            data['otp_token'] = otp_token

        return self.retrieve_saml_assertion(url, data, version_id)

    # Multi-factor Auth Methods
    @exception_handler
    def get_factors(self, user_id):
        """

        Returns a list of authentication factors that are available for user enrollment via API.

        :param user_id: Set to the id of the user.
        :type user_id: integer

        :return: AuthFactor list
        :rtype: list[AuthFactor]

        See https://developers.onelogin.com/api-docs/1/multi-factor-authentication/available-factors Get Available Authentication Factors documentation
            https://developers.onelogin.com/api-docs/2/multi-factor-authentication/available-factors
        """
        self.clean_error()

        version_id = self.get_version_id("GET_FACTORS_URL")
        index = None
        if version_id == 1:
            index = 'auth_factors'
            url = self.get_url(Constants.GET_FACTORS_URL, user_id, version_id=version_id)
        else:
            url = self.get_url(Constants.V2_GET_FACTORS_URL, user_id, version_id=version_id)

        return self.retrieve_resource_list(AuthFactor, url, None, index, version_id)

    @exception_handler
    def enroll_factor(self, user_id, factor_id, display_name, number=None, verified=False, expires_in=None, custom_message=None):
        """

        Enroll a user with a given authentication factor.

        :param user_id: Set to the id of the user.
        :type user_id: integer

        :param factor_id: The identifier of the factor to enroll the user with.
        :type factor_id: integer

        :param display_name: A name for the users device.
        :type display_name: string

        :param number: The phone number of the user in E.164 format.. (V1 only)
        :type number: string

        :param verified: Default false. Pre-verified and can be immediately activated.
                                        (OL Voice requires verified = true)
        :type number: bool

        :param expires_in: Default 120. Valid range 120-900  (V2 Only)
        :type number: int

        :param custom_message: Only applies to SMS factor (V2 only)
        : type custom_message: string

        :return: MFA device
        :rtype: OTP_Device

        See https://developers.onelogin.com/api-docs/1/multi-factor-authentication/enroll-factor Enroll an Authentication Factor documentation
            https://developers.onelogin.com/api-docs/2/multi-factor-authentication/enroll-factor
        """
        self.clean_error()

        version_id = self.get_version_id("ENROLL_FACTOR_URL")
        if version_id == 1:
            url = self.get_url(Constants.ENROLL_FACTOR_URL, user_id, version_id=version_id)

            if custom_message is not None:
                raise Exception("custom_message parameter not available on /1")
            if expires_in is not None:
                raise Exception("expires_in parameter not available on /1")
        else:
            url = self.get_url(Constants.V2_ENROLL_FACTOR_URL, user_id, version_id=version_id)
            if number is not None:
                raise Exception("number parameter not available on /2")

        data = {
            'factor_id': int(factor_id),
            'display_name': display_name,
            'verified': verified
        }
        if number is not None:
            data["number"] = number
        if custom_message is not None:
            data["custom_message"] = custom_message
        if expires_in is not None:
            data["expires_in"] = expires_in

        return self.create_resource(OTP_Device, url, data, None, version_id)

    @exception_handler
    def verify_enroll_factor_otp(self, user_id, registration_id, otp):
        """

        Verify enrollment for OneLogin SMS, OneLogin Email, OneLogin Protect and Authenticator authentication factors.

        :param user_id: Set to the id of the user.
        :type user_id: integer

        :param registration_id: uuid of the registration process (enroll factor)
        :type registration_id: string

        :param otp: One-Time-Password
        :type otp: string


        :return: Enrollment status
        :rtype: MFACheckStatus

        See https://developers.onelogin.com/api-docs/2/multi-factor-authentication/enroll-factor-verify-otp Verify Enrollment of Authentication Factors documentation
        """
        self.clean_error()

        version_id = self.get_version_id("VERIFY_ENROLLMENT_SMS_EMAIL_PROTECT_AUTH_URL")
        url = self.get_url(Constants.VERIFY_ENROLLMENT_SMS_EMAIL_PROTECT_AUTH_URL, user_id, registration_id, version_id=version_id)

        data = {
            'otp': otp
        }

        return self.update_resource(MFACheckStatus, url, data, None, version_id)

    @exception_handler
    def verify_enroll_factor_poll(self, user_id, registration_id):
        """

        Verify enrollment for OneLogin Voice & Protect Push authentication factors.

        :param user_id: Set to the id of the user.
        :type user_id: integer

        :param registration_id: uuid of the registration process (enroll factor)
        :type registration_id: string

        :return: Enrollment status
        :rtype: MFACheckStatus

        See https://developers.onelogin.com/api-docs/2/multi-factor-authentication/enroll-factor-verify-poll Verify Enrollment of OneLogin Voice & Protect documentation
        """
        self.clean_error()

        version_id = self.get_version_id("VERIFY_ENROLLMENT__PROTECTPUSH_VOICE_URL")
        url = self.get_url(Constants.VERIFY_ENROLLMENT__PROTECTPUSH_VOICE_URL, user_id, registration_id, version_id=version_id)

        return self.retrieve_resource(MFACheckStatus, url, version_id)

    @exception_handler
    def get_enrolled_factors(self, user_id):
        """

        Return a list of authentication factors registered to a particular user for multifactor authentication (MFA)

        :param user_id: Set to the id of the user.
        :type user_id: integer

        :return: OTP_Device list
        :rtype: list[OTP_Device]

        See https://developers.onelogin.com/api-docs/1/multi-factor-authentication/enrolled-factors Get Enrolled Authentication Factors documentation
            https://developers.onelogin.com/api-docs/2/multi-factor-authentication/enrolled-factors
        """
        self.clean_error()

        version_id = self.get_version_id("GET_ENROLLED_FACTORS_URL")
        index = None
        if version_id == 1:
            index = 'otp_devices'
            url = self.get_url(Constants.GET_ENROLLED_FACTORS_URL, user_id, version_id=version_id)
        else:
            url = self.get_url(Constants.V2_GET_ENROLLED_FACTORS_URL, user_id, version_id=version_id)

        return self.retrieve_resource_list(OTP_Device, url, None, index, version_id)

    @exception_handler
    def activate_factor(self, user_id, device_id, expires_in=None, custom_message=None):
        """

        Triggers an SMS or Push notification containing a One-Time Password (OTP)
        that can be used to authenticate a user with the Verify Factor call.

        :param user_id: Set to the id of the user.
        :type user_id: integer

        :param device_id: Set to the device_id of the MFA device.
        :type device_id: integer

        :param expires_in: Default 120. Valid range 120-900  (V2 Only)
        :type number: int

        :param custom_message: Only applies to SMS factor (V2 only)
        : type custom_message: string

        :return: Info with User Id, Device Id, and otp_device
        :rtype: FactorEnrollmentResponse

        See https://developers.onelogin.com/api-docs/1/multi-factor-authentication/activate-factor Activate an Authentication Factor documentation
            https://developers.onelogin.com/api-docs/1/multi-factor-authentication/activate-factor
        """
        self.clean_error()

        version_id = self.get_version_id("ACTIVATE_FACTOR_URL")
        data = None
        if version_id == 1:
            url = self.get_url(Constants.ACTIVATE_FACTOR_URL, user_id, device_id, version_id=version_id)
            if custom_message is not None:
                raise Exception("custom_message parameter not available on /1")
            if expires_in is not None:
                raise Exception("expires_in parameter not available on /1")
        else:
            url = self.get_url(Constants.V2_ACTIVATE_FACTOR_URL, user_id, version_id=version_id)
            data = {"device_id": device_id}
            if custom_message is not None:
                data["custom_message"] = custom_message
            if expires_in is not None:
                data["expires_in"] = expires_in

        return self.create_resource(FactorEnrollmentResponse, url, data, None, version_id)

    @exception_handler_return_false
    def verify_factor(self, user_id, device_id, otp_token=None, state_token=None):
        """

        Authenticates a one-time password (OTP) code provided by a multifactor authentication (MFA) device.

        :param user_id: Set to the id of the user.
        :type user_id: integer

        :param device_id: Set to the device_id of the MFA device.
        :type device_id: integer

        :param otp_token: OTP code provided by the device or SMS message sent to user.
                          When a device like OneLogin Protect that supports Push has
                          been used you do not need to provide the otp_token.
        :type otp_token: string

        :param state_token: The state_token is returned after a successful request
                            to Enroll a Factor or Activate a Factor.
                            MUST be provided if the needs_trigger attribute from
                            the proceeding calls is set to true.
        :type state_token: string

        :return: true if action succeed
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/multi-factor-authentication/verify-factor Verify an Authentication Factor documentation

        """
        self.clean_error()

        version_id = self.get_version_id("VERIFY_FACTOR_URL")
        url = self.get_url(Constants.VERIFY_FACTOR_URL, user_id, device_id, version_id=version_id)

        data = {}
        if otp_token:
            data['otp_token'] = otp_token
        if state_token:
            data['state_token'] = state_token

        return self.create_operation(url, data)

    @exception_handler
    def verify_factor_otp(self, user_id, verification_id, otp, device_id=None):
        """

        Verify an OTP code provided by SMS, Email, OneLogin Protect or Authenticator

        :param user_id: Set to the id of the user.
        :type user_id: integer

        :param verification_id: uuid of the verification process (activate factor)
        :type verification_id: string

        :param otp: One-Time-Password
        :type otp: string

        :param device_id: The device_id of the enrolled factors (No required on OL SMS and OL Email)
        :type device_id: int

        :return: Enrollment status
        :rtype: MFACheckStatus

        See https://developers.onelogin.com/api-docs/2/multi-factor-authentication/verify-factor Verify an Authentication Factor documentation
        """
        self.clean_error()

        version_id = self.get_version_id("VERIFY_FACTOR_SMS_EMAIL_PROTECT_AUTH_URL")
        url = self.get_url(Constants.VERIFY_FACTOR_SMS_EMAIL_PROTECT_AUTH_URL, user_id, verification_id, version_id=version_id)

        data = {
            'otp': otp
        }
        if device_id is not None:
            data["device_id"] = int(device_id)

        return self.update_operation(url, data)

    @exception_handler
    def verify_factor_poll(self, user_id, verification_id):
        """

        Verify completion of OneLogin Push or OneLogin Voice factors.

        :param user_id: Set to the id of the user.
        :type user_id: integer

        :param verification_id: uuid of the verification process (activate factor)
        :type verification_id: string

        :return: Enrollment status
        :rtype: MFACheckStatus

        See https://developers.onelogin.com/api-docs/2/multi-factor-authentication/verify-factor-poll Verify an Authentication Factor documentation
        """
        self.clean_error()

        version_id = self.get_version_id("VERIFY_FACTOR_PROTECTPUSH_VOICE_URL")
        url = self.get_url(Constants.VERIFY_FACTOR_PROTECTPUSH_VOICE_URL, user_id, verification_id, version_id=version_id)

        return self.retrieve_resource(MFACheckStatus, url, version_id)

    @exception_handler_return_false
    def remove_factor(self, user_id, device_id):
        """

        Remove an enrolled factor from a user.

        :param user_id: Set to the id of the user.
        :type user_id: integer

        :param device_id: The device_id of the MFA device.
        :type device_id: integer

        :return: true if action succeed
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/multi-factor-authentication/remove-factor Remove a Factor documentation
            https://developers.onelogin.com/api-docs/2/multi-factor-authentication/remove-factor
        """
        self.clean_error()

        version_id = self.get_version_id("DELETE_FACTOR_URL")
        if version_id == 1:
            url = self.get_url(Constants.DELETE_FACTOR_URL, user_id, device_id, version_id=version_id)
        else:
            url = self.get_url(Constants.V2_DELETE_FACTOR_URL, user_id, device_id, version_id=version_id)

        return self.delete_resource(url, version_id)

    # Invite Links Methods
    @exception_handler
    def generate_invite_link(self, email):
        """

        Generates an invite link for a user that you have already created in your OneLogin account.

        :param email: Set to the email address of the user that you want to generate an invite link for.
        :type email: string

        Returns the invitation link
        :return: link
        :rtype: str

        See https://developers.onelogin.com/api-docs/1/invite-links/generate-invite-link Generate Invite Link documentation

        """
        self.clean_error()

        version_id = self.get_version_id("GENERATE_INVITE_LINK_URL")
        url = self.get_url(Constants.GENERATE_INVITE_LINK_URL, version_id=version_id)

        data = {
            'email': email
        }

        response = self.execute_call('post', url, json=data)
        if response.status_code == 200:
            json_data = response.json()
            if json_data and json_data.get('data', None):
                return json_data['data'][0]
        else:
            self.set_error(response)

    @exception_handler_return_false
    def send_invite_link(self, email, personal_email=None):
        """

        Sends an invite link to a user that you have already created in your OneLogin account.

        :param email: Set to the email address of the user that you want to send an invite link for.
        :type email: string

        :param personal_email: If you want to send the invite email to an email other than the
                               one provided in email, provide it here. The invite link will be
                               sent to this address instead.
        :type personal_email: string

        Returns the result of the operation
        :return: True if the mail with the link was sent
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/invite-links/send-invite-link Send Invite Link documentation

        """
        self.clean_error()

        version_id = self.get_version_id("SEND_INVITE_LINK_URL")
        url = self.get_url(Constants.SEND_INVITE_LINK_URL, version_id=version_id)

        data = {
            'email': email
        }

        if personal_email:
            data['personal_email'] = personal_email

        return self.create_operation(url, data)

    # Embed Apps Method
    @exception_handler
    def get_embed_apps(self, token, email):
        """

        Lists apps accessible by a OneLogin user.

        :param token: Provide your embedding token.
        :type token: string

        :param email: Provide the email of the user for which you want to return a list of embeddable apps.
        :type email: string

        Returns the embed apps
        :return: A list of Apps
        :rtype: list[App]

        See https://developers.onelogin.com/api-docs/1/embed-apps/get-apps-to-embed-for-a-user Get Apps to Embed for a User documentation

        """
        self.clean_error()

        url = Constants.EMBED_APP_URL

        data = {
            'token': token,
            'email': email
        }

        headers = {
            'User-Agent': self.user_agent
        }

        response = requests.get(url, headers=headers, params=data)
        if response.status_code == 200 and response.content:
            return retrieve_apps_from_xml(EmbedApp, response.content)
        else:
            self.error = str(response.status_code)
            if response.content:
                self.error_description = response.content

    # Brand Methods
    @exception_handler
    def get_brands(self, query_parameters=None, max_results=None):
        """

        Get a list of account brands

        :param query_parameters: Parameters to filter the result of the list
        :type query_parameters: dict

        :param max_results: Limit the number of brands returned (optional)
        :type max_results: int

        Returns the list of brands
        :return: brand list
        :rtype: list[Brand]

        See https://developers.onelogin.com/api-docs/2/branding/list-account-brands List Account Brands documentation

        """
        self.clean_error()

        version_id = self.get_version_id("GET_ACCOUNT_BRANDS_URL")
        url = self.get_url(Constants.GET_ACCOUNT_BRANDS_URL, version_id=version_id)

        return self.retrieve_resources(Brand, url, query_parameters, max_results, version_id)

    @exception_handler
    def create_brand(self, brand_params):
        """

        Creates accound brand

        :param brand_params: Brand data (name, enabled, custom_support_enabled, custom_color,
                                         custom_accent_color, custom_masking_color, custom_masking_opacity,
                                         enable_custom_label_for_login_screen, custom_label_text_for_login_screen,
                                         login_instruction_title, login_instruction, hide_onelogin_footer,
                                         mfa_enrollment_message, background, logo)
        :type brand_params: dict

        Returns the created brand
        :return: brand
        :rtype: Brand

        See https://developers.onelogin.com/api-docs/2/branding/create-account-brand Create Account Brand documentation
        """
        self.clean_error()

        version_id = self.get_version_id("CREATE_ACCOUNT_BRAND_URL")
        url = self.get_url(Constants.CREATE_ACCOUNT_BRAND_URL, version_id=version_id)

        return self.create_resource(Brand, url, brand_params, None, version_id)

    @exception_handler
    def get_brand(self, brand_id):
        """

        Gets Brand by ID.

        :param brand_id: Id of the brand
        :type brand_id: int

        Returns the brand identified by the id
        :return: brand
        :rtype: Brand

        See https://developers.onelogin.com/api-docs/2/branding/get-account-brand Get Account Brand documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_ACCOUNT_BRAND_URL")
        url = self.get_url(Constants.GET_ACCOUNT_BRAND_URL, brand_id, version_id=version_id)

        return self.retrieve_resource(Brand, url, version_id)

    @exception_handler
    def update_brand(self, brand_id, brand_params):
        """

        Updates accound brand

        :param brand_id: Id of the brand
        :type brand_id: int

        :param brand_params: Brand data (name, enabled, custom_support_enabled, custom_color,
                                         custom_accent_color, custom_masking_color, custom_masking_opacity,
                                         enable_custom_label_for_login_screen, custom_label_text_for_login_screen,
                                         login_instruction_title, login_instruction, hide_onelogin_footer,
                                         mfa_enrollment_message, background, logo)
        :type brand_params: dict

        Returns the modified brand
        :return: brand
        :rtype: Brand

        See https://developers.onelogin.com/api-docs/2/branding/update-account-brand Update Account Brand documentation
        """
        self.clean_error()

        version_id = self.get_version_id("UPDATE_ACCOUNT_BRAND_URL")
        url = self.get_url(Constants.UPDATE_ACCOUNT_BRAND_URL, brand_id, version_id=version_id)

        return self.update_resource(Brand, url, brand_params, None, version_id)

    @exception_handler_return_false
    def delete_brand(self, brand_id):
        """

        Deletes Account Brand

        :param brand_id: Id of the brand to be deleted
        :type brand_id: int

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/2/branding/delete-account-brand Deletes Account Brand documentation

        """
        self.clean_error()

        version_id = self.get_version_id("DELETE_ACCOUNT_BRAND_URL")
        url = self.get_url(Constants.DELETE_ACCOUNT_BRAND_URL, brand_id, version_id=version_id)

        return self.delete_resource(url, version_id)

    @exception_handler
    def get_brand_apps(self, brand_id, max_results=None):
        """

        Get Apps Associated with Account Brand.

        :param brand_id: Id of the brand
        :type brand_id: int

        :param max_results: Limit the number of apps returned (optional)
        :type max_results: int

        Returns a list of Apps of a brand.
        :return: app list
        :rtype: list[OneloginApp]

        See https://developers.onelogin.com/api-docs/2/branding/get-apps-associated-with-account-brand Get Apps Associated with Account Brand documentation

        """
        self.clean_error()

        version_id = self.get_version_id("GET_APPS_BRAND_URL")
        url = self.get_url(Constants.GET_APPS_BRAND_URL, brand_id, version_id=version_id)

        return self.retrieve_resources(OneLoginApp, url, None, max_results, version_id)

    @exception_handler
    def get_email_settings(self):
        """

        Get Email Settings Config


        Returns a dict with email settings
        :return: email_settings
        :rtype: dict

        See https://developers.onelogin.com/api-docs/2/branding/get-email-settings Get Email Settings Config documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_ACCOUNT_EMAIL_SETTINGS")
        url = self.get_url(Constants.GET_ACCOUNT_EMAIL_SETTINGS, version_id=version_id)

        response = self.execute_call('get', url)
        if response.status_code == 200:
            return response.json()
        else:
            self.set_error(response)

    @exception_handler
    def update_email_settings(self, email_settings):
        """

        Update Email Settings Config

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/2/branding/update-email-settings Update Email Settings Config documentation
        """
        self.clean_error()

        version_id = self.get_version_id("UPDATE_ACCOUNT_EMAIL_SETTINGS")
        url = self.get_url(Constants.UPDATE_ACCOUNT_EMAIL_SETTINGS, version_id=version_id)

        return self.update_operation(url, email_settings)

    @exception_handler
    def reset_email_settings(self):
        """

        Reset Email Settings Config

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/2/branding/reset-email-settings Reset Email Settings Config documentation
        """
        self.clean_error()

        version_id = self.get_version_id("UPDATE_ACCOUNT_EMAIL_SETTINGS")
        url = self.get_url(Constants.UPDATE_ACCOUNT_EMAIL_SETTINGS, version_id=version_id)

        # version 1 status code
        return self.delete_resource(url, 1)

    # Smart Hooks Methods
    @exception_handler
    def get_smart_hooks(self, query_parameters=None, max_results=None):
        """

        Gets a list of hooks.

        :param query_parameters: Parameters to filter the result of the list
        :type query_parameters: dict

        :param max_results: Limit the number of smart hooks returned (optional)
        :type max_results: int

        Returns the list of smart hooks
        :return: smart hooks list
        :rtype: list[SmartHook]

        See https://developers.onelogin.com/api-docs/2/hooks/list-hooks List Hooks documentation

        """
        self.clean_error()

        version_id = self.get_version_id("GET_HOOKS_URL")
        url = self.get_url(Constants.GET_HOOKS_URL, version_id=version_id)

        return self.retrieve_resource_list(SmartHook, url, query_parameters, max_results, version_id)

    @exception_handler
    def create_smart_hook(self, smart_hook_params):
        """

        Creates a hook

        :param smart_hook_params: Smart Hook data (type, disabled, timeout, env_vars,
                                                   runtime, context_version, retries,
                                                   risk_enabled, mfa_device_info_enabled,
                                                   location_enabled, packages, function)
        :type smart_hook_params: dict

        Returns the created hook
        :return: smart_hook
        :rtype: SmartHook

        See https://developers.onelogin.com/api-docs/2/hooks/create-hook Create a Hook documentation
        """
        self.clean_error()

        version_id = self.get_version_id("CREATE_HOOK_URL")
        url = self.get_url(Constants.CREATE_HOOK_URL, version_id=version_id)

        return self.create_resource(SmartHook, url, smart_hook_params, None, version_id)

    @exception_handler
    def get_smart_hook(self, smart_hook_id):
        """

        Gets Smart Hook

        :param smart_hook_id: Id of the smart_hook
        :type smart_hook_id: string

        Returns the requested smart_hook
        :return: smart_hook
        :rtype: SmartHook

        See https://developers.onelogin.com/api-docs/2/smart-hooks/get-hook Get a Hook documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_HOOK_URL")
        url = self.get_url(Constants.GET_HOOK_URL, smart_hook_id, version_id=version_id)

        return self.retrieve_resource(SmartHook, url, version_id)

    @exception_handler
    def update_smart_hook(self, smart_hook_id, smart_hook_params):
        """

        Updates a hook

        :param smart_hook_id: Id of the smart hook
        :type smart_hook_id: int

        :param smart_hook_params: Smart Hook data (type, disabled, timeout, env_vars,
                                                   runtime, context_version, retries,
                                                   risk_enabled, mfa_device_info_enabled,
                                                   location_enabled, packages, function)
        :type smart_hook_params: dict

        Returns the modified hook
        :return: smart_hook
        :rtype: SmartHook

        See https://developers.onelogin.com/api-docs/2/hooks/update-hook Update a Hook documentation
        """
        self.clean_error()

        version_id = self.get_version_id("UPDATE_HOOK_URL")
        url = self.get_url(Constants.UPDATE_HOOK_URL, smart_hook_id, version_id=version_id)

        return self.update_resource(SmartHook, url, smart_hook_params, None, version_id)

    @exception_handler
    def delete_smart_hook(self, smart_hook_id):
        """

        Deletes a hook

        :param smart_hook_id: The id of the Smart Hook.
        :type smart_hook_id: string

        :return: true if action succeed
        :rtype: bool

        See https://developers.onelogin.com/api-docs/2/hooks/delete-hook Delete a Hook documentation
        """
        self.clean_error()

        version_id = self.get_version_id("UPDATE_HOOK_URL")
        url = self.get_url(Constants.UPDATE_HOOK_URL, smart_hook_id, version_id=version_id)

        return self.delete_resource(url, version_id)

    @exception_handler
    def get_smart_hook_logs(self, smart_hook_id, query_parameters=None, max_results=None):
        """

        Gets a list of smart hook logs.

        :param smart_hook_id: The id of the Smart Hook.
        :type smart_hook_id: string

        :param query_parameters: Parameters to filter the result of the list
        :type query_parameters: dict

        :param max_results: Limit the number of smart hook logs returned (optional)
        :type max_results: int

        Returns the list of smart hook logs
        :return: smart hook log list
        :rtype: list[SmartHookLog]

        See https://developers.onelogin.com/api-docs/2/hooks/get-hook-logs Get Hook Logs documentation

        """
        self.clean_error()

        version_id = self.get_version_id("GET_HOOK_LOGS_URL")
        url = self.get_url(Constants.GET_HOOK_LOGS_URL, smart_hook_id, version_id=version_id)

        return self.retrieve_resource_list(SmartHookLog, url, query_parameters, max_results, version_id)

    @exception_handler
    def get_env_vars(self, max_results=None):
        """

        Gets a list of environment variables.

        :param max_results: Limit the number of smart hooks returned (optional)
        :type max_results: int

        Returns the list of smart hooks
        :return: environment variables list
        :rtype: list[SmartHookEnv]

        See https://developers.onelogin.com/api-docs/2/hooks/list-environment-variables List Environment Variables documentation

        """
        self.clean_error()

        version_id = self.get_version_id("GET_HOOK_ENVS_URL")
        url = self.get_url(Constants.GET_HOOK_ENVS_URL, version_id=version_id)

        return self.retrieve_resource_list(SmartHookEnv, url, None, max_results, version_id)

    @exception_handler
    def create_env_var(self, env_var_params):
        """

        Creates an environment variable

        :param env_var_params: Smart Hook data (name, value)
        :type env_var_params: dict

        Returns the created environment variable
        :return: environment variable
        :rtype: SmartHookEnv

        See https://developers.onelogin.com/api-docs/2/hooks/create-environment-variable Create Environment Variable documentation
        """
        self.clean_error()

        version_id = self.get_version_id("CREATE_HOOK_ENV_URL")
        url = self.get_url(Constants.CREATE_HOOK_ENV_URL, version_id=version_id)

        return self.create_resource(SmartHookEnv, url, env_var_params, None, version_id)

    @exception_handler
    def get_env_var(self, env_var_id):
        """

        Return a single Smart Hook Environment Variable

        :param env_var_id: Id of the environment variable
        :type env_var_id: string

        Returns the requested environment variable
        :return: environment variable
        :rtype: SmartHookEnv

        See https://developers.onelogin.com/api-docs/2/hooks/get-environment-variable Get Environment Variable documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_HOOK_ENV_URL")
        url = self.get_url(Constants.GET_HOOK_ENV_URL, env_var_id, version_id=version_id)

        return self.retrieve_resource(SmartHookEnv, url, version_id)

    @exception_handler
    def update_env_var(self, env_var_id, value):
        """

        Updates an environment variable

        :param env_var_id: Id of the environment variable
        :type env_var_id: string

        :param env_var_params: Environment variable data (name, value)
        :type env_var_params: dict

        Returns the modified environment variable
        :return: environment variable
        :rtype: SmartHookEnv

        See https://developers.onelogin.com/api-docs/2/hooks/update-environment-variable Update Environment Variable documentation
        """
        self.clean_error()

        if type(value) is dict:
            env_var_params = value
        else:
            env_var_params = {
                "value": value
            }

        version_id = self.get_version_id("UPDATE_HOOK_ENV_URL")
        url = self.get_url(Constants.UPDATE_HOOK_ENV_URL, env_var_id, version_id=version_id)

        return self.update_resource(SmartHookEnv, url, env_var_params, None, version_id)

    @exception_handler
    def delete_env_var(self, env_var_id):
        """

        Deletes an environment variable

        :param env_var_id: Id of the environment variable
        :type env_var_id: string

        :return: true if action succeed
        :rtype: bool

        See https://developers.onelogin.com/api-docs/2/hooks/delete-environment-variable Delete Environment Variable documentation
        """
        self.clean_error()

        version_id = self.get_version_id("DELETE_HOOK_ENV_URL")
        url = self.get_url(Constants.DELETE_HOOK_ENV_URL, env_var_id, version_id=version_id)

        return self.delete_resource(url, version_id)

    # Smart MFA
    @exception_handler
    def validate_user(self, validate_user_params):
        """

        Validates a User

        :param validate_user_params: Smart MFA User data (user_identifier, email, phone, context, risk_threshold,
                                                          firstname, lastname, expires_in)
        :type validate_user_params: dict

        Returns a mfa validation response
        :return: smart_mfa
        :rtype: SmartMFA

        See https://developers.onelogin.com/api-docs/2/smart-mfa/validate-user Validate a User documentation
        """
        self.clean_error()

        version_id = self.get_version_id("SMART_MFA_VALIDATE_USER")
        url = self.get_url(Constants.SMART_MFA_VALIDATE_USER, version_id=version_id)

        return self.create_resource(SmartMFA, url, validate_user_params, None, version_id)

    @exception_handler
    def verify_token(self, state_token, otp_token):
        """

        Verify MFA Token

        :param state_token: The state_token value returned from the Validate a User endpoint
        :type state_token: string

        :param state_token: The MFA token that was sent to the user via Email or SMS using the Validate a User endpoint
        :type state_token: string

        :return: true if action succeed
        :rtype: bool

        See https://developers.onelogin.com/api-docs/2/smart-mfa/verify-token Verify MFA Token documentation
        """
        self.clean_error()

        version_id = self.get_version_id("SMART_MFA_VERFY_TOKEN")
        url = self.get_url(Constants.SMART_MFA_VERFY_TOKEN, version_id=version_id)

        data = {
            'state_token': state_token,
            'otp_token': otp_token
        }

        response = self.execute_call('post', url, json=data)

        if op_create_success(response.status_code):
            return True
        else:
            self.set_error(response)
        return False

    # Vigilance AI Methods
    @exception_handler
    def track_event(self, track_event_params):
        """

        Tracks an Event

        :param track_event_params: Event data (verb, ip, user_agent, user[id, name, authenticated],
                                         source[id,name], session[id], device[id], fp, published)
                             user id data needs to be in the format: {instance region}_{OneLogin User Id}
        :type track_event_params: dict

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/2/vigilance/train Track an Event documentation
        """
        self.clean_error()

        version_id = self.get_version_id("TRACK_EVENT_URL")
        url = self.get_url(Constants.TRACK_EVENT_URL, version_id=version_id)

        return self.submit_operation(url, track_event_params)

    @exception_handler
    def get_risk_score(self, track_event_params):
        """

        Gets a Risk Score

        :param track_event_params: Event data (verb, ip, user_agent, user[id, name, authenticated],
                                         source[id,name], session[id], device[id], fp, published)
                             user id data needs to be in the format: {instance region}_{OneLogin User Id}
        :type track_event_params: dict

        Returns the risk score
        :return: risk_score
        :rtype: RiskScore

        See https://developers.onelogin.com/api-docs/2/vigilance/verify Get a Risk Score documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_RISK_SCORE_URL")
        url = self.get_url(Constants.GET_RISK_SCORE_URL, version_id=version_id)

        return self.create_resource(RiskScore, url, track_event_params, None, version_id)

    @exception_handler
    def get_risk_rules(self):
        """

        Gets a list of risk rules.

        Returns the list of risk rules
        :return: risk rule list
        :rtype: list[RiskRule]

        See https://developers.onelogin.com/api-docs/2/vigilance/get-rules List Rules documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_RISK_RULES_URL")
        url = self.get_url(Constants.GET_RISK_RULES_URL, version_id=version_id)
        return self.retrieve_resources(RiskRule, url, None, None, version_id)

    @exception_handler
    def get_risk_rule(self, risk_rule_id):
        """

        Gets Risk Rule by ID.

        :param risk_rule_id: Id of the risk rule
        :type risk_rule_id: int

        Returns the risk rule identified by the id
        :return: risk_rule
        :rtype: RiskRule

        See https://developers.onelogin.com/api-docs/2/vigilance/get-rule Get a Rule documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_RISK_RULE_URL")
        url = self.get_url(Constants.GET_RISK_RULE_URL, risk_rule_id, version_id=version_id)

        return self.retrieve_resource(RiskRule, url, version_id)

    @exception_handler
    def create_risk_rule(self, risk_rule_params):
        """

        Creates a risk rule

        :param risk_rule_params: Risk Rule data (name, type, target, filters, source)
        :type risk_rule_params: dict

        Returns the created risk rule
        :return: risk_rule
        :rtype: RiskRule

        See https://developers.onelogin.com/api-docs/2/vigilance/create-rule Create a Rule documentation
        """
        self.clean_error()

        version_id = self.get_version_id("CREATE_RISK_RULE_URL")
        url = self.get_url(Constants.CREATE_RISK_RULE_URL, version_id=version_id)

        return self.create_resource(RiskRule, url, risk_rule_params, None, version_id)

    @exception_handler
    def update_risk_rule(self, risk_rule_id, risk_rule_params):
        """

        Updates a risk rule

        :param risk_rule_id: Id of the risk rule
        :type risk_rule_id: int

        :param risk_rule_params: Risk Rule data (name, type, target, filters, source)
        :type risk_rule_params: dict

        Returns the modified risk rule
        :return: risk_rule
        :rtype: RiskRule

        See https://developers.onelogin.com/api-docs/2/vigilance/update-rule Update a Rule documentation
        """
        self.clean_error()

        version_id = self.get_version_id("UPDATE_RISK_RULE_URL")
        url = self.get_url(Constants.UPDATE_RISK_RULE_URL, risk_rule_id, version_id=version_id)

        return self.update_resource(RiskRule, url, risk_rule_params, None, version_id)

    @exception_handler_return_false
    def delete_risk_rule(self, risk_rule_id):
        """

        Deletes a risk rule

        :param risk_rule_id: Id of the risk rule
        :type risk_rule_id: int

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/2/vigilance/delete-rule Delete a Rule documentation

        """
        self.clean_error()

        version_id = self.get_version_id("DELETE_RISK_RULE_URL")
        url = self.get_url(Constants.DELETE_RISK_RULE_URL, risk_rule_id, version_id=version_id)

        return self.delete_resource(url, version_id)

    @exception_handler
    def get_risk_score_insights(self, query_parameters=None):
        """

        Get Score Insights.

        :param query_parameters: Parameters to filter the result of the list
        :type query_parameters: dict

        Returns the risk score insight info
        :return: risk_score_insights
        :rtype: RiskScoreInsights

        See https://developers.onelogin.com/api-docs/2/vigilance/get-scores Get Score Insights documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_SCORE_INSIGHTS")
        url = self.get_url(Constants.GET_SCORE_INSIGHTS, version_id=version_id)

        return self.retrieve_resource(RiskScoreInsights, url, version_id)

    # User Mappings Methods
    @exception_handler
    def get_mappings(self, query_parameters=None):
        """

        Gets a list of Mapping resources.

        :param query_parameters: Parameters to filter the result of the list
        :type query_parameters: dict

        Returns the list of mappings
        :return: role list
        :rtype: list[Mapping]

        See https://developers.onelogin.com/api-docs/2/user-mappings/list-mappings List Mappings documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_MAPPINGS_URL")
        url = self.get_url(Constants.GET_MAPPINGS_URL, version_id=version_id)

        return self.retrieve_resources(Mapping, url, query_parameters, None, version_id)

    @exception_handler
    def create_mapping(self, mapping_params):
        """

        Creates Mapping

        :param mapping_params: Mapping data (name, enabled, match, position
                                          conditions[source, operator,value],
                                          actions[action, value])
        :type mapping_params: dict

        Returns the mapping
        :return: mapping
        :rtype: Mapping

        See https://developers.onelogin.com/api-docs/2/user-mappings/create-mapping Create Mapping documentation
        """
        self.clean_error()

        version_id = self.get_version_id("CREATE_MAPPING_URL")
        url = self.get_url(Constants.CREATE_MAPPING_URL, version_id=version_id)

        if 'actions' in mapping_params:
            for action in mapping_params['actions']:
                if 'value' in action and not isinstance(action['value'], list):
                    self.error = "422"
                    self.error_description = "Validation Failed"
                    self.error_attribute = "Verify that the value of any action provided has the type array"
                    return

        return self.create_resource(Mapping, url, mapping_params, None, version_id)

    @exception_handler
    def get_mapping(self, mapping_id):
        """

        Gets Mapping by ID.

        :param mapping_id: Id of the Mapping
        :type mapping_id: int

        Returns the mapping identified by the id
        :return: mapping
        :rtype: Mapping

        See https://developers.onelogin.com/api-docs/2/user-mappings/get-mapping Get Mapping documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_MAPPING_URL")
        url = self.get_url(Constants.GET_MAPPING_URL, mapping_id, version_id=version_id)

        return self.retrieve_resource(Mapping, url, version_id)

    @exception_handler
    def update_mapping(self, mapping_id, mapping_params):
        """

        Updates Mapping

        :param mapping_id: Id of the mapping
        :type mapping_id: int

        :param mapping_params: Mapping data (name, enabled, match, position
                                          conditions[source, operator,value],
                                          actions[action, value])
        :type mapping_params: dict

        Returns the mapping
        :return: mapping
        :rtype: Mapping

        Returns the modified mapping
        :return: mapping
        :rtype: Mapping

        See https://developers.onelogin.com/api-docs/2/user-mappings/update-mapping Update Mapping documentation
        """
        self.clean_error()

        version_id = self.get_version_id("UPDATE_MAPPING_URL")
        url = self.get_url(Constants.UPDATE_MAPPING_URL, mapping_id, version_id=version_id)

        return self.update_resource(Mapping, url, mapping_params, None, version_id)

    @exception_handler_return_false
    def delete_mapping(self, mapping_id):
        """

        Deletes mapping

        :param mapping_id: Id of the mapping to be deleted
        :type mapping_id: int

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/2/user-mappings/delete-mapping Delete Mapping documentation

        """
        self.clean_error()

        version_id = self.get_version_id("DELETE_MAPPING_URL")
        url = self.get_url(Constants.DELETE_MAPPING_URL, mapping_id, version_id=version_id)

        return self.delete_resource(url, version_id)

    @exception_handler
    def dryrun_mapping(self, mapping_id, user_ids):
        """

        Performs a User Mappings dry run

        :param mapping_id: Id of the mapping to be deleted
        :type mapping_id: int

        :param user_ids: List of user IDs tested against the mapping conditions to verify that the mapping would be applied
        :type user_ids: list[int]

        Returns
        :return: list of {User,mapped}
        :rtype: dict

        See https://developers.onelogin.com/api-docs/2/user-mappings/dry-run-mapping Dry Run Mapping documentation

        """
        self.clean_error()

        version_id = self.get_version_id("DRYRUN_MAPPING_URL")
        url = self.get_url(Constants.DRYRUN_MAPPING_URL, mapping_id, version_id=version_id)

        response = self.execute_call('post', url, json=user_ids)

        if response.status_code == 200:
            result = []
            data = response.json()
            for info in data:
                result_entry = {"user": User(info['user']),
                                "mapped": info["mapped"]}
                result.append(result_entry)
            return result
        else:
            self.set_error(response, True)
        return None

    @exception_handler
    def get_mapping_conditions(self):
        """

        Gets a list of Mapping Conditions types that can be used to match users when mappings are run.

        Returns the list of conditions
        :return: condition list
        :rtype: list[dict]

        See https://developers.onelogin.com/api-docs/2/user-mappings/list-conditions List Conditions documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_MAPPING_CONDITIONS_URL")
        url = self.get_url(Constants.GET_MAPPING_CONDITIONS_URL, version_id=version_id)

        return self.retrieve_list(url, version_id)

    @exception_handler
    def get_mapping_condition_operators(self, condition_value):
        """

        Gets a list of possible operators for a given condition value.

        :param condition_value: Value for the selected condition (A Mapping Condition).
        :type condition_value: string

        Returns the list of operators
        :return: operator list
        :rtype: list[dict]

        See https://developers.onelogin.com/api-docs/2/user-mappings/list-condition-operators List Conditions Operators documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_MAPPING_CONDITION_OPERATORS_URL")
        url = self.get_url(Constants.GET_MAPPING_CONDITION_OPERATORS_URL, condition_value, version_id=version_id)

        return self.retrieve_list(url, version_id)

    @exception_handler
    def get_mapping_condition_values(self, condition_value):
        """

        Gets a list of possible values to compare to a condition type.

        :param condition_value: Value for the selected condition (A Mapping Condition).
        :type condition_value: string

        Returns the list of values
        :return: value list
        :rtype: list[dict]

        See https://developers.onelogin.com/api-docs/2/user-mappings/list-condition-values List Condition Values documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_MAPPING_CONDITION_VALUES_URL")
        url = self.get_url(Constants.GET_MAPPING_CONDITION_VALUES_URL, condition_value, version_id=version_id)

        return self.retrieve_list(url, version_id)

    @exception_handler
    def get_mapping_actions(self):
        """

        Gets a list of the actions that can be applied when a mapping runs.

        Returns the list of actions
        :return: action list
        :rtype: list[dict]

        See https://developers.onelogin.com/api-docs/2/user-mappings/list-actions List Actions documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_MAPPING_ACTIONS_URL")
        url = self.get_url(Constants.GET_MAPPING_ACTIONS_URL, version_id=version_id)

        return self.retrieve_list(url, version_id)

    @exception_handler
    def get_mapping_action_values(self, action_value):
        """

        Gets a list of possible values to set using a given action.

        :param action_value: Value for the selected action (A Mapping Action).
        :type action_value: string

        Returns the list of values
        :return: value list
        :rtype: list[dict]

        See https://developers.onelogin.com/api-docs/2/user-mappings/list-action-values List Action values documentation
        """
        self.clean_error()

        version_id = self.get_version_id("GET_MAPPING_ACTION_VALUES_URL")
        url = self.get_url(Constants.GET_MAPPING_ACTION_VALUES_URL, action_value, version_id=version_id)

        return self.retrieve_list(url, version_id)

    @exception_handler
    def mapping_sort(self, mapping_ids):
        """

        Update order of mappings

        :param mapping_ids: ordered list of mapping_ids
        :type mapping_ids: list

        Returns the list of processed mapping ids
        :return: mapping_id list
        :rtype: list[int]

        See https://developers.onelogin.com/api-docs/2/user-mappings/bulk-sort Bulk Sort documentation
        """
        self.clean_error()

        version_id = self.get_version_id("MAPPING_SORT_URL")
        url = self.get_url(Constants.MAPPING_SORT_URL, version_id=version_id)

        return self.set_operation(url, mapping_ids, version_id)

    # Privilege Methods
    @exception_handler
    def get_privileges(self):
        """

        Gets a list of the Privileges created in an account.

        Returns the list of privileges
        :return: privileges list
        :rtype: list[Privilege]

        See https://developers.onelogin.com/api-docs/1/privileges/list-privileges List Privileges documentation

        """
        self.clean_error()

        version_id = self.get_version_id("LIST_PRIVILEGES_URL")
        url = self.get_url(Constants.LIST_PRIVILEGES_URL, version_id=version_id)

        # It has version 2 result
        return self.retrieve_resource_list(Privilege, url, None, None, 2)

    @exception_handler
    def create_privilege(self, name, version, statements):
        """

        Creates a Privilege

        :param name: The name of the privilege.
        :type name: string

        :param version: The version for the privilege schema. Set to 2018-05-18.
        :type version: string

        :param statements: A list of statements. Statement object or a dict with the keys Effect, Action and Scope
        :type statements: list[Statement] or list[dict]

        Returns the created privilege
        :return: privilege
        :rtype: Privilege

        See https://developers.onelogin.com/api-docs/1/privileges/create-privilege Create Privilege documentation

        """
        self.clean_error()

        version_id = self.get_version_id("CREATE_PRIVILEGE_URL")
        url = self.get_url(Constants.CREATE_PRIVILEGE_URL, version_id=version_id)

        statement_data = []
        for statement in statements:
            if isinstance(statement, Statement):
                statement_data.append({
                    'Effect': statement.effect,
                    'Action': statement.actions,
                    'Scope': statement.scopes

                })
            elif isinstance(statement, dict) and 'Effect' in statement and 'Action' in statement and 'Scope' in statement:
                statement_data.append(statement)
            else:
                self.error = str(400)
                self.error_description = "statements is invalid. Provide a list of statements. The statement should be an Statement object or dict with the keys Effect, Action and Scope"
                return

        privilege_data = {
            'name': name,
            'privilege': {
                'Version': version,
                'Statement': statement_data
            }
        }

        response = self.execute_call('post', url, json=privilege_data)
        if response.status_code == 201:
            json_data = response.json()
            if json_data and 'id' in json_data:
                return Privilege(str(json_data['id']), name, version, statements)
        else:
            self.set_error(response)

    @exception_handler
    def get_privilege(self, privilege_id):
        """

        Get a Privilege

        :param privilege_id: The id of the privilege.
        :type privilege_id: string

        Returns the privilege identified by the id
        :return: privilege
        :rtype: Privilege

        See https://developers.onelogin.com/api-docs/1/privileges/get-privilege Get Privilege documentation

        """
        self.clean_error()

        privilege_id = str(privilege_id)

        version_id = self.get_version_id("GET_PRIVILEGE_URL")
        url = self.get_url(Constants.GET_PRIVILEGE_URL, privilege_id, version_id=version_id)

        # It has version 2 result
        return self.retrieve_resource(Privilege, url, 2)

    @exception_handler
    def update_privilege(self, privilege_id, name, version, statements):
        """

        Updates a Privilege

        :param privilege_id: The id of the privilege you want to update.
        :type privilege_id: string

        :param name: The name of the privilege.
        :type name: string

        :param version: The version for the privilege schema. Set to 2018-05-18.
        :type version: string

        :param statements: A list of statements. Statement object or a dict with the keys Effect, Action and Scope
        :type statements: list[Statement] or list[dict]

        Returns the modified privilege
        :return: privilege
        :rtype: Privilege

        See https://developers.onelogin.com/api-docs/1/privileges/update-privilege Update Privilege documentation

        """
        self.clean_error()

        privilege_id = str(privilege_id)

        version_id = self.get_version_id("UPDATE_PRIVILEGE_URL")
        url = self.get_url(Constants.UPDATE_PRIVILEGE_URL, privilege_id, version_id=version_id)

        statement_data = []
        for statement in statements:
            if isinstance(statement, Statement):
                statement_data.append({
                    'Effect': statement.effect,
                    'Action': statement.actions,
                    'Scope': statement.scopes
                })
            elif isinstance(statement, dict) and 'Effect' in statement and 'Action' in statement and 'Scope' in statement:
                statement_data.append(statement)
            else:
                self.error = str(400)
                self.error_description = "statements is invalid. Provide a list of statements. The statement should be an Statement object or dict with the keys Effect, Action and Scope"
                return

        privilege_data = {
            'name': name,
            'privilege': {
                'Version': version,
                'Statement': statement_data,
            }
        }

        response = self.execute_call('put', url, json=privilege_data)
        if response.status_code == 200:
            json_data = response.json()
            if json_data and 'id' in json_data:
                return Privilege(str(json_data['id']), name, version, statements)
        else:
            self.set_error(response)

    @exception_handler
    def delete_privilege(self, privilege_id):
        """

        Deletes a Privilege

        :param privilege_id: The id of the privilege you want to delete.
        :type privilege_id: string

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/privileges/delete-privilege Delete Privilege documentation

        """
        self.clean_error()

        privilege_id = str(privilege_id)

        version_id = self.get_version_id("DELETE_PRIVILEGE_URL")
        url = self.get_url(Constants.DELETE_PRIVILEGE_URL, privilege_id, version_id=version_id)

        # Version 2 result, no content
        return self.delete_resource(url, 2)

    @exception_handler
    def get_roles_assigned_to_privilege(self, privilege_id, max_results=None):
        """

        Gets a list of the roles assigned to a privilege.

        :param privilege_id: The id of the privilege.
        :type privilege_id: string

        :param max_results: Limit the number of roles returned (optional)
        :type max_results: int

        Returns the list of roles
        :return: role_ids list
        :rtype: list[int]

        See https://developers.onelogin.com/api-docs/1/privileges/get-roles Get Assigned Roles documentation

        """
        self.clean_error()

        if max_results is None:
            max_results = self.max_results if self.max_results > 1000 else 1000

        version_id = self.get_version_id("GET_ROLES_ASSIGNED_TO_PRIVILEGE_URL")
        url = self.get_url(Constants.GET_ROLES_ASSIGNED_TO_PRIVILEGE_URL, privilege_id, version_id=version_id)

        role_ids = []
        response = None
        after_cursor = None
        query_parameters = None
        while (not response) or (len(role_ids) < max_results and after_cursor):
            response = self.execute_call('get', url, params=query_parameters)
            if response.status_code == 200:
                json_data = response.json()
                if json_data and 'roles' in json_data:
                    if len(role_ids) + len(json_data['roles']) < max_results:
                        role_ids += json_data['roles']
                    elif len(role_ids) + len(json_data['roles']) == max_results:
                        role_ids += json_data['roles']
                        return role_ids
                    else:
                        for role_id in json_data['roles']:
                            if len(role_ids) < max_results:
                                role_ids.append(role_id)
                            else:
                                return role_ids

                after_cursor = get_after_cursor(response, version_id)
                if after_cursor:
                    if not query_parameters:
                        query_parameters = {}
                    query_parameters['after_cursor'] = after_cursor
            else:
                self.set_error(response)
                break

        return role_ids

    @exception_handler_return_false
    def assign_roles_to_privilege(self, privilege_id, role_ids):
        """

        Assign one or more roles to a privilege.

        :param privilege_id: The id of the privilege.
        :type privilege_id: string

        :param role_ids: The ids of the roles to be assigned.
        :type role_ids: list

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/privileges/assign-role Assign Roles documentation

        """
        self.clean_error()

        version_id = self.get_version_id("ASSIGN_ROLES_TO_PRIVILEGE_URL")
        url = self.get_url(Constants.ASSIGN_ROLES_TO_PRIVILEGE_URL, privilege_id, version_id=version_id)

        data = {
            'roles': role_ids,
        }

        return self.create_operation(url, data)

    @exception_handler_return_false
    def remove_role_from_privilege(self, privilege_id, role_id):
        """

        Removes one role from the privilege.

        :param privilege_id: The id of the privilege.
        :type privilege_id: string

        :param role_id: The id of the role to be removed.
        :type role_id: int

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/privileges/remove-role Remove Role documentation

        """
        self.clean_error()

        version_id = self.get_version_id("REMOVE_ROLE_FROM_PRIVILEGE_URL")
        url = self.get_url(Constants.REMOVE_ROLE_FROM_PRIVILEGE_URL, privilege_id, role_id, version_id=version_id)

        # Version 2 result, no content
        return self.delete_resource(url, 2)

    @exception_handler
    def get_users_assigned_to_privilege(self, privilege_id, max_results=None):
        """

        Gets a list of the users assigned to a privilege.

        :param privilege_id: The id of the privilege.
        :type privilege_id: string

        :param max_results: Limit the number of users returned (optional)
        :type max_results: int

        Returns the list of users
        :return: user_ids list
        :rtype: list[int]

        See https://developers.onelogin.com/api-docs/1/privileges/get-users Get Assigned Users documentation

        """
        self.clean_error()

        if max_results is None:
            max_results = self.max_results if self.max_results > 1000 else 1000

        version_id = self.get_version_id("GET_USERS_ASSIGNED_TO_PRIVILEGE_URL")
        url = self.get_url(Constants.GET_USERS_ASSIGNED_TO_PRIVILEGE_URL, privilege_id, version_id=version_id)

        user_ids = []
        response = None
        after_cursor = None
        query_parameters = None
        while (not response) or (len(user_ids) < max_results and after_cursor):
            response = self.execute_call('get', url, params=query_parameters)
            if response.status_code == 200:
                json_data = response.json()
                if json_data and 'users' in json_data:
                    if len(user_ids) + len(json_data['users']) < max_results:
                        user_ids += json_data['users']
                    elif len(user_ids) + len(json_data['users']) == max_results:
                        user_ids += json_data['users']
                        return user_ids
                    else:
                        for user_id in json_data['users']:
                            if len(user_ids) < max_results:
                                user_ids.append(user_id)
                            else:
                                return user_ids

                after_cursor = get_after_cursor(response, version_id)
                if after_cursor:
                    if not query_parameters:
                        query_parameters = {}
                    query_parameters['after_cursor'] = after_cursor
            else:
                self.set_error(response)
                break

        return user_ids

    @exception_handler_return_false
    def assign_users_to_privilege(self, privilege_id, user_ids):
        """

        Assign one or more users to a privilege.

        :param privilege_id: The id of the privilege.
        :type privilege_id: string

        :param user_ids: The ids of the users to be assigned.
        :type user_ids: list

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/privileges/assign-users Assign Users documentation

        """
        self.clean_error()

        version_id = self.get_version_id("ASSIGN_USERS_TO_PRIVILEGE_URL")
        url = self.get_url(Constants.ASSIGN_USERS_TO_PRIVILEGE_URL, privilege_id, version_id=version_id)

        data = {
            'users': user_ids,
        }

        return self.create_operation(url, data)

    @exception_handler_return_false
    def remove_user_from_privilege(self, privilege_id, user_id):
        """

        Removes one user from the privilege.

        :param privilege_id: The id of the privilege.
        :type privilege_id: string

        :param user_id: The id of the user to be removed.
        :type user_id: int

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/privileges/remove-user Remove User documentation

        """
        self.clean_error()

        version_id = self.get_version_id("REMOVE_USER_FROM_PRIVILEGE_URL")
        url = self.get_url(Constants.REMOVE_USER_FROM_PRIVILEGE_URL, privilege_id, user_id, version_id=version_id)

        # Version 2 result, no content
        return self.delete_resource(url, 2)

    def execute_call(self, method, url, headers=None, params=None, json=None):
        self.prepare_token()

        if headers is None:
            headers = self.get_authorized_headers()

        response = None
        tries = 0
        while (tries < 2):
            if method == 'get':
                response = requests.get(url, headers=headers, params=params, timeout=self.requests_timeout)
            elif method == 'post':
                response = requests.post(url, headers=headers, json=json, params=params, timeout=self.requests_timeout)
            elif method == 'put':
                response = requests.put(url, headers=headers, json=json, params=params, timeout=self.requests_timeout)
            elif method == 'delete':
                response = requests.delete(url, headers=headers, json=json, timeout=self.requests_timeout)
            else:
                return response
            if response.status_code == 504 or (response.status_code == 401 and extract_error_message_from_response(response) == "Unauthorized"):
                if response.status_code == 401 and extract_error_message_from_response(response) == "Unauthorized":
                    if tries == 1:
                        self.access_token = None
                    self.clean_error()
                    self.prepare_token()
                    headers = self.get_authorized_headers(headers=headers)

                tries += 1
            else:
                return response

        return response
