# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v1.model.webhooks_integration_custom_variable_response import (
    WebhooksIntegrationCustomVariableResponse,
)
from datadog_api_client.v1.model.webhooks_integration_custom_variable import WebhooksIntegrationCustomVariable
from datadog_api_client.v1.model.webhooks_integration_custom_variable_update_request import (
    WebhooksIntegrationCustomVariableUpdateRequest,
)
from datadog_api_client.v1.model.webhooks_integration import WebhooksIntegration
from datadog_api_client.v1.model.webhooks_integration_update_request import WebhooksIntegrationUpdateRequest


class WebhooksIntegrationApi:
    """
    Configure your Datadog-Webhooks integration directly through the Datadog API.
    For more information about the Datadog-Webhooks integration,
    see the `integration page <https://docs.datadoghq.com/integrations/webhooks>`_.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_webhooks_integration_endpoint = _Endpoint(
            settings={
                "response_type": (WebhooksIntegration,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/webhooks/configuration/webhooks",
                "operation_id": "create_webhooks_integration",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (WebhooksIntegration,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._create_webhooks_integration_custom_variable_endpoint = _Endpoint(
            settings={
                "response_type": (WebhooksIntegrationCustomVariableResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/webhooks/configuration/custom-variables",
                "operation_id": "create_webhooks_integration_custom_variable",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (WebhooksIntegrationCustomVariable,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_webhooks_integration_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/webhooks/configuration/webhooks/{webhook_name}",
                "operation_id": "delete_webhooks_integration",
                "http_method": "DELETE",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "webhook_name": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "webhook_name",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._delete_webhooks_integration_custom_variable_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/webhooks/configuration/custom-variables/{custom_variable_name}",
                "operation_id": "delete_webhooks_integration_custom_variable",
                "http_method": "DELETE",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "custom_variable_name": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "custom_variable_name",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_webhooks_integration_endpoint = _Endpoint(
            settings={
                "response_type": (WebhooksIntegration,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/webhooks/configuration/webhooks/{webhook_name}",
                "operation_id": "get_webhooks_integration",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "webhook_name": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "webhook_name",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_webhooks_integration_custom_variable_endpoint = _Endpoint(
            settings={
                "response_type": (WebhooksIntegrationCustomVariableResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/webhooks/configuration/custom-variables/{custom_variable_name}",
                "operation_id": "get_webhooks_integration_custom_variable",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "custom_variable_name": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "custom_variable_name",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._update_webhooks_integration_endpoint = _Endpoint(
            settings={
                "response_type": (WebhooksIntegration,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/webhooks/configuration/webhooks/{webhook_name}",
                "operation_id": "update_webhooks_integration",
                "http_method": "PUT",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "webhook_name": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "webhook_name",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (WebhooksIntegrationUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_webhooks_integration_custom_variable_endpoint = _Endpoint(
            settings={
                "response_type": (WebhooksIntegrationCustomVariableResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/webhooks/configuration/custom-variables/{custom_variable_name}",
                "operation_id": "update_webhooks_integration_custom_variable",
                "http_method": "PUT",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "custom_variable_name": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "custom_variable_name",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (WebhooksIntegrationCustomVariableUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_webhooks_integration(
        self,
        body: WebhooksIntegration,
    ) -> WebhooksIntegration:
        """Create a webhooks integration.

        Creates an endpoint with the name ``<WEBHOOK_NAME>``.

        :param body: Create a webhooks integration request body.
        :type body: WebhooksIntegration
        :rtype: WebhooksIntegration
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_webhooks_integration_endpoint.call_with_http_info(**kwargs)

    def create_webhooks_integration_custom_variable(
        self,
        body: WebhooksIntegrationCustomVariable,
    ) -> WebhooksIntegrationCustomVariableResponse:
        """Create a custom variable.

        Creates an endpoint with the name ``<CUSTOM_VARIABLE_NAME>``.

        :param body: Define a custom variable request body.
        :type body: WebhooksIntegrationCustomVariable
        :rtype: WebhooksIntegrationCustomVariableResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_webhooks_integration_custom_variable_endpoint.call_with_http_info(**kwargs)

    def delete_webhooks_integration(
        self,
        webhook_name: str,
    ) -> None:
        """Delete a webhook.

        Deletes the endpoint with the name ``<WEBHOOK NAME>``.

        :param webhook_name: The name of the webhook.
        :type webhook_name: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["webhook_name"] = webhook_name

        return self._delete_webhooks_integration_endpoint.call_with_http_info(**kwargs)

    def delete_webhooks_integration_custom_variable(
        self,
        custom_variable_name: str,
    ) -> None:
        """Delete a custom variable.

        Deletes the endpoint with the name ``<CUSTOM_VARIABLE_NAME>``.

        :param custom_variable_name: The name of the custom variable.
        :type custom_variable_name: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["custom_variable_name"] = custom_variable_name

        return self._delete_webhooks_integration_custom_variable_endpoint.call_with_http_info(**kwargs)

    def get_webhooks_integration(
        self,
        webhook_name: str,
    ) -> WebhooksIntegration:
        """Get a webhook integration.

        Gets the content of the webhook with the name ``<WEBHOOK_NAME>``.

        :param webhook_name: The name of the webhook.
        :type webhook_name: str
        :rtype: WebhooksIntegration
        """
        kwargs: Dict[str, Any] = {}
        kwargs["webhook_name"] = webhook_name

        return self._get_webhooks_integration_endpoint.call_with_http_info(**kwargs)

    def get_webhooks_integration_custom_variable(
        self,
        custom_variable_name: str,
    ) -> WebhooksIntegrationCustomVariableResponse:
        """Get a custom variable.

        Shows the content of the custom variable with the name ``<CUSTOM_VARIABLE_NAME>``.

        If the custom variable is secret, the value does not return in the
        response payload.

        :param custom_variable_name: The name of the custom variable.
        :type custom_variable_name: str
        :rtype: WebhooksIntegrationCustomVariableResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["custom_variable_name"] = custom_variable_name

        return self._get_webhooks_integration_custom_variable_endpoint.call_with_http_info(**kwargs)

    def update_webhooks_integration(
        self,
        webhook_name: str,
        body: WebhooksIntegrationUpdateRequest,
    ) -> WebhooksIntegration:
        """Update a webhook.

        Updates the endpoint with the name ``<WEBHOOK_NAME>``.

        :param webhook_name: The name of the webhook.
        :type webhook_name: str
        :param body: Update an existing Datadog-Webhooks integration.
        :type body: WebhooksIntegrationUpdateRequest
        :rtype: WebhooksIntegration
        """
        kwargs: Dict[str, Any] = {}
        kwargs["webhook_name"] = webhook_name

        kwargs["body"] = body

        return self._update_webhooks_integration_endpoint.call_with_http_info(**kwargs)

    def update_webhooks_integration_custom_variable(
        self,
        custom_variable_name: str,
        body: WebhooksIntegrationCustomVariableUpdateRequest,
    ) -> WebhooksIntegrationCustomVariableResponse:
        """Update a custom variable.

        Updates the endpoint with the name ``<CUSTOM_VARIABLE_NAME>``.

        :param custom_variable_name: The name of the custom variable.
        :type custom_variable_name: str
        :param body: Update an existing custom variable request body.
        :type body: WebhooksIntegrationCustomVariableUpdateRequest
        :rtype: WebhooksIntegrationCustomVariableResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["custom_variable_name"] = custom_variable_name

        kwargs["body"] = body

        return self._update_webhooks_integration_custom_variable_endpoint.call_with_http_info(**kwargs)
