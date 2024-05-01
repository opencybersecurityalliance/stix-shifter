# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v1.model.gcp_account import GCPAccount
from datadog_api_client.v1.model.gcp_account_list_response import GCPAccountListResponse


class GCPIntegrationApi:
    """
    Configure your Datadog-Google Cloud Platform (GCP) integration directly
    through the Datadog API. Read more about the `Datadog-Google Cloud Platform integration <https://docs.datadoghq.com/integrations/google_cloud_platform>`_.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_gcp_integration_endpoint = _Endpoint(
            settings={
                "response_type": (dict,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/gcp",
                "operation_id": "create_gcp_integration",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (GCPAccount,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_gcp_integration_endpoint = _Endpoint(
            settings={
                "response_type": (dict,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/gcp",
                "operation_id": "delete_gcp_integration",
                "http_method": "DELETE",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (GCPAccount,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._list_gcp_integration_endpoint = _Endpoint(
            settings={
                "response_type": (GCPAccountListResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/gcp",
                "operation_id": "list_gcp_integration",
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

        self._update_gcp_integration_endpoint = _Endpoint(
            settings={
                "response_type": (dict,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/integration/gcp",
                "operation_id": "update_gcp_integration",
                "http_method": "PUT",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (GCPAccount,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_gcp_integration(
        self,
        body: GCPAccount,
    ) -> dict:
        """Create a GCP integration.

        Create a Datadog-GCP integration.

        :param body: Create a Datadog-GCP integration.
        :type body: GCPAccount
        :rtype: dict
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_gcp_integration_endpoint.call_with_http_info(**kwargs)

    def delete_gcp_integration(
        self,
        body: GCPAccount,
    ) -> dict:
        """Delete a GCP integration.

        Delete a given Datadog-GCP integration.

        :param body: Delete a given Datadog-GCP integration.
        :type body: GCPAccount
        :rtype: dict
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._delete_gcp_integration_endpoint.call_with_http_info(**kwargs)

    def list_gcp_integration(
        self,
    ) -> GCPAccountListResponse:
        """List all GCP integrations.

        List all Datadog-GCP integrations configured in your Datadog account.

        :rtype: GCPAccountListResponse
        """
        kwargs: Dict[str, Any] = {}
        return self._list_gcp_integration_endpoint.call_with_http_info(**kwargs)

    def update_gcp_integration(
        self,
        body: GCPAccount,
    ) -> dict:
        """Update a GCP integration.

        Update a Datadog-GCP integrations host_filters and/or auto-mute.
        Requires a ``project_id`` and ``client_email`` , however these fields cannot be updated.
        If you need to update these fields, delete and use the create ( ``POST`` ) endpoint.
        The unspecified fields will keep their original values.

        :param body: Update a Datadog-GCP integration.
        :type body: GCPAccount
        :rtype: dict
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._update_gcp_integration_endpoint.call_with_http_info(**kwargs)
