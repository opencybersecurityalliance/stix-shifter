# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v2.model.cloudflare_accounts_response import CloudflareAccountsResponse
from datadog_api_client.v2.model.cloudflare_account_response import CloudflareAccountResponse
from datadog_api_client.v2.model.cloudflare_account_create_request import CloudflareAccountCreateRequest
from datadog_api_client.v2.model.cloudflare_account_update_request import CloudflareAccountUpdateRequest


class CloudflareIntegrationApi:
    """
    Configure your Datadog Cloudflare integration directly through the Datadog API.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_cloudflare_account_endpoint = _Endpoint(
            settings={
                "response_type": (CloudflareAccountResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/cloudflare/accounts",
                "operation_id": "create_cloudflare_account",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (CloudflareAccountCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_cloudflare_account_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/cloudflare/accounts/{account_id}",
                "operation_id": "delete_cloudflare_account",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "account_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "account_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_cloudflare_account_endpoint = _Endpoint(
            settings={
                "response_type": (CloudflareAccountResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/cloudflare/accounts/{account_id}",
                "operation_id": "get_cloudflare_account",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "account_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "account_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_cloudflare_accounts_endpoint = _Endpoint(
            settings={
                "response_type": (CloudflareAccountsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/cloudflare/accounts",
                "operation_id": "list_cloudflare_accounts",
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

        self._update_cloudflare_account_endpoint = _Endpoint(
            settings={
                "response_type": (CloudflareAccountResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/cloudflare/accounts/{account_id}",
                "operation_id": "update_cloudflare_account",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "account_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "account_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (CloudflareAccountUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_cloudflare_account(
        self,
        body: CloudflareAccountCreateRequest,
    ) -> CloudflareAccountResponse:
        """Add Cloudflare account.

        Create a Cloudflare account.

        :type body: CloudflareAccountCreateRequest
        :rtype: CloudflareAccountResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_cloudflare_account_endpoint.call_with_http_info(**kwargs)

    def delete_cloudflare_account(
        self,
        account_id: str,
    ) -> None:
        """Delete Cloudflare account.

        Delete a Cloudflare account.

        :param account_id: None
        :type account_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_id"] = account_id

        return self._delete_cloudflare_account_endpoint.call_with_http_info(**kwargs)

    def get_cloudflare_account(
        self,
        account_id: str,
    ) -> CloudflareAccountResponse:
        """Get Cloudflare account.

        Get a Cloudflare account.

        :param account_id: None
        :type account_id: str
        :rtype: CloudflareAccountResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_id"] = account_id

        return self._get_cloudflare_account_endpoint.call_with_http_info(**kwargs)

    def list_cloudflare_accounts(
        self,
    ) -> CloudflareAccountsResponse:
        """List Cloudflare accounts.

        List Cloudflare accounts.

        :rtype: CloudflareAccountsResponse
        """
        kwargs: Dict[str, Any] = {}
        return self._list_cloudflare_accounts_endpoint.call_with_http_info(**kwargs)

    def update_cloudflare_account(
        self,
        account_id: str,
        body: CloudflareAccountUpdateRequest,
    ) -> CloudflareAccountResponse:
        """Update Cloudflare account.

        Update a Cloudflare account.

        :param account_id: None
        :type account_id: str
        :type body: CloudflareAccountUpdateRequest
        :rtype: CloudflareAccountResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_id"] = account_id

        kwargs["body"] = body

        return self._update_cloudflare_account_endpoint.call_with_http_info(**kwargs)
