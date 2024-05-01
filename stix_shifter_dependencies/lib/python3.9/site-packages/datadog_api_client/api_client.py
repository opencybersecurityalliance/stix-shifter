# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.

import json
import atexit
import mimetypes
import warnings
import multiprocessing
from multiprocessing.pool import ThreadPool
from datetime import date, datetime
import io
import os
import re
from typing import Any, Dict, Optional, List, Tuple, Union
from typing_extensions import Self
from urllib.parse import quote
from urllib3.fields import RequestField  # type: ignore


from datadog_api_client import rest
from datadog_api_client.configuration import Configuration
from datadog_api_client.exceptions import ApiTypeError, ApiValueError
from datadog_api_client.model_utils import (
    ModelNormal,
    ModelSimple,
    ModelComposed,
    check_allowed_values,
    check_validations,
    deserialize_file,
    file_type,
    model_to_dict,
    validate_and_convert_types,
)


class ApiClient:
    """Generic API client for OpenAPI client library builds.

    OpenAPI generic API client. This client handles the client-
    server communication, and is invariant across implementations. Specifics of
    the methods and models for each application are generated from the OpenAPI
    templates.

    :param configuration: Configuration object for this client
    :param header_name: A header to pass when making calls to the API.
    :param header_value: A header value to pass when making calls to
        the API.
    """

    def __init__(self, configuration: Configuration):
        self.configuration = configuration

        self.rest_client = self._build_rest_client()
        self.default_headers = {}
        if self.configuration.compress:
            self.default_headers["Accept-Encoding"] = "gzip"
        # Set default User-Agent.
        self.user_agent = user_agent()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def close(self) -> None:
        self.rest_client.pool_manager.clear()

    def _build_rest_client(self):
        return rest.RESTClientObject(self.configuration)

    @property
    def user_agent(self) -> str:
        """User agent for this API client"""
        return self.default_headers["User-Agent"]

    @user_agent.setter
    def user_agent(self, value: str) -> None:
        self.default_headers["User-Agent"] = value

    def set_default_header(self, header_name: str, header_value: str) -> None:
        self.default_headers[header_name] = header_value

    def _call_api(
        self,
        method: str,
        url: str,
        query_params: Optional[List[Tuple[str, Any]]] = None,
        header_params: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
        post_params: Optional[List[Tuple[str, Any]]] = None,
        response_type: Optional[Tuple[Any]] = None,
        return_http_data_only: Optional[bool] = None,
        preload_content: bool = True,
        request_timeout: Optional[Union[int, float, Tuple[Union[int, float], Union[int, float]]]] = None,
        check_type: Optional[bool] = None,
    ):
        # perform request and return response
        response = self.rest_client.request(
            method,
            url,
            query_params=query_params,
            headers=header_params,
            post_params=post_params,
            body=body,
            preload_content=preload_content,
            request_timeout=request_timeout,
        )

        if not preload_content:
            return response

        # deserialize response data
        if response_type:
            if response_type == (file_type,):
                content_disposition = response.getheader("Content-Disposition")
                return_data = deserialize_file(
                    response.data, self.configuration.temp_folder_path, content_disposition=content_disposition
                )
            else:
                encoding = "utf-8"
                content_type = response.getheader("content-type")
                if content_type is not None:
                    match = re.search(r"charset=([a-zA-Z\-\d]+)[\s\;]?", content_type)
                    if match:
                        encoding = match.group(1)
                response_data = response.data.decode(encoding)

                return_data = self.deserialize(response_data, response_type, check_type)
        else:
            return_data = None

        if return_http_data_only:
            return return_data
        return (return_data, response.status, response.getheaders())

    def parameters_to_multipart(self, params):
        """Get parameters as list of tuples, formatting as json if value is dict.

        :param params: Parameters as list of two-tuples.

        :return: Parameters as list of tuple or urllib3.fields.RequestField
        """
        new_params = []
        for k, v in params.items() if isinstance(params, dict) else params:
            if isinstance(v, dict):  # v is instance of collection_type, formatting as application/json
                v = json.dumps(v, ensure_ascii=False).encode("utf-8")
                field = RequestField(k, v)
                field.make_multipart(content_type="application/json; charset=utf-8")
                new_params.append(field)
            else:
                new_params.append((k, v))
        return new_params

    @classmethod
    def sanitize_for_serialization(cls, obj):
        """Prepares data for transmission before it is sent with the rest client.
        If obj is None, return None.
        If obj is str, int, long, float, bool, return directly.
        If obj is datetime.datetime, datetime.date convert to string in iso8601 format.
        If obj is list, sanitize each element in the list.
        If obj is dict, return the dict.
        If obj is OpenAPI model, return the properties dict.
        If obj is io.IOBase, return the bytes.

        :param obj: The data to serialize.
        :return: The serialized form of data.
        """
        if isinstance(obj, (ModelNormal, ModelComposed)):
            return {key: cls.sanitize_for_serialization(val) for key, val in model_to_dict(obj).items()}
        elif isinstance(obj, io.IOBase):
            return cls.get_file_data_and_close_file(obj)
        elif isinstance(obj, (str, int, float, bool)) or obj is None:
            return obj
        elif isinstance(obj, (datetime, date)):
            if getattr(obj, "tzinfo", None) is not None:
                return obj.isoformat()
            return obj.strftime("%Y-%m-%dT%H:%M:%S") + obj.strftime(".%f")[:4] + "Z"
        elif isinstance(obj, ModelSimple):
            return cls.sanitize_for_serialization(obj.value)
        elif isinstance(obj, (list, tuple)):
            return [cls.sanitize_for_serialization(item) for item in obj]
        if isinstance(obj, dict):
            return {key: cls.sanitize_for_serialization(val) for key, val in obj.items()}
        raise ApiValueError("Unable to prepare type {} for serialization".format(obj.__class__.__name__))

    def deserialize(self, response_data: str, response_type: Any, check_type: Optional[bool]):
        """Deserializes response into an object.

        :param response_data: Response data to be deserialized.
        :param response_type: For the response, a tuple containing:
            valid classes
            a list containing valid classes (for list schemas)
            a dict containing a tuple of valid classes as the value
            Example values:
            (str,)
            (Pet,)
            (float, none_type)
            ([int, none_type],)
            ({str: (bool, str, int, float, date, datetime, str, none_type)},)
        :param check_type: boolean, whether to check the types of the data
            received from the server
        :type check_type: bool

        :return: deserialized object.
        """
        # fetch data from response object
        try:
            received_data = json.loads(response_data)
        except ValueError:
            received_data = response_data

        # store our data under the key of 'received_data' so users have some
        # context if they are deserializing a string and the data type is wrong
        deserialized_data = validate_and_convert_types(
            received_data, response_type, ["received_data"], True, check_type, configuration=self.configuration
        )
        return deserialized_data

    def call_api(
        self,
        resource_path: str,
        method: str,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[List[Tuple[str, Any]]] = None,
        header_params: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
        post_params: Optional[List[Tuple[str, Any]]] = None,
        files: Optional[Dict[str, List[io.FileIO]]] = None,
        response_type: Optional[Tuple[Any]] = None,
        return_http_data_only: Optional[bool] = None,
        collection_formats: Optional[Dict[str, str]] = None,
        preload_content: bool = True,
        request_timeout: Optional[Union[int, float, Tuple[Union[int, float], Union[int, float]]]] = None,
        host: Optional[str] = None,
        check_type: Optional[bool] = None,
    ):
        """Makes the HTTP request (synchronous) and returns deserialized data.

        :param resource_path: Path to method endpoint.
        :param method: Method to call.
        :param path_params: Path parameters in the url.
        :param query_params: Query parameters in the url.
        :param header_params: Header parameters to be
            placed in the request header.
        :param body: Request body.
        :param post_params dict: Request post form parameters,
            for `application/x-www-form-urlencoded`, `multipart/form-data`.
        :param response_type: For the response, a tuple containing:
            valid classes
            a list containing valid classes (for list schemas)
            a dict containing a tuple of valid classes as the value
            Example values:
            (str,)
            (Pet,)
            (float, none_type)
            ([int, none_type],)
            ({str: (bool, str, int, float, date, datetime, str, none_type)},)
        :param files: key -> field name, value -> a list of open file
            objects for `multipart/form-data`.
        :type files: dict
        :param return_http_data_only: response data without head status code
                                       and headers
        :type return_http_data_only: bool, optional
        :param collection_formats: dict of collection formats for path, query,
            header, and post parameters.
        :type collection_formats: dict, optional
        :param preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type preload_content: bool, optional
        :param request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param check_type: boolean describing if the data back from the server
            should have its type checked.
        :type check_type: bool, optional
        :return: the HTTP response.
        """
        # header parameters
        header_params = header_params or {}
        header_params.update(self.default_headers)
        if header_params:
            header_params = self.sanitize_for_serialization(header_params)
            header_params = dict(self.parameters_to_tuples(header_params, collection_formats))

        # path parameters
        if path_params:
            path_params = self.sanitize_for_serialization(path_params)
            for k, v in self.parameters_to_tuples(path_params, collection_formats):
                # specified safe chars, encode everything
                resource_path = resource_path.replace(
                    f"{{{k}}}", quote(str(v), safe=self.configuration.safe_chars_for_path_param)
                )

        # query parameters
        if query_params:
            query_params = self.sanitize_for_serialization(query_params)
            query_params = self.parameters_to_tuples(query_params, collection_formats)

        # post parameters
        if post_params or files:
            post_params = post_params or []
            post_params = self.sanitize_for_serialization(post_params)
            post_params = self.parameters_to_tuples(post_params, collection_formats)
            post_params.extend(self.files_parameters(files))
            if header_params["Content-Type"].startswith("multipart"):
                post_params = self.parameters_to_multipart(post_params)

        # body
        if body:
            body = self.sanitize_for_serialization(body)

        # request url
        if host is None:
            url = self.configuration.host + resource_path
        else:
            # use server/host defined in path or operation instead
            url = host + resource_path

        return self._call_api(
            method,
            url,
            query_params,
            header_params,
            body,
            post_params,
            response_type,
            return_http_data_only,
            preload_content,
            request_timeout,
            check_type,
        )

    def parameters_to_tuples(self, params, collection_formats) -> List[Tuple[str, Any]]:
        """Get parameters as list of tuples, formatting collections.

        :param params: Parameters as dict or list of two-tuples
        :param dict collection_formats: Parameter collection formats
        :return: Parameters as list of tuples, collections formatted
        """
        new_params: List[Tuple[str, str]] = []
        if collection_formats is None:
            collection_formats = {}
        for k, v in params.items() if isinstance(params, dict) else params:
            if k in collection_formats:
                collection_format = collection_formats[k]
                if collection_format == "multi":
                    new_params.extend((k, value) for value in v)
                else:
                    if collection_format == "ssv":
                        delimiter = " "
                    elif collection_format == "tsv":
                        delimiter = "\t"
                    elif collection_format == "pipes":
                        delimiter = "|"
                    else:  # csv is the default
                        delimiter = ","
                    new_params.append((k, delimiter.join(str(value) for value in v)))
            else:
                if isinstance(v, bool):
                    v = json.dumps(v)
                new_params.append((k, v))
        return new_params

    @staticmethod
    def get_file_data_and_close_file(file_instance: io.IOBase) -> bytes:
        file_data = file_instance.read()
        file_instance.close()
        return file_data

    def files_parameters(self, files: Optional[Dict[str, List[io.FileIO]]] = None):
        """Builds form parameters.

        :param files: None or a dict with key=param_name and
            value is a list of open file objects
        :return: List of tuples of form parameters with file data
        """
        if files is None:
            return []

        params = []
        for param_name, file_instances in files.items():
            if file_instances is None:
                # if the file field is nullable, skip None values
                continue
            for file_instance in file_instances:
                if file_instance is None:
                    # if the file field is nullable, skip None values
                    continue
                if file_instance.closed is True:
                    raise ApiValueError(
                        "Cannot read a closed file. The passed in file_type " "for %s must be open." % param_name
                    )
                filename = os.path.basename(str(file_instance.name))
                filedata = self.get_file_data_and_close_file(file_instance)
                mimetype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
                params.append(tuple([param_name, tuple([filename, filedata, mimetype])]))

        return params

    def select_header_accept(self, accepts: List[str]) -> str:
        """Returns `Accept` based on an array of accepts provided.

        :param accepts: List of headers.
        :return: Accept (e.g. application/json).
        """
        return ", ".join(accepts)

    def select_header_content_type(self, content_types: List[str]) -> str:
        """Returns `Content-Type` based on an array of content_types provided.

        :param content_types: List of content-types.
        :return: Content-Type (e.g. application/json).
        """
        if not content_types:
            return "application/json"

        content_types = [x.lower() for x in content_types]

        if "application/json" in content_types or "*/*" in content_types:
            return "application/json"
        return content_types[0]


class ThreadedApiClient(ApiClient):

    _pool = None

    def __init__(self, configuration: Configuration, pool_threads: int = 1):
        self.pool_threads = pool_threads
        self.connection_pool_maxsize = multiprocessing.cpu_count() * 5
        super().__init__(configuration)

    def _build_rest_client(self):
        return rest.RESTClientObject(self.configuration, maxsize=self.connection_pool_maxsize)

    def close(self) -> None:
        self.rest_client.pool_manager.clear()
        if self._pool:
            self._pool.close()
            self._pool.join()
            self._pool = None
            if hasattr(atexit, "unregister"):
                atexit.unregister(self.close)

    @property
    def pool(self) -> ThreadPool:
        """Create thread pool on first request
        avoids instantiating unused threadpool for blocking clients.
        """
        if self._pool is None:
            atexit.register(self.close)
            self._pool = ThreadPool(self.pool_threads)
        return self._pool

    def _call_api(
        self,
        method: str,
        url: str,
        query_params: Optional[List[Tuple[str, Any]]] = None,
        header_params: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
        post_params: Optional[List[Tuple[str, Any]]] = None,
        response_type: Optional[Tuple[Any]] = None,
        return_http_data_only: Optional[bool] = None,
        preload_content: bool = True,
        request_timeout: Optional[Union[int, float, Tuple]] = None,
        check_type: Optional[bool] = None,
    ):
        return self.pool.apply_async(
            super()._call_api,
            (
                method,
                url,
                query_params,
                header_params,
                body,
                post_params,
                response_type,
                return_http_data_only,
                preload_content,
                request_timeout,
                check_type,
            ),
        )


class AsyncApiClient(ApiClient):
    def _build_rest_client(self):
        return rest.AsyncRESTClientObject(self.configuration)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, _exc_type, exc, _tb):
        if exc:
            raise exc
        await self.rest_client._client.shutdown()

    async def _call_api(
        self,
        method: str,
        url: str,
        query_params: Optional[List[Tuple[str, Any]]] = None,
        header_params: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
        post_params: Optional[List[Tuple[str, Any]]] = None,
        response_type: Optional[Tuple[Any]] = None,
        return_http_data_only: Optional[bool] = None,
        preload_content: bool = True,
        request_timeout: Optional[Union[int, float, Tuple[Union[int, float], Union[int, float]]]] = None,
        check_type: Optional[bool] = None,
    ):

        # perform request and return response
        response = await self.rest_client.request(
            method,
            url,
            query_params=query_params,
            headers=header_params,
            post_params=post_params,
            body=body,
            preload_content=preload_content,
            request_timeout=request_timeout,
        )

        if not preload_content:
            return response

        # deserialize response data
        if response_type:
            if response_type == (file_type,):
                content_disposition = response.headers.get("Content-Disposition")
                response_data = await response.content()
                return_data = deserialize_file(
                    response_data, self.configuration.temp_folder_path, content_disposition=content_disposition
                )
            else:
                response_data = await response.text()

                return_data = self.deserialize(response_data, response_type, check_type)
        else:
            return_data = None

        if return_http_data_only:
            return return_data
        return (return_data, response.status_code, response.headers)


class Endpoint:
    def __init__(
        self,
        settings: Dict[str, Any],
        params_map: Dict[str, Dict[str, Any]],
        headers_map: Dict[str, List[str]],
        api_client: ApiClient,
    ):
        """Creates an endpoint.

        :param settings: See below key value pairs:
            'response_type' (tuple/None): response type
            'auth' (list): a list of auth type keys
            'endpoint_path' (str): the endpoint path
            'operation_id' (str): endpoint string identifier
            'http_method' (str): POST/PUT/PATCH/GET etc
            'servers' (list): list of str servers that this endpoint is at
            'version' (str): the API version
        :type settings: dict
        :param params_map: See below key value pairs:
            'required' (bool): whether the parameter is required
            'nullable' (bool): whether the parameter is nullable
            'validations' (dict): the validations dictionaries
            'allowed_values' (dict): the allowed values (enum) dictionaries
            'openapi_types' (dict): param_name to openapi type
            'attribute' (str): camelCase name
            'location' (str): 'body', 'file', 'form', 'header', 'path', 'query'
            'collection_format' (str): `csv` etc.
        :type params_map: dict
        :param headers_map: See below key value pairs:
            'accept' (list): list of Accept header strings
            'content_type' (list): list of Content-Type header strings
        :type headers_map: dict
        :param api_client API client instance.
        :type api_client: ApiClient
        """
        self.settings = settings
        self.params_map = params_map
        self.headers_map = headers_map
        self.api_client = api_client

    def _validate_inputs(self, kwargs):
        for param in kwargs:
            param_map = self.params_map[param]
            allowed_values = param_map.get("allowed_values")
            if allowed_values:
                check_allowed_values(list(allowed_values.values()), param, kwargs[param])

            validations = param_map.get("validation")
            if validations:
                check_validations(validations, param, kwargs[param], configuration=self.api_client.configuration)

        if not self.api_client.configuration.check_input_type:
            return

        for key, value in kwargs.items():
            fixed_val = validate_and_convert_types(
                value,
                self.params_map[key]["openapi_types"],
                [key],
                self.api_client.configuration.spec_property_naming,
                self.api_client.configuration.check_input_type,
                configuration=self.api_client.configuration,
            )
            kwargs[key] = fixed_val

    def _gather_params(self, kwargs):
        params = {"body": None, "collection_format": {}, "file": {}, "form": [], "header": {}, "path": {}, "query": []}

        for param_name, param_value in kwargs.items():
            param_map = self.params_map[param_name]
            param_location = param_map.get("location")
            if param_location is None:
                continue
            if param_location:
                if param_location == "body":
                    params["body"] = param_value
                    continue
                base_name = param_map["attribute"]
                openapi_types = param_map["openapi_types"]
                if param_location == "form" and openapi_types == (file_type,):
                    params["file"][param_name] = [param_value]
                elif param_location == "form" and openapi_types == ([file_type],):
                    # param_value is already a list
                    params["file"][param_name] = param_value
                elif param_location in {"form", "query"}:
                    param_value_full = (base_name, param_value)
                    params[param_location].append(param_value_full)
                if param_location not in {"form", "query"}:
                    params[param_location][base_name] = param_value
                collection_format = param_map.get("collection_format")
                if collection_format:
                    params["collection_format"][base_name] = collection_format

        return params

    def call_with_http_info(self, **kwargs):

        is_unstable = self.api_client.configuration.unstable_operations.get(
            "{}.{}".format(self.settings["version"], self.settings["operation_id"])
        )
        if is_unstable:
            warnings.warn("Using unstable operation '{0}'".format(self.settings["operation_id"]))
        elif is_unstable is False:
            raise ApiValueError("Unstable operation '{0}' is disabled".format(self.settings["operation_id"]))

        try:
            index = self.api_client.configuration.server_operation_index.get(
                self.settings["operation_id"], self.api_client.configuration.server_index
            )
            server_variables = self.api_client.configuration.server_operation_variables.get(
                self.settings["operation_id"], self.api_client.configuration.server_variables
            )
            host = self.api_client.configuration.get_host_from_settings(
                index, variables=server_variables, servers=self.settings["servers"]
            )
        except IndexError:
            if self.settings["servers"]:
                raise ApiValueError("Invalid host index. Must be 0 <= index < %s" % len(self.settings["servers"]))
            host = None

        for key, value in kwargs.items():
            if key not in self.params_map:
                raise ApiTypeError(
                    "Got an unexpected parameter '%s'" " to method `%s`" % (key, self.settings["operation_id"])
                )
            # only throw this nullable ApiValueError if check_input_type
            # is False, if check_input_type==True we catch this case
            # in self._validate_inputs
            if (
                not self.params_map[key].get("nullable")
                and value is None
                and not self.api_client.configuration.check_input_type
            ):
                raise ApiValueError(
                    "Value may not be None for non-nullable parameter `%s`"
                    " when calling `%s`" % (key, self.settings["operation_id"])
                )

        for key, param_map in self.params_map.items():
            if param_map.get("required") and key not in kwargs:
                raise ApiValueError(
                    "Missing the required parameter `%s` when calling " "`%s`" % (key, self.settings["operation_id"])
                )

        self._validate_inputs(kwargs)

        params = self._gather_params(kwargs)

        accept_headers_list = self.headers_map["accept"]
        if accept_headers_list:
            params["header"]["Accept"] = self.api_client.select_header_accept(accept_headers_list)

        content_type_headers_list = self.headers_map["content_type"]
        if content_type_headers_list:
            header_list = self.api_client.select_header_content_type(content_type_headers_list)
            params["header"]["Content-Type"] = header_list

        self.update_params_for_auth(params["header"], params["query"])

        return self.api_client.call_api(
            self.settings["endpoint_path"],
            self.settings["http_method"],
            params["path"],
            params["query"],
            params["header"],
            body=params["body"],
            post_params=params["form"],
            files=params["file"],
            response_type=self.settings["response_type"],
            check_type=self.api_client.configuration.check_return_type,
            return_http_data_only=self.api_client.configuration.return_http_data_only,
            preload_content=self.api_client.configuration.preload_content,
            request_timeout=self.api_client.configuration.request_timeout,
            host=host,
            collection_formats=params["collection_format"],
        )

    def update_params_for_auth(self, headers, queries) -> None:
        """Updates header and query params based on authentication setting.

        :param headers: Header parameters dict to be updated.
        :param queries: Query parameters tuple list to be updated.
        """
        if not self.settings["auth"]:
            return

        for auth in self.settings["auth"]:
            auth_setting = self.api_client.configuration.auth_settings().get(auth)
            if auth_setting:
                if auth_setting["in"] == "header":
                    if auth_setting["type"] != "http-signature":
                        if auth_setting["value"] is None:
                            raise ApiValueError("Invalid authentication token for {}".format(auth_setting["key"]))
                        headers[auth_setting["key"]] = auth_setting["value"]
                elif auth_setting["in"] == "query":
                    queries.append((auth_setting["key"], auth_setting["value"]))
                else:
                    raise ApiValueError("Authentication token must be in `query` or `header`")


def user_agent() -> str:
    """Generate default User-Agent header."""
    import platform
    from datadog_api_client.version import __version__

    return "datadog-api-client-python/{version} (python {py}; os {os}; arch {arch})".format(
        version=__version__,
        py=platform.python_version(),
        os=platform.system(),
        arch=platform.machine(),
    )
