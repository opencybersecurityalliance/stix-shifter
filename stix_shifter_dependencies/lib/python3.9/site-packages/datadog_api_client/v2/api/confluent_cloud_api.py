# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v2.model.confluent_accounts_response import ConfluentAccountsResponse
from datadog_api_client.v2.model.confluent_account_response import ConfluentAccountResponse
from datadog_api_client.v2.model.confluent_account_create_request import ConfluentAccountCreateRequest
from datadog_api_client.v2.model.confluent_account_update_request import ConfluentAccountUpdateRequest
from datadog_api_client.v2.model.confluent_resources_response import ConfluentResourcesResponse
from datadog_api_client.v2.model.confluent_resource_response import ConfluentResourceResponse
from datadog_api_client.v2.model.confluent_resource_request import ConfluentResourceRequest


class ConfluentCloudApi:
    """
    Configure your Datadog Confluent Cloud integration directly through the Datadog API.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_confluent_account_endpoint = _Endpoint(
            settings={
                "response_type": (ConfluentAccountResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/confluent-cloud/accounts",
                "operation_id": "create_confluent_account",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (ConfluentAccountCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._create_confluent_resource_endpoint = _Endpoint(
            settings={
                "response_type": (ConfluentResourceResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/confluent-cloud/accounts/{account_id}/resources",
                "operation_id": "create_confluent_resource",
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
                    "openapi_types": (ConfluentResourceRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_confluent_account_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/confluent-cloud/accounts/{account_id}",
                "operation_id": "delete_confluent_account",
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

        self._delete_confluent_resource_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/confluent-cloud/accounts/{account_id}/resources/{resource_id}",
                "operation_id": "delete_confluent_resource",
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
                "resource_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "resource_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_confluent_account_endpoint = _Endpoint(
            settings={
                "response_type": (ConfluentAccountResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/confluent-cloud/accounts/{account_id}",
                "operation_id": "get_confluent_account",
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

        self._get_confluent_resource_endpoint = _Endpoint(
            settings={
                "response_type": (ConfluentResourceResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/confluent-cloud/accounts/{account_id}/resources/{resource_id}",
                "operation_id": "get_confluent_resource",
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
                "resource_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "resource_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_confluent_account_endpoint = _Endpoint(
            settings={
                "response_type": (ConfluentAccountsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/confluent-cloud/accounts",
                "operation_id": "list_confluent_account",
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

        self._list_confluent_resource_endpoint = _Endpoint(
            settings={
                "response_type": (ConfluentResourcesResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/confluent-cloud/accounts/{account_id}/resources",
                "operation_id": "list_confluent_resource",
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

        self._update_confluent_account_endpoint = _Endpoint(
            settings={
                "response_type": (ConfluentAccountResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/confluent-cloud/accounts/{account_id}",
                "operation_id": "update_confluent_account",
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
                    "openapi_types": (ConfluentAccountUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_confluent_resource_endpoint = _Endpoint(
            settings={
                "response_type": (ConfluentResourceResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/integrations/confluent-cloud/accounts/{account_id}/resources/{resource_id}",
                "operation_id": "update_confluent_resource",
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
                "resource_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "resource_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (ConfluentResourceRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_confluent_account(
        self,
        body: ConfluentAccountCreateRequest,
    ) -> ConfluentAccountResponse:
        """Add Confluent account.

        Create a Confluent account.

        :param body: Confluent payload
        :type body: ConfluentAccountCreateRequest
        :rtype: ConfluentAccountResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_confluent_account_endpoint.call_with_http_info(**kwargs)

    def create_confluent_resource(
        self,
        account_id: str,
        body: ConfluentResourceRequest,
    ) -> ConfluentResourceResponse:
        """Add resource to Confluent account.

        Create a Confluent resource for the account associated with the provided ID.

        :param account_id: Confluent Account id.
        :type account_id: str
        :param body: Confluent payload
        :type body: ConfluentResourceRequest
        :rtype: ConfluentResourceResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_id"] = account_id

        kwargs["body"] = body

        return self._create_confluent_resource_endpoint.call_with_http_info(**kwargs)

    def delete_confluent_account(
        self,
        account_id: str,
    ) -> None:
        """Delete Confluent account.

        Delete a Confluent account with the provided account ID.

        :param account_id: Confluent Account id.
        :type account_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_id"] = account_id

        return self._delete_confluent_account_endpoint.call_with_http_info(**kwargs)

    def delete_confluent_resource(
        self,
        account_id: str,
        resource_id: str,
    ) -> None:
        """Delete resource from Confluent account.

        Delete a Confluent resource with the provided resource id for the account associated with the provided account ID.

        :param account_id: Confluent Account id.
        :type account_id: str
        :param resource_id: Confluent Account Resource ID.
        :type resource_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_id"] = account_id

        kwargs["resource_id"] = resource_id

        return self._delete_confluent_resource_endpoint.call_with_http_info(**kwargs)

    def get_confluent_account(
        self,
        account_id: str,
    ) -> ConfluentAccountResponse:
        """Get Confluent account.

        Get the Confluent account with the provided account ID.

        :param account_id: Confluent Account id.
        :type account_id: str
        :rtype: ConfluentAccountResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_id"] = account_id

        return self._get_confluent_account_endpoint.call_with_http_info(**kwargs)

    def get_confluent_resource(
        self,
        account_id: str,
        resource_id: str,
    ) -> ConfluentResourceResponse:
        """Get resource from Confluent account.

        Get a Confluent resource with the provided resource id for the account associated with the provided account ID.

        :param account_id: Confluent Account id.
        :type account_id: str
        :param resource_id: Confluent Account Resource ID.
        :type resource_id: str
        :rtype: ConfluentResourceResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_id"] = account_id

        kwargs["resource_id"] = resource_id

        return self._get_confluent_resource_endpoint.call_with_http_info(**kwargs)

    def list_confluent_account(
        self,
    ) -> ConfluentAccountsResponse:
        """List Confluent accounts.

        List Confluent accounts.

        :rtype: ConfluentAccountsResponse
        """
        kwargs: Dict[str, Any] = {}
        return self._list_confluent_account_endpoint.call_with_http_info(**kwargs)

    def list_confluent_resource(
        self,
        account_id: str,
    ) -> ConfluentResourcesResponse:
        """List Confluent Account resources.

        Get a Confluent resource for the account associated with the provided ID.

        :param account_id: Confluent Account id.
        :type account_id: str
        :rtype: ConfluentResourcesResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_id"] = account_id

        return self._list_confluent_resource_endpoint.call_with_http_info(**kwargs)

    def update_confluent_account(
        self,
        account_id: str,
        body: ConfluentAccountUpdateRequest,
    ) -> ConfluentAccountResponse:
        """Update Confluent account.

        Update the Confluent account with the provided account ID.

        :param account_id: Confluent Account id.
        :type account_id: str
        :param body: Confluent payload
        :type body: ConfluentAccountUpdateRequest
        :rtype: ConfluentAccountResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_id"] = account_id

        kwargs["body"] = body

        return self._update_confluent_account_endpoint.call_with_http_info(**kwargs)

    def update_confluent_resource(
        self,
        account_id: str,
        resource_id: str,
        body: ConfluentResourceRequest,
    ) -> ConfluentResourceResponse:
        """Update resource in Confluent account.

        Update a Confluent resource with the provided resource id for the account associated with the provided account ID.

        :param account_id: Confluent Account id.
        :type account_id: str
        :param resource_id: Confluent Account Resource ID.
        :type resource_id: str
        :param body: Confluent payload
        :type body: ConfluentResourceRequest
        :rtype: ConfluentResourceResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["account_id"] = account_id

        kwargs["resource_id"] = resource_id

        kwargs["body"] = body

        return self._update_confluent_resource_endpoint.call_with_http_info(**kwargs)
