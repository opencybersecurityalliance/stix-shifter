# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v2.model.opsgenie_services_response import OpsgenieServicesResponse
from datadog_api_client.v2.model.opsgenie_service_response import OpsgenieServiceResponse
from datadog_api_client.v2.model.opsgenie_service_create_request import OpsgenieServiceCreateRequest
from datadog_api_client.v2.model.opsgenie_service_update_request import OpsgenieServiceUpdateRequest


class OpsgenieIntegrationApi:
    """
    Configure your `Datadog Opsgenie integration <https://docs.datadoghq.com/integrations/opsgenie/>`_
    directly through the Datadog API.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_opsgenie_service_endpoint = _Endpoint(
            settings={
                "response_type": (OpsgenieServiceResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integration/opsgenie/services",
                "operation_id": "create_opsgenie_service",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (OpsgenieServiceCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_opsgenie_service_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integration/opsgenie/services/{integration_service_id}",
                "operation_id": "delete_opsgenie_service",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "integration_service_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "integration_service_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_opsgenie_service_endpoint = _Endpoint(
            settings={
                "response_type": (OpsgenieServiceResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integration/opsgenie/services/{integration_service_id}",
                "operation_id": "get_opsgenie_service",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "integration_service_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "integration_service_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_opsgenie_services_endpoint = _Endpoint(
            settings={
                "response_type": (OpsgenieServicesResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integration/opsgenie/services",
                "operation_id": "list_opsgenie_services",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={},
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._update_opsgenie_service_endpoint = _Endpoint(
            settings={
                "response_type": (OpsgenieServiceResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integration/opsgenie/services/{integration_service_id}",
                "operation_id": "update_opsgenie_service",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "integration_service_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "integration_service_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (OpsgenieServiceUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_opsgenie_service(
        self,
        body: OpsgenieServiceCreateRequest,
    ) -> OpsgenieServiceResponse:
        """Create a new service object.

        Create a new service object in the Opsgenie integration.

        :param body: Opsgenie service payload
        :type body: OpsgenieServiceCreateRequest
        :rtype: OpsgenieServiceResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_opsgenie_service_endpoint.call_with_http_info(**kwargs)

    def delete_opsgenie_service(
        self,
        integration_service_id: str,
    ) -> None:
        """Delete a single service object.

        Delete a single service object in the Datadog Opsgenie integration.

        :param integration_service_id: The UUID of the service.
        :type integration_service_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["integration_service_id"] = integration_service_id

        return self._delete_opsgenie_service_endpoint.call_with_http_info(**kwargs)

    def get_opsgenie_service(
        self,
        integration_service_id: str,
    ) -> OpsgenieServiceResponse:
        """Get a single service object.

        Get a single service from the Datadog Opsgenie integration.

        :param integration_service_id: The UUID of the service.
        :type integration_service_id: str
        :rtype: OpsgenieServiceResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["integration_service_id"] = integration_service_id

        return self._get_opsgenie_service_endpoint.call_with_http_info(**kwargs)

    def list_opsgenie_services(
        self,
    ) -> OpsgenieServicesResponse:
        """Get all service objects.

        Get a list of all services from the Datadog Opsgenie integration.

        :rtype: OpsgenieServicesResponse
        """
        kwargs: Dict[str, Any] = {}
        return self._list_opsgenie_services_endpoint.call_with_http_info(**kwargs)

    def update_opsgenie_service(
        self,
        integration_service_id: str,
        body: OpsgenieServiceUpdateRequest,
    ) -> OpsgenieServiceResponse:
        """Update a single service object.

        Update a single service object in the Datadog Opsgenie integration.

        :param integration_service_id: The UUID of the service.
        :type integration_service_id: str
        :param body: Opsgenie service payload.
        :type body: OpsgenieServiceUpdateRequest
        :rtype: OpsgenieServiceResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["integration_service_id"] = integration_service_id

        kwargs["body"] = body

        return self._update_opsgenie_service_endpoint.call_with_http_info(**kwargs)
