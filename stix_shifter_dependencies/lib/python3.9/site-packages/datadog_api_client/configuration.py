# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.

import copy
import logging
import os
import urllib3  # type: ignore

from http import client as http_client
from datadog_api_client.exceptions import ApiValueError


JSON_SCHEMA_VALIDATION_KEYWORDS = {
    "multipleOf",
    "maximum",
    "exclusiveMaximum",
    "minimum",
    "exclusiveMinimum",
    "maxLength",
    "minLength",
    "pattern",
    "maxItems",
    "minItems",
}


class _UnstableOperations:
    def __init__(self, values):
        self.values = values

    def get(self, key, default=None):
        if key in self:
            return self[key]
        return default

    def __getitem__(self, key):
        if key in self.values:
            return self.values[key]
        for version in ("v1", "v2"):
            version_key = f"{version}.{key}"
            if version_key in self.values:
                return self.values[version_key]
        raise KeyError(f"Unknown unstable operation {key}")

    def __setitem__(self, key, value):
        if key in self.values:
            self.values[key] = value
        for version in ("v1", "v2"):
            version_key = f"{version}.{key}"
            if version_key in self.values:
                self.values[version_key] = value
                break
        else:
            raise KeyError(f"Unknown unstable operation {key}")

    def __contains__(self, key):
        if key in self.values:
            return True
        for version in ("v1", "v2"):
            version_key = f"{version}.{key}"
            if version_key in self.values:
                return True
        return False


class Configuration:
    """
    :param host: Base url.
    :param api_key: Dict to store API key(s).
        Each entry in the dict specifies an API key.
        The dict key is the name of the security scheme in the OAS specification.
        The dict value is the API key secret.
    :param api_key_prefix: Dict to store API prefix (e.g. Bearer).
        The dict key is the name of the security scheme in the OAS specification.
        The dict value is an API key prefix when generating the auth data.
    :param username: Username for HTTP basic authentication.
    :param password: Password for HTTP basic authentication.
    :param discard_unknown_keys: Boolean value indicating whether to discard
        unknown properties. A server may send a response that includes additional
        properties that are not known by the client in the following scenarios:

            1. The OpenAPI document is incomplete, i.e. it does not match the server
               implementation.
            2. The client was generated using an older version of the OpenAPI document
               and the server has been upgraded since then.

        If a schema in the OpenAPI document defines the additionalProperties
        attribute, then all undeclared properties received by the server are injected
        into the additional properties map. In that case, there are undeclared
        properties, and nothing to discard.
    :param disabled_client_side_validations: Comma-separated list of
        JSON schema validation keywords to disable JSON schema structural validation
        rules. The following keywords may be specified: multipleOf, maximum,
        exclusiveMaximum, minimum, exclusiveMinimum, maxLength, minLength, pattern,
        maxItems, minItems.
        By default, the validation is performed for data generated locally by the client
        and data received from the server, independent of any validation performed by
        the server side. If the input data does not satisfy the JSON schema validation
        rules specified in the OpenAPI document, an exception is raised.
        If disabled_client_side_validations is set, structural validation is
        disabled. This can be useful to troubleshoot data validation problem, such as
        when the OpenAPI document validation rules do not match the actual API data
        received by the server.
    :type disabled_client_side_validations: str
    :param server_index: Index to servers configuration.
    :param server_variables: Mapping with string values to replace variables in
        templated server configuration. The validation of enums is performed for
        variables with defined enum values before.
    :param server_operation_index: Mapping from operation ID to an index to
        server configuration.
    :param server_operation_variables: Mapping from operation ID to a mapping with
        string values to replace variables in templated server configuration.
        The validation of enums is performed for variables with defined enum values before.
    :param ssl_ca_cert: The path to a file of concatenated CA certificates
        in PEM format.
    :param compress: Boolean indicating whether encoded responses are accepted or not.
    :type compress: bool
    :param return_http_data_only: Response data without head status
        code and headers. Default is True.
    :type return_http_data_only: bool
    :param preload_content: If False, the urllib3.HTTPResponse object
        will be returned without reading/decoding response data.
        Default is True.
    :type preload_content: bool
    :param request_timeout: Timeout setting for this request. If one
        number provided, it will be total request timeout. It can also be a
        pair (tuple) of (connection, read) timeouts.  Default is None.
    :type request_timeout: float/tuple
    :param check_input_type: Specifies if type checking should be done one
        the data sent to the server. Default is True.
    :type check_input_type: bool
    :param check_return_type: Specifies if type checking should be done
        one the data received from the server. Default is True.
    :type check_return_type: bool
    :param spec_property_naming: Whether names in properties are expected to respect the spec or use snake case.
    :type spec_property_naming: bool
    """

    def __init__(
        self,
        host=None,
        api_key=None,
        api_key_prefix=None,
        access_token=None,
        username=None,
        password=None,
        discard_unknown_keys=True,
        disabled_client_side_validations="",
        server_index=None,
        server_variables=None,
        server_operation_index=None,
        server_operation_variables=None,
        ssl_ca_cert=None,
        compress=True,
        return_http_data_only=True,
        preload_content=True,
        request_timeout=None,
        check_input_type=True,
        check_return_type=True,
        spec_property_naming=False,
    ):
        """Constructor."""
        self._base_path = "https://api.datadoghq.com" if host is None else host
        self.server_index = 0 if server_index is None and host is None else server_index
        self.server_operation_index = server_operation_index or {}
        self.server_variables = server_variables or {}
        self.server_operation_variables = server_operation_variables or {}
        self.temp_folder_path = None

        # Authentication Settings
        self.access_token = access_token
        self.api_key = {}
        if api_key:
            self.api_key = api_key

        self.api_key_prefix = {}
        if api_key_prefix:
            self.api_key_prefix = api_key_prefix

        self.refresh_api_key_hook = None
        self.username = username
        self.password = password
        self.discard_unknown_keys = discard_unknown_keys
        self.disabled_client_side_validations = disabled_client_side_validations
        self.logger = {}
        self.logger["package_logger"] = logging.getLogger("datadog_api_client")
        self.logger["urllib3_logger"] = logging.getLogger("urllib3")
        self.logger_format = "%(asctime)s %(levelname)s %(message)s"
        self.logger_stream_handler = None
        self.logger_file_handler = None
        self.logger_file = None
        self.debug = False

        self.verify_ssl = True
        self.ssl_ca_cert = ssl_ca_cert
        self.cert_file = None
        self.key_file = None
        self.assert_hostname = None

        self.proxy = None
        self.proxy_headers = None
        self.safe_chars_for_path_param = ""
        self.retries = None
        # Enable client side validation
        self.client_side_validation = True

        # Options to pass down to the underlying urllib3 socket
        self.socket_options = None

        # Will translate to a Accept-Encoding header
        self.compress = compress

        self.return_http_data_only = return_http_data_only
        self.preload_content = preload_content
        self.request_timeout = request_timeout
        self.check_input_type = check_input_type
        self.check_return_type = check_return_type
        self.spec_property_naming = spec_property_naming

        # Keep track of unstable operations
        self.unstable_operations = _UnstableOperations(
            {
                "v2.list_events": False,
                "v2.search_events": False,
                "v2.create_incident": False,
                "v2.create_incident_integration": False,
                "v2.create_incident_todo": False,
                "v2.delete_incident": False,
                "v2.delete_incident_integration": False,
                "v2.delete_incident_todo": False,
                "v2.get_incident": False,
                "v2.get_incident_integration": False,
                "v2.get_incident_todo": False,
                "v2.list_incident_attachments": False,
                "v2.list_incident_integrations": False,
                "v2.list_incidents": False,
                "v2.list_incident_todos": False,
                "v2.search_incidents": False,
                "v2.update_incident": False,
                "v2.update_incident_attachments": False,
                "v2.update_incident_integration": False,
                "v2.update_incident_todo": False,
                "v2.query_scalar_data": False,
                "v2.query_timeseries_data": False,
                "v2.create_incident_service": False,
                "v2.delete_incident_service": False,
                "v2.get_incident_service": False,
                "v2.list_incident_services": False,
                "v2.update_incident_service": False,
                "v2.create_incident_team": False,
                "v2.delete_incident_team": False,
                "v2.get_incident_team": False,
                "v2.list_incident_teams": False,
                "v2.update_incident_team": False,
            }
        )

        # Load default values from environment
        if "DD_SITE" in os.environ:
            self.server_variables["site"] = os.environ["DD_SITE"]
        if "DD_API_KEY" in os.environ:
            self.api_key["apiKeyAuth"] = os.environ["DD_API_KEY"]
        if "DD_APP_KEY" in os.environ:
            self.api_key["appKeyAuth"] = os.environ["DD_APP_KEY"]

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k not in ("logger", "logger_file_handler"):
                setattr(result, k, copy.deepcopy(v, memo))
        # Shallow copy of loggers
        result.logger = copy.copy(self.logger)
        # Use setters to configure loggers
        result.logger_file = self.logger_file
        result.debug = self.debug
        return result

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name == "disabled_client_side_validations":
            s = set(filter(None, value.split(",")))
            for v in s:
                if v not in JSON_SCHEMA_VALIDATION_KEYWORDS:
                    raise ApiValueError("Invalid keyword: '{0}''".format(v))
            self._disabled_client_side_validations = s

    @property
    def logger_file(self):
        """The logger file.

        If the logger_file is None, then add stream handler and remove file
        handler. Otherwise, add file handler and remove stream handler.

        :return: The logger_file path.
        :rtype: str
        """
        return self._logger_file

    @logger_file.setter
    def logger_file(self, value):
        """The logger file.

        If the logger_file is None, then add stream handler and remove file
        handler. Otherwise, add file handler and remove stream handler.

        :param value: The logger_file path.
        :type value: str
        """
        self._logger_file = value
        if self._logger_file:
            # If set logging file,
            # then add file handler and remove stream handler.
            self.logger_file_handler = logging.FileHandler(self._logger_file)
            self.logger_file_handler.setFormatter(self.logger_formatter)
            for _, logger in self.logger.items():
                logger.addHandler(self.logger_file_handler)

    @property
    def debug(self):
        """Debug status.

        :return: The debug status, True or False.
        :rtype: bool
        """
        return self._debug

    @debug.setter
    def debug(self, value):
        """Debug status.

        :param value: The debug status, True or False.
        :type value: bool
        """
        self._debug = value
        if self._debug:
            # if debug status is True, turn on debug logging
            for _, logger in self.logger.items():
                logger.setLevel(logging.DEBUG)
            # turn on http_client debug
            http_client.HTTPConnection.debuglevel = 1
        else:
            # if debug status is False, turn off debug logging,
            # setting log level to default `logging.WARNING`
            for _, logger in self.logger.items():
                logger.setLevel(logging.WARNING)
            # turn off http_client debug
            http_client.HTTPConnection.debuglevel = 0

    @property
    def logger_format(self):
        """The logger format.

        The logger_formatter will be updated when sets logger_format.

        :return: The format string.
        :rtype: str
        """
        return self._logger_format

    @logger_format.setter
    def logger_format(self, value):
        """The logger format.

        The logger_formatter will be updated when sets logger_format.

        :param value: The format string.
        :type value: str
        """
        self._logger_format = value
        self.logger_formatter = logging.Formatter(self._logger_format)

    def get_api_key_with_prefix(self, identifier, alias=None):
        """Gets API key (with prefix if set).

        :param identifier: The identifier of apiKey.
        :param alias: The alternative identifier of apiKey.

        :return: The token for api key authentication.
        """
        if self.refresh_api_key_hook is not None:
            self.refresh_api_key_hook(self)
        key = self.api_key.get(identifier, self.api_key.get(alias) if alias is not None else None)
        if key:
            prefix = self.api_key_prefix.get(identifier)
            if prefix:
                return "%s %s" % (prefix, key)
            else:
                return key

    def get_basic_auth_token(self):
        """Gets HTTP basic authentication header (string).

        :return: The token for basic HTTP authentication.
        """
        username = ""
        if self.username is not None:
            username = self.username
        password = ""
        if self.password is not None:
            password = self.password
        return urllib3.util.make_headers(basic_auth=username + ":" + password).get("authorization")

    def get_host_settings(self):
        """Gets an array of host settings

        :return: An array of host settings
        """
        return [
            {
                "url": "https://{subdomain}.{site}",
                "description": "No description provided",
                "variables": {
                    "site": {
                        "description": "The regional site for Datadog customers.",
                        "default_value": "datadoghq.com",
                        "enum_values": [
                            "datadoghq.com",
                            "us3.datadoghq.com",
                            "us5.datadoghq.com",
                            "ap1.datadoghq.com",
                            "datadoghq.eu",
                            "ddog-gov.com",
                        ],
                    },
                    "subdomain": {
                        "description": "The subdomain where the API is deployed.",
                        "default_value": "api",
                    },
                },
            },
            {
                "url": "{protocol}://{name}",
                "description": "No description provided",
                "variables": {
                    "name": {
                        "description": "Full site DNS name.",
                        "default_value": "api.datadoghq.com",
                    },
                    "protocol": {
                        "description": "The protocol for accessing the API.",
                        "default_value": "https",
                    },
                },
            },
            {
                "url": "https://{subdomain}.{site}",
                "description": "No description provided",
                "variables": {
                    "site": {
                        "description": "Any Datadog deployment.",
                        "default_value": "datadoghq.com",
                    },
                    "subdomain": {
                        "description": "The subdomain where the API is deployed.",
                        "default_value": "api",
                    },
                },
            },
        ]

    def get_host_from_settings(self, index, variables=None, servers=None):
        """Gets host URL based on the index and variables.

        :param index: Array index of the host settings.
        :param variables: Hash of variable and the corresponding value.
        :param servers: An array of host settings or None.

        :return: URL based on host settings.
        """
        if index is None:
            return self._base_path

        variables = {} if variables is None else variables
        servers = self.get_host_settings() if servers is None else servers

        try:
            server = servers[index]
        except IndexError:
            raise ValueError(
                "Invalid index {0} when selecting the host settings. "
                "Must be less than {1}".format(index, len(servers))
            )

        url = server["url"]

        # go through variables and replace placeholders
        for variable_name, variable in server.get("variables", {}).items():
            used_value = variables.get(variable_name, variable["default_value"])

            if "enum_values" in variable and used_value not in variable["enum_values"]:
                raise ValueError(
                    "The variable `{0}` in the host URL has invalid value "
                    "{1}. Must be {2}.".format(variable_name, variables[variable_name], variable["enum_values"])
                )

            url = url.replace("{" + variable_name + "}", used_value)

        return url

    @property
    def host(self):
        """Return generated host."""
        return self.get_host_from_settings(self.server_index, variables=self.server_variables)

    @host.setter
    def host(self, value):
        """Fix base path."""
        self._base_path = value
        self.server_index = None

    def auth_settings(self):
        """Gets Auth Settings dict for api client.

        :return: The Auth Settings information dict.
        """
        auth = {}
        if self.access_token is not None:
            auth["AuthZ"] = {
                "type": "oauth2",
                "in": "header",
                "key": "Authorization",
                "value": "Bearer " + self.access_token,
            }
        if "apiKeyAuth" in self.api_key:
            auth["apiKeyAuth"] = {
                "type": "api_key",
                "in": "header",
                "key": "DD-API-KEY",
                "value": self.get_api_key_with_prefix(
                    "apiKeyAuth",
                ),
            }
        if "appKeyAuth" in self.api_key:
            auth["appKeyAuth"] = {
                "type": "api_key",
                "in": "header",
                "key": "DD-APPLICATION-KEY",
                "value": self.get_api_key_with_prefix(
                    "appKeyAuth",
                ),
            }
        return auth
