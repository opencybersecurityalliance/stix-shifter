# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict, Union

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.model_utils import (
    UnsetType,
    unset,
)
from datadog_api_client.v2.model.user_response import UserResponse
from datadog_api_client.v2.model.service_account_create_request import ServiceAccountCreateRequest
from datadog_api_client.v2.model.list_application_keys_response import ListApplicationKeysResponse
from datadog_api_client.v2.model.application_keys_sort import ApplicationKeysSort
from datadog_api_client.v2.model.application_key_response import ApplicationKeyResponse
from datadog_api_client.v2.model.application_key_create_request import ApplicationKeyCreateRequest
from datadog_api_client.v2.model.partial_application_key_response import PartialApplicationKeyResponse
from datadog_api_client.v2.model.application_key_update_request import ApplicationKeyUpdateRequest


class ServiceAccountsApi:
    """
    Create, edit, and disable service accounts.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_service_account_endpoint = _Endpoint(
            settings={
                "response_type": (UserResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/service_accounts",
                "operation_id": "create_service_account",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (ServiceAccountCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._create_service_account_application_key_endpoint = _Endpoint(
            settings={
                "response_type": (ApplicationKeyResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/service_accounts/{service_account_id}/application_keys",
                "operation_id": "create_service_account_application_key",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "service_account_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "service_account_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (ApplicationKeyCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_service_account_application_key_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/service_accounts/{service_account_id}/application_keys/{app_key_id}",
                "operation_id": "delete_service_account_application_key",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "service_account_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "service_account_id",
                    "location": "path",
                },
                "app_key_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "app_key_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_service_account_application_key_endpoint = _Endpoint(
            settings={
                "response_type": (PartialApplicationKeyResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/service_accounts/{service_account_id}/application_keys/{app_key_id}",
                "operation_id": "get_service_account_application_key",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "service_account_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "service_account_id",
                    "location": "path",
                },
                "app_key_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "app_key_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_service_account_application_keys_endpoint = _Endpoint(
            settings={
                "response_type": (ListApplicationKeysResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/service_accounts/{service_account_id}/application_keys",
                "operation_id": "list_service_account_application_keys",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "service_account_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "service_account_id",
                    "location": "path",
                },
                "page_size": {
                    "openapi_types": (int,),
                    "attribute": "page[size]",
                    "location": "query",
                },
                "page_number": {
                    "openapi_types": (int,),
                    "attribute": "page[number]",
                    "location": "query",
                },
                "sort": {
                    "openapi_types": (ApplicationKeysSort,),
                    "attribute": "sort",
                    "location": "query",
                },
                "filter": {
                    "openapi_types": (str,),
                    "attribute": "filter",
                    "location": "query",
                },
                "filter_created_at_start": {
                    "openapi_types": (str,),
                    "attribute": "filter[created_at][start]",
                    "location": "query",
                },
                "filter_created_at_end": {
                    "openapi_types": (str,),
                    "attribute": "filter[created_at][end]",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._update_service_account_application_key_endpoint = _Endpoint(
            settings={
                "response_type": (PartialApplicationKeyResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/service_accounts/{service_account_id}/application_keys/{app_key_id}",
                "operation_id": "update_service_account_application_key",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "service_account_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "service_account_id",
                    "location": "path",
                },
                "app_key_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "app_key_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (ApplicationKeyUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_service_account(
        self,
        body: ServiceAccountCreateRequest,
    ) -> UserResponse:
        """Create a service account.

        Create a service account for your organization.

        :type body: ServiceAccountCreateRequest
        :rtype: UserResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_service_account_endpoint.call_with_http_info(**kwargs)

    def create_service_account_application_key(
        self,
        service_account_id: str,
        body: ApplicationKeyCreateRequest,
    ) -> ApplicationKeyResponse:
        """Create an application key for this service account.

        Create an application key for this service account.

        :param service_account_id: The ID of the service account.
        :type service_account_id: str
        :type body: ApplicationKeyCreateRequest
        :rtype: ApplicationKeyResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["service_account_id"] = service_account_id

        kwargs["body"] = body

        return self._create_service_account_application_key_endpoint.call_with_http_info(**kwargs)

    def delete_service_account_application_key(
        self,
        service_account_id: str,
        app_key_id: str,
    ) -> None:
        """Delete an application key for this service account.

        Delete an application key owned by this service account.

        :param service_account_id: The ID of the service account.
        :type service_account_id: str
        :param app_key_id: The ID of the application key.
        :type app_key_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["service_account_id"] = service_account_id

        kwargs["app_key_id"] = app_key_id

        return self._delete_service_account_application_key_endpoint.call_with_http_info(**kwargs)

    def get_service_account_application_key(
        self,
        service_account_id: str,
        app_key_id: str,
    ) -> PartialApplicationKeyResponse:
        """Get one application key for this service account.

        Get an application key owned by this service account.

        :param service_account_id: The ID of the service account.
        :type service_account_id: str
        :param app_key_id: The ID of the application key.
        :type app_key_id: str
        :rtype: PartialApplicationKeyResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["service_account_id"] = service_account_id

        kwargs["app_key_id"] = app_key_id

        return self._get_service_account_application_key_endpoint.call_with_http_info(**kwargs)

    def list_service_account_application_keys(
        self,
        service_account_id: str,
        *,
        page_size: Union[int, UnsetType] = unset,
        page_number: Union[int, UnsetType] = unset,
        sort: Union[ApplicationKeysSort, UnsetType] = unset,
        filter: Union[str, UnsetType] = unset,
        filter_created_at_start: Union[str, UnsetType] = unset,
        filter_created_at_end: Union[str, UnsetType] = unset,
    ) -> ListApplicationKeysResponse:
        """List application keys for this service account.

        List all application keys available for this service account.

        :param service_account_id: The ID of the service account.
        :type service_account_id: str
        :param page_size: Size for a given page. The maximum allowed value is 5000.
        :type page_size: int, optional
        :param page_number: Specific page number to return.
        :type page_number: int, optional
        :param sort: Application key attribute used to sort results. Sort order is ascending
            by default. In order to specify a descending sort, prefix the
            attribute with a minus sign.
        :type sort: ApplicationKeysSort, optional
        :param filter: Filter application keys by the specified string.
        :type filter: str, optional
        :param filter_created_at_start: Only include application keys created on or after the specified date.
        :type filter_created_at_start: str, optional
        :param filter_created_at_end: Only include application keys created on or before the specified date.
        :type filter_created_at_end: str, optional
        :rtype: ListApplicationKeysResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["service_account_id"] = service_account_id

        if page_size is not unset:
            kwargs["page_size"] = page_size

        if page_number is not unset:
            kwargs["page_number"] = page_number

        if sort is not unset:
            kwargs["sort"] = sort

        if filter is not unset:
            kwargs["filter"] = filter

        if filter_created_at_start is not unset:
            kwargs["filter_created_at_start"] = filter_created_at_start

        if filter_created_at_end is not unset:
            kwargs["filter_created_at_end"] = filter_created_at_end

        return self._list_service_account_application_keys_endpoint.call_with_http_info(**kwargs)

    def update_service_account_application_key(
        self,
        service_account_id: str,
        app_key_id: str,
        body: ApplicationKeyUpdateRequest,
    ) -> PartialApplicationKeyResponse:
        """Edit an application key for this service account.

        Edit an application key owned by this service account.

        :param service_account_id: The ID of the service account.
        :type service_account_id: str
        :param app_key_id: The ID of the application key.
        :type app_key_id: str
        :type body: ApplicationKeyUpdateRequest
        :rtype: PartialApplicationKeyResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["service_account_id"] = service_account_id

        kwargs["app_key_id"] = app_key_id

        kwargs["body"] = body

        return self._update_service_account_application_key_endpoint.call_with_http_info(**kwargs)
