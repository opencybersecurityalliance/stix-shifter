# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v2.model.fastly_accounts_response import FastlyAccountsResponse
from datadog_api_client.v2.model.fastly_account_response import FastlyAccountResponse
from datadog_api_client.v2.model.fastly_account_create_request import FastlyAccountCreateRequest
from datadog_api_client.v2.model.fastly_account_update_request import FastlyAccountUpdateRequest
from datadog_api_client.v2.model.fastly_services_response import FastlyServicesResponse
from datadog_api_client.v2.model.fastly_service_response import FastlyServiceResponse
from datadog_api_client.v2.model.fastly_service_request import FastlyServiceRequest


class FastlyIntegrationApi:
    """
    Configure your Datadog Fastly integration directly through the Datadog API.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_fastly_account_endpoint = _Endpoint(
            settings={
                "response_type": (FastlyAccountResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/fastly/accounts",
                "operation_id": "create_fastly_account",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (FastlyAccountCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._create_fastly_service_endpoint = _Endpoint(
            settings={
                "response_type": (FastlyServiceResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/fastly/accounts/{account_id}/services",
                "operation_id": "create_fastly_service",
                "http_method": "POST",
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
                    "openapi_types": (FastlyServiceRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_fastly_account_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/fastly/accounts/{account_id}",
                "operation_id": "delete_fastly_account",
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

        self._delete_fastly_service_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/fastly/accounts/{account_id}/services/{service_id}",
                "operation_id": "delete_fastly_service",
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
                "service_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "service_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_fastly_account_endpoint = _Endpoint(
            settings={
                "response_type": (FastlyAccountResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/fastly/accounts/{account_id}",
                "operation_id": "get_fastly_account",
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

        self._get_fastly_service_endpoint = _Endpoint(
            settings={
                "response_type": (FastlyServiceResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/fastly/accounts/{account_id}/services/{service_id}",
                "operation_id": "get_fastly_service",
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
                "service_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "service_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_fastly_accounts_endpoint = _Endpoint(
            settings={
                "response_type": (FastlyAccountsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/fastly/accounts",
                "operation_id": "list_fastly_accounts",
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

        self._list_fastly_services_endpoint = _Endpoint(
            settings={
                "response_type": (FastlyServicesResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/fastly/accounts/{account_id}/services",
                "operation_id": "list_fastly_services",
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

        self._update_fastly_account_endpoint = _Endpoint(
            settings={
                "response_type": (FastlyAccountResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/fastly/accounts/{account_id}",
                "operation_id": "update_fastly_account",
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
                    "openapi_types": (FastlyAccountUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_fastly_service_endpoint = _Endpoint(
            settings={
                "response_type": (FastlyServiceResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/fastly/accounts/{account_id}/services/{service_id}",
                "operation_id": "update_fastly_service",
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
                "service_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "service_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (FastlyServiceRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_fastly_account(
        self,
        body: FastlyAccountCreateRequest,
    ) -> FastlyAccountResponse:
        """Add Fastly account.

        Create a Fastly account.

        :type body: FastlyAccountCreateRequest
        :rtype: FastlyAccountResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_fastly_account_endpoint.call_with_http_info(**kwargs)

    def create_fastly_service(
        self,
        account_id: str,
        body: FastlyServiceRequest,
    ) -> FastlyServiceResponse:
        """Add Fastly service.

        Create a Fastly service for an account.

        :param account_id: Fastly Account id.
        :type account_id: str
        :type body: FastlyServiceRequest
        :rtype: FastlyServiceResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_id"] = account_id

        kwargs["body"] = body

        return self._create_fastly_service_endpoint.call_with_http_info(**kwargs)

    def delete_fastly_account(
        self,
        account_id: str,
    ) -> None:
        """Delete Fastly account.

        Delete a Fastly account.

        :param account_id: Fastly Account id.
        :type account_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_id"] = account_id

        return self._delete_fastly_account_endpoint.call_with_http_info(**kwargs)

    def delete_fastly_service(
        self,
        account_id: str,
        service_id: str,
    ) -> None:
        """Delete Fastly service.

        Delete a Fastly service for an account.

        :param account_id: Fastly Account id.
        :type account_id: str
        :param service_id: Fastly Service ID.
        :type service_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_id"] = account_id

        kwargs["service_id"] = service_id

        return self._delete_fastly_service_endpoint.call_with_http_info(**kwargs)

    def get_fastly_account(
        self,
        account_id: str,
    ) -> FastlyAccountResponse:
        """Get Fastly account.

        Get a Fastly account.

        :param account_id: Fastly Account id.
        :type account_id: str
        :rtype: FastlyAccountResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_id"] = account_id

        return self._get_fastly_account_endpoint.call_with_http_info(**kwargs)

    def get_fastly_service(
        self,
        account_id: str,
        service_id: str,
    ) -> FastlyServiceResponse:
        """Get Fastly service.

        Get a Fastly service for an account.

        :param account_id: Fastly Account id.
        :type account_id: str
        :param service_id: Fastly Service ID.
        :type service_id: str
        :rtype: FastlyServiceResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_id"] = account_id

        kwargs["service_id"] = service_id

        return self._get_fastly_service_endpoint.call_with_http_info(**kwargs)

    def list_fastly_accounts(
        self,
    ) -> FastlyAccountsResponse:
        """List Fastly accounts.

        List Fastly accounts.

        :rtype: FastlyAccountsResponse
        """
        kwargs: Dict[str, Any] = {}
        return self._list_fastly_accounts_endpoint.call_with_http_info(**kwargs)

    def list_fastly_services(
        self,
        account_id: str,
    ) -> FastlyServicesResponse:
        """List Fastly services.

        List Fastly services for an account.

        :param account_id: Fastly Account id.
        :type account_id: str
        :rtype: FastlyServicesResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_id"] = account_id

        return self._list_fastly_services_endpoint.call_with_http_info(**kwargs)

    def update_fastly_account(
        self,
        account_id: str,
        body: FastlyAccountUpdateRequest,
    ) -> FastlyAccountResponse:
        """Update Fastly account.

        Update a Fastly account.

        :param account_id: Fastly Account id.
        :type account_id: str
        :type body: FastlyAccountUpdateRequest
        :rtype: FastlyAccountResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_id"] = account_id

        kwargs["body"] = body

        return self._update_fastly_account_endpoint.call_with_http_info(**kwargs)

    def update_fastly_service(
        self,
        account_id: str,
        service_id: str,
        body: FastlyServiceRequest,
    ) -> FastlyServiceResponse:
        """Update Fastly service.

        Update a Fastly service for an account.

        :param account_id: Fastly Account id.
        :type account_id: str
        :param service_id: Fastly Service ID.
        :type service_id: str
        :type body: FastlyServiceRequest
        :rtype: FastlyServiceResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_id"] = account_id

        kwargs["service_id"] = service_id

        kwargs["body"] = body

        return self._update_fastly_service_endpoint.call_with_http_info(**kwargs)
