# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict, List, Union

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.model_utils import (
    UnsetType,
    unset,
)
from datadog_api_client.v1.model.synthetics_batch_details import SyntheticsBatchDetails
from datadog_api_client.v1.model.synthetics_locations import SyntheticsLocations
from datadog_api_client.v1.model.synthetics_private_location_creation_response import (
    SyntheticsPrivateLocationCreationResponse,
)
from datadog_api_client.v1.model.synthetics_private_location import SyntheticsPrivateLocation
from datadog_api_client.v1.model.synthetics_list_tests_response import SyntheticsListTestsResponse
from datadog_api_client.v1.model.synthetics_api_test import SyntheticsAPITest
from datadog_api_client.v1.model.synthetics_browser_test import SyntheticsBrowserTest
from datadog_api_client.v1.model.synthetics_get_browser_test_latest_results_response import (
    SyntheticsGetBrowserTestLatestResultsResponse,
)
from datadog_api_client.v1.model.synthetics_browser_test_result_full import SyntheticsBrowserTestResultFull
from datadog_api_client.v1.model.synthetics_delete_tests_response import SyntheticsDeleteTestsResponse
from datadog_api_client.v1.model.synthetics_delete_tests_payload import SyntheticsDeleteTestsPayload
from datadog_api_client.v1.model.synthetics_trigger_ci_tests_response import SyntheticsTriggerCITestsResponse
from datadog_api_client.v1.model.synthetics_trigger_body import SyntheticsTriggerBody
from datadog_api_client.v1.model.synthetics_ci_test_body import SyntheticsCITestBody
from datadog_api_client.v1.model.synthetics_test_details import SyntheticsTestDetails
from datadog_api_client.v1.model.synthetics_get_api_test_latest_results_response import (
    SyntheticsGetAPITestLatestResultsResponse,
)
from datadog_api_client.v1.model.synthetics_api_test_result_full import SyntheticsAPITestResultFull
from datadog_api_client.v1.model.synthetics_update_test_pause_status_payload import (
    SyntheticsUpdateTestPauseStatusPayload,
)
from datadog_api_client.v1.model.synthetics_list_global_variables_response import SyntheticsListGlobalVariablesResponse
from datadog_api_client.v1.model.synthetics_global_variable import SyntheticsGlobalVariable


class SyntheticsApi:
    """
    Datadog Synthetics uses simulated user requests and browser rendering to help you ensure uptime,
    identify regional issues, and track your application performance. Datadog Synthetics tests come in
    two different flavors, `API tests <https://docs.datadoghq.com/synthetics/api_tests/?tab=httptest>`_
    and `browser tests <https://docs.datadoghq.com/synthetics/browser_tests>`_. You can use Datadog’s API to
    manage both test types programmatically.

    For more information about Synthetics, see the `Synthetics overview <https://docs.datadoghq.com/synthetics/>`_.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_global_variable_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsGlobalVariable,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/variables",
                "operation_id": "create_global_variable",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (SyntheticsGlobalVariable,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._create_private_location_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsPrivateLocationCreationResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/private-locations",
                "operation_id": "create_private_location",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (SyntheticsPrivateLocation,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._create_synthetics_api_test_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsAPITest,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/tests/api",
                "operation_id": "create_synthetics_api_test",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (SyntheticsAPITest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._create_synthetics_browser_test_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsBrowserTest,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/tests/browser",
                "operation_id": "create_synthetics_browser_test",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (SyntheticsBrowserTest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_global_variable_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/variables/{variable_id}",
                "operation_id": "delete_global_variable",
                "http_method": "DELETE",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "variable_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "variable_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._delete_private_location_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/private-locations/{location_id}",
                "operation_id": "delete_private_location",
                "http_method": "DELETE",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "location_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "location_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._delete_tests_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsDeleteTestsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/tests/delete",
                "operation_id": "delete_tests",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (SyntheticsDeleteTestsPayload,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._edit_global_variable_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsGlobalVariable,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/variables/{variable_id}",
                "operation_id": "edit_global_variable",
                "http_method": "PUT",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "variable_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "variable_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (SyntheticsGlobalVariable,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._get_api_test_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsAPITest,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/tests/api/{public_id}",
                "operation_id": "get_api_test",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "public_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "public_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_api_test_latest_results_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsGetAPITestLatestResultsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/tests/{public_id}/results",
                "operation_id": "get_api_test_latest_results",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "public_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "public_id",
                    "location": "path",
                },
                "from_ts": {
                    "openapi_types": (int,),
                    "attribute": "from_ts",
                    "location": "query",
                },
                "to_ts": {
                    "openapi_types": (int,),
                    "attribute": "to_ts",
                    "location": "query",
                },
                "probe_dc": {
                    "openapi_types": ([str],),
                    "attribute": "probe_dc",
                    "location": "query",
                    "collection_format": "multi",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_api_test_result_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsAPITestResultFull,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/tests/{public_id}/results/{result_id}",
                "operation_id": "get_api_test_result",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "public_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "public_id",
                    "location": "path",
                },
                "result_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "result_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_browser_test_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsBrowserTest,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/tests/browser/{public_id}",
                "operation_id": "get_browser_test",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "public_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "public_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_browser_test_latest_results_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsGetBrowserTestLatestResultsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/tests/browser/{public_id}/results",
                "operation_id": "get_browser_test_latest_results",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "public_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "public_id",
                    "location": "path",
                },
                "from_ts": {
                    "openapi_types": (int,),
                    "attribute": "from_ts",
                    "location": "query",
                },
                "to_ts": {
                    "openapi_types": (int,),
                    "attribute": "to_ts",
                    "location": "query",
                },
                "probe_dc": {
                    "openapi_types": ([str],),
                    "attribute": "probe_dc",
                    "location": "query",
                    "collection_format": "multi",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_browser_test_result_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsBrowserTestResultFull,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/tests/browser/{public_id}/results/{result_id}",
                "operation_id": "get_browser_test_result",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "public_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "public_id",
                    "location": "path",
                },
                "result_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "result_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_global_variable_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsGlobalVariable,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/variables/{variable_id}",
                "operation_id": "get_global_variable",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "variable_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "variable_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_private_location_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsPrivateLocation,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/private-locations/{location_id}",
                "operation_id": "get_private_location",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "location_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "location_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_synthetics_ci_batch_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsBatchDetails,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/ci/batch/{batch_id}",
                "operation_id": "get_synthetics_ci_batch",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "batch_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "batch_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_test_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsTestDetails,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/tests/{public_id}",
                "operation_id": "get_test",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "public_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "public_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_global_variables_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsListGlobalVariablesResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/variables",
                "operation_id": "list_global_variables",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={},
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_locations_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsLocations,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/locations",
                "operation_id": "list_locations",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={},
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_tests_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsListTestsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/tests",
                "operation_id": "list_tests",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "page_size": {
                    "openapi_types": (str,),
                    "attribute": "page_size",
                    "location": "query",
                },
                "page_number": {
                    "openapi_types": (str,),
                    "attribute": "page_number",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._trigger_ci_tests_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsTriggerCITestsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/tests/trigger/ci",
                "operation_id": "trigger_ci_tests",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (SyntheticsCITestBody,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._trigger_tests_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsTriggerCITestsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/tests/trigger",
                "operation_id": "trigger_tests",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (SyntheticsTriggerBody,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_api_test_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsAPITest,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/tests/api/{public_id}",
                "operation_id": "update_api_test",
                "http_method": "PUT",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "public_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "public_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (SyntheticsAPITest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_browser_test_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsBrowserTest,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/tests/browser/{public_id}",
                "operation_id": "update_browser_test",
                "http_method": "PUT",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "public_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "public_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (SyntheticsBrowserTest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_private_location_endpoint = _Endpoint(
            settings={
                "response_type": (SyntheticsPrivateLocation,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/private-locations/{location_id}",
                "operation_id": "update_private_location",
                "http_method": "PUT",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "location_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "location_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (SyntheticsPrivateLocation,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_test_pause_status_endpoint = _Endpoint(
            settings={
                "response_type": (bool,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/synthetics/tests/{public_id}/status",
                "operation_id": "update_test_pause_status",
                "http_method": "PUT",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "public_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "public_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (SyntheticsUpdateTestPauseStatusPayload,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_global_variable(
        self,
        body: SyntheticsGlobalVariable,
    ) -> SyntheticsGlobalVariable:
        """Create a global variable.

        Create a Synthetics global variable.

        :param body: Details of the global variable to create.
        :type body: SyntheticsGlobalVariable
        :rtype: SyntheticsGlobalVariable
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_global_variable_endpoint.call_with_http_info(**kwargs)

    def create_private_location(
        self,
        body: SyntheticsPrivateLocation,
    ) -> SyntheticsPrivateLocationCreationResponse:
        """Create a private location.

        Create a new Synthetics private location.

        :param body: Details of the private location to create.
        :type body: SyntheticsPrivateLocation
        :rtype: SyntheticsPrivateLocationCreationResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_private_location_endpoint.call_with_http_info(**kwargs)

    def create_synthetics_api_test(
        self,
        body: SyntheticsAPITest,
    ) -> SyntheticsAPITest:
        """Create an API test.

        Create a Synthetic API test.

        :param body: Details of the test to create.
        :type body: SyntheticsAPITest
        :rtype: SyntheticsAPITest
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_synthetics_api_test_endpoint.call_with_http_info(**kwargs)

    def create_synthetics_browser_test(
        self,
        body: SyntheticsBrowserTest,
    ) -> SyntheticsBrowserTest:
        """Create a browser test.

        Create a Synthetic browser test.

        :param body: Details of the test to create.
        :type body: SyntheticsBrowserTest
        :rtype: SyntheticsBrowserTest
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_synthetics_browser_test_endpoint.call_with_http_info(**kwargs)

    def delete_global_variable(
        self,
        variable_id: str,
    ) -> None:
        """Delete a global variable.

        Delete a Synthetics global variable.

        :param variable_id: The ID of the global variable.
        :type variable_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["variable_id"] = variable_id

        return self._delete_global_variable_endpoint.call_with_http_info(**kwargs)

    def delete_private_location(
        self,
        location_id: str,
    ) -> None:
        """Delete a private location.

        Delete a Synthetics private location.

        :param location_id: The ID of the private location.
        :type location_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["location_id"] = location_id

        return self._delete_private_location_endpoint.call_with_http_info(**kwargs)

    def delete_tests(
        self,
        body: SyntheticsDeleteTestsPayload,
    ) -> SyntheticsDeleteTestsResponse:
        """Delete tests.

        Delete multiple Synthetic tests by ID.

        :param body: Public ID list of the Synthetic tests to be deleted.
        :type body: SyntheticsDeleteTestsPayload
        :rtype: SyntheticsDeleteTestsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._delete_tests_endpoint.call_with_http_info(**kwargs)

    def edit_global_variable(
        self,
        variable_id: str,
        body: SyntheticsGlobalVariable,
    ) -> SyntheticsGlobalVariable:
        """Edit a global variable.

        Edit a Synthetics global variable.

        :param variable_id: The ID of the global variable.
        :type variable_id: str
        :param body: Details of the global variable to update.
        :type body: SyntheticsGlobalVariable
        :rtype: SyntheticsGlobalVariable
        """
        kwargs: Dict[str, Any] = {}
        kwargs["variable_id"] = variable_id

        kwargs["body"] = body

        return self._edit_global_variable_endpoint.call_with_http_info(**kwargs)

    def get_api_test(
        self,
        public_id: str,
    ) -> SyntheticsAPITest:
        """Get an API test.

        Get the detailed configuration associated with
        a Synthetic API test.

        :param public_id: The public ID of the test to get details from.
        :type public_id: str
        :rtype: SyntheticsAPITest
        """
        kwargs: Dict[str, Any] = {}
        kwargs["public_id"] = public_id

        return self._get_api_test_endpoint.call_with_http_info(**kwargs)

    def get_api_test_latest_results(
        self,
        public_id: str,
        *,
        from_ts: Union[int, UnsetType] = unset,
        to_ts: Union[int, UnsetType] = unset,
        probe_dc: Union[List[str], UnsetType] = unset,
    ) -> SyntheticsGetAPITestLatestResultsResponse:
        """Get an API test's latest results summaries.

        Get the last 150 test results summaries for a given Synthetics API test.

        :param public_id: The public ID of the test for which to search results for.
        :type public_id: str
        :param from_ts: Timestamp in milliseconds from which to start querying results.
        :type from_ts: int, optional
        :param to_ts: Timestamp in milliseconds up to which to query results.
        :type to_ts: int, optional
        :param probe_dc: Locations for which to query results.
        :type probe_dc: [str], optional
        :rtype: SyntheticsGetAPITestLatestResultsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["public_id"] = public_id

        if from_ts is not unset:
            kwargs["from_ts"] = from_ts

        if to_ts is not unset:
            kwargs["to_ts"] = to_ts

        if probe_dc is not unset:
            kwargs["probe_dc"] = probe_dc

        return self._get_api_test_latest_results_endpoint.call_with_http_info(**kwargs)

    def get_api_test_result(
        self,
        public_id: str,
        result_id: str,
    ) -> SyntheticsAPITestResultFull:
        """Get an API test result.

        Get a specific full result from a given (API) Synthetic test.

        :param public_id: The public ID of the API test to which the target result belongs.
        :type public_id: str
        :param result_id: The ID of the result to get.
        :type result_id: str
        :rtype: SyntheticsAPITestResultFull
        """
        kwargs: Dict[str, Any] = {}
        kwargs["public_id"] = public_id

        kwargs["result_id"] = result_id

        return self._get_api_test_result_endpoint.call_with_http_info(**kwargs)

    def get_browser_test(
        self,
        public_id: str,
    ) -> SyntheticsBrowserTest:
        """Get a browser test.

        Get the detailed configuration (including steps) associated with
        a Synthetic browser test.

        :param public_id: The public ID of the test to get details from.
        :type public_id: str
        :rtype: SyntheticsBrowserTest
        """
        kwargs: Dict[str, Any] = {}
        kwargs["public_id"] = public_id

        return self._get_browser_test_endpoint.call_with_http_info(**kwargs)

    def get_browser_test_latest_results(
        self,
        public_id: str,
        *,
        from_ts: Union[int, UnsetType] = unset,
        to_ts: Union[int, UnsetType] = unset,
        probe_dc: Union[List[str], UnsetType] = unset,
    ) -> SyntheticsGetBrowserTestLatestResultsResponse:
        """Get a browser test's latest results summaries.

        Get the last 150 test results summaries for a given Synthetics Browser test.

        :param public_id: The public ID of the browser test for which to search results
            for.
        :type public_id: str
        :param from_ts: Timestamp in milliseconds from which to start querying results.
        :type from_ts: int, optional
        :param to_ts: Timestamp in milliseconds up to which to query results.
        :type to_ts: int, optional
        :param probe_dc: Locations for which to query results.
        :type probe_dc: [str], optional
        :rtype: SyntheticsGetBrowserTestLatestResultsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["public_id"] = public_id

        if from_ts is not unset:
            kwargs["from_ts"] = from_ts

        if to_ts is not unset:
            kwargs["to_ts"] = to_ts

        if probe_dc is not unset:
            kwargs["probe_dc"] = probe_dc

        return self._get_browser_test_latest_results_endpoint.call_with_http_info(**kwargs)

    def get_browser_test_result(
        self,
        public_id: str,
        result_id: str,
    ) -> SyntheticsBrowserTestResultFull:
        """Get a browser test result.

        Get a specific full result from a given (browser) Synthetic test.

        :param public_id: The public ID of the browser test to which the target result
            belongs.
        :type public_id: str
        :param result_id: The ID of the result to get.
        :type result_id: str
        :rtype: SyntheticsBrowserTestResultFull
        """
        kwargs: Dict[str, Any] = {}
        kwargs["public_id"] = public_id

        kwargs["result_id"] = result_id

        return self._get_browser_test_result_endpoint.call_with_http_info(**kwargs)

    def get_global_variable(
        self,
        variable_id: str,
    ) -> SyntheticsGlobalVariable:
        """Get a global variable.

        Get the detailed configuration of a global variable.

        :param variable_id: The ID of the global variable.
        :type variable_id: str
        :rtype: SyntheticsGlobalVariable
        """
        kwargs: Dict[str, Any] = {}
        kwargs["variable_id"] = variable_id

        return self._get_global_variable_endpoint.call_with_http_info(**kwargs)

    def get_private_location(
        self,
        location_id: str,
    ) -> SyntheticsPrivateLocation:
        """Get a private location.

        Get a Synthetics private location.

        :param location_id: The ID of the private location.
        :type location_id: str
        :rtype: SyntheticsPrivateLocation
        """
        kwargs: Dict[str, Any] = {}
        kwargs["location_id"] = location_id

        return self._get_private_location_endpoint.call_with_http_info(**kwargs)

    def get_synthetics_ci_batch(
        self,
        batch_id: str,
    ) -> SyntheticsBatchDetails:
        """Get details of batch.

        Get a batch's updated details.

        :param batch_id: The ID of the batch.
        :type batch_id: str
        :rtype: SyntheticsBatchDetails
        """
        kwargs: Dict[str, Any] = {}
        kwargs["batch_id"] = batch_id

        return self._get_synthetics_ci_batch_endpoint.call_with_http_info(**kwargs)

    def get_test(
        self,
        public_id: str,
    ) -> SyntheticsTestDetails:
        """Get a test configuration.

        Get the detailed configuration associated with a Synthetics test.

        :param public_id: The public ID of the test to get details from.
        :type public_id: str
        :rtype: SyntheticsTestDetails
        """
        kwargs: Dict[str, Any] = {}
        kwargs["public_id"] = public_id

        return self._get_test_endpoint.call_with_http_info(**kwargs)

    def list_global_variables(
        self,
    ) -> SyntheticsListGlobalVariablesResponse:
        """Get all global variables.

        Get the list of all Synthetics global variables.

        :rtype: SyntheticsListGlobalVariablesResponse
        """
        kwargs: Dict[str, Any] = {}
        return self._list_global_variables_endpoint.call_with_http_info(**kwargs)

    def list_locations(
        self,
    ) -> SyntheticsLocations:
        """Get all locations (public and private).

        Get the list of public and private locations available for Synthetic
        tests. No arguments required.

        :rtype: SyntheticsLocations
        """
        kwargs: Dict[str, Any] = {}
        return self._list_locations_endpoint.call_with_http_info(**kwargs)

    def list_tests(
        self,
        *,
        page_size: Union[str, UnsetType] = unset,
        page_number: Union[str, UnsetType] = unset,
    ) -> SyntheticsListTestsResponse:
        """Get the list of all Synthetic tests.

        Get the list of all Synthetic tests.

        :param page_size: Used for pagination. The number of tests returned in the page.
        :type page_size: str, optional
        :param page_number: Used for pagination. Which page you want to retrieve. Starts at zero.
        :type page_number: str, optional
        :rtype: SyntheticsListTestsResponse
        """
        kwargs: Dict[str, Any] = {}
        if page_size is not unset:
            kwargs["page_size"] = page_size

        if page_number is not unset:
            kwargs["page_number"] = page_number

        return self._list_tests_endpoint.call_with_http_info(**kwargs)

    def trigger_ci_tests(
        self,
        body: SyntheticsCITestBody,
    ) -> SyntheticsTriggerCITestsResponse:
        """Trigger tests from CI/CD pipelines.

        Trigger a set of Synthetics tests for continuous integration.

        :param body: Details of the test to trigger.
        :type body: SyntheticsCITestBody
        :rtype: SyntheticsTriggerCITestsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._trigger_ci_tests_endpoint.call_with_http_info(**kwargs)

    def trigger_tests(
        self,
        body: SyntheticsTriggerBody,
    ) -> SyntheticsTriggerCITestsResponse:
        """Trigger Synthetics tests.

        Trigger a set of Synthetics tests.

        :param body: The identifiers of the tests to trigger.
        :type body: SyntheticsTriggerBody
        :rtype: SyntheticsTriggerCITestsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._trigger_tests_endpoint.call_with_http_info(**kwargs)

    def update_api_test(
        self,
        public_id: str,
        body: SyntheticsAPITest,
    ) -> SyntheticsAPITest:
        """Edit an API test.

        Edit the configuration of a Synthetic API test.

        :param public_id: The public ID of the test to get details from.
        :type public_id: str
        :param body: New test details to be saved.
        :type body: SyntheticsAPITest
        :rtype: SyntheticsAPITest
        """
        kwargs: Dict[str, Any] = {}
        kwargs["public_id"] = public_id

        kwargs["body"] = body

        return self._update_api_test_endpoint.call_with_http_info(**kwargs)

    def update_browser_test(
        self,
        public_id: str,
        body: SyntheticsBrowserTest,
    ) -> SyntheticsBrowserTest:
        """Edit a browser test.

        Edit the configuration of a Synthetic browser test.

        :param public_id: The public ID of the test to get details from.
        :type public_id: str
        :param body: New test details to be saved.
        :type body: SyntheticsBrowserTest
        :rtype: SyntheticsBrowserTest
        """
        kwargs: Dict[str, Any] = {}
        kwargs["public_id"] = public_id

        kwargs["body"] = body

        return self._update_browser_test_endpoint.call_with_http_info(**kwargs)

    def update_private_location(
        self,
        location_id: str,
        body: SyntheticsPrivateLocation,
    ) -> SyntheticsPrivateLocation:
        """Edit a private location.

        Edit a Synthetics private location.

        :param location_id: The ID of the private location.
        :type location_id: str
        :param body: Details of the private location to be updated.
        :type body: SyntheticsPrivateLocation
        :rtype: SyntheticsPrivateLocation
        """
        kwargs: Dict[str, Any] = {}
        kwargs["location_id"] = location_id

        kwargs["body"] = body

        return self._update_private_location_endpoint.call_with_http_info(**kwargs)

    def update_test_pause_status(
        self,
        public_id: str,
        body: SyntheticsUpdateTestPauseStatusPayload,
    ) -> bool:
        """Pause or start a test.

        Pause or start a Synthetics test by changing the status.

        :param public_id: The public ID of the Synthetic test to update.
        :type public_id: str
        :param body: Status to set the given Synthetic test to.
        :type body: SyntheticsUpdateTestPauseStatusPayload
        :rtype: bool
        """
        kwargs: Dict[str, Any] = {}
        kwargs["public_id"] = public_id

        kwargs["body"] = body

        return self._update_test_pause_status_endpoint.call_with_http_info(**kwargs)
