# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v1.model.azure_account import AzureAccount
from datadog_api_client.v1.model.azure_account_list_response import AzureAccountListResponse


class AzureIntegrationApi:
    """
    Configure your Datadog-Azure integration directly through the Datadog API.
    For more information, see the `Datadog-Azure integration page <https://docs.datadoghq.com/integrations/azure>`_.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_azure_integration_endpoint = _Endpoint(
            settings={
                "response_type": (dict,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/azure",
                "operation_id": "create_azure_integration",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (AzureAccount,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_azure_integration_endpoint = _Endpoint(
            settings={
                "response_type": (dict,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/azure",
                "operation_id": "delete_azure_integration",
                "http_method": "DELETE",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (AzureAccount,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._list_azure_integration_endpoint = _Endpoint(
            settings={
                "response_type": (AzureAccountListResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/azure",
                "operation_id": "list_azure_integration",
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

        self._update_azure_host_filters_endpoint = _Endpoint(
            settings={
                "response_type": (dict,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/azure/host_filters",
                "operation_id": "update_azure_host_filters",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (AzureAccount,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_azure_integration_endpoint = _Endpoint(
            settings={
                "response_type": (dict,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/azure",
                "operation_id": "update_azure_integration",
                "http_method": "PUT",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (AzureAccount,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_azure_integration(
        self,
        body: AzureAccount,
    ) -> dict:
        """Create an Azure integration.

        Create a Datadog-Azure integration.

        Using the ``POST`` method updates your integration configuration by adding your new
        configuration to the existing one in your Datadog organization.

        Using the ``PUT`` method updates your integration configuration by replacing your
        current configuration with the new one sent to your Datadog organization.

        :param body: Create a Datadog-Azure integration for your Datadog account request body.
        :type body: AzureAccount
        :rtype: dict
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_azure_integration_endpoint.call_with_http_info(**kwargs)

    def delete_azure_integration(
        self,
        body: AzureAccount,
    ) -> dict:
        """Delete an Azure integration.

        Delete a given Datadog-Azure integration from your Datadog account.

        :param body: Delete a given Datadog-Azure integration request body.
        :type body: AzureAccount
        :rtype: dict
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._delete_azure_integration_endpoint.call_with_http_info(**kwargs)

    def list_azure_integration(
        self,
    ) -> AzureAccountListResponse:
        """List all Azure integrations.

        List all Datadog-Azure integrations configured in your Datadog account.

        :rtype: AzureAccountListResponse
        """
        kwargs: Dict[str, Any] = {}
        return self._list_azure_integration_endpoint.call_with_http_info(**kwargs)

    def update_azure_host_filters(
        self,
        body: AzureAccount,
    ) -> dict:
        """Update Azure integration host filters.

        Update the defined list of host filters for a given Datadog-Azure integration.

        :param body: Update a Datadog-Azure integration's host filters request body.
        :type body: AzureAccount
        :rtype: dict
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._update_azure_host_filters_endpoint.call_with_http_info(**kwargs)

    def update_azure_integration(
        self,
        body: AzureAccount,
    ) -> dict:
        """Update an Azure integration.

        Update a Datadog-Azure integration. Requires an existing ``tenant_name`` and ``client_id``.
        Any other fields supplied will overwrite existing values. To overwrite ``tenant_name`` or ``client_id`` ,
        use ``new_tenant_name`` and ``new_client_id``. To leave a field unchanged, do not supply that field in the payload.

        :param body: Update a Datadog-Azure integration request body.
        :type body: AzureAccount
        :rtype: dict
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._update_azure_integration_endpoint.call_with_http_info(**kwargs)
