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
from datadog_api_client.v2.model.authn_mappings_response import AuthNMappingsResponse
from datadog_api_client.v2.model.authn_mappings_sort import AuthNMappingsSort
from datadog_api_client.v2.model.authn_mapping_response import AuthNMappingResponse
from datadog_api_client.v2.model.authn_mapping_create_request import AuthNMappingCreateRequest
from datadog_api_client.v2.model.authn_mapping_update_request import AuthNMappingUpdateRequest


class AuthNMappingsApi:
    """
    `AuthN Mappings API <https://docs.datadoghq.com/account_management/authn_mapping/?tab=example>`_
    is used to automatically map group of users to roles in Datadog using attributes
    sent from Identity Providers.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_authn_mapping_endpoint = _Endpoint(
            settings={
                "response_type": (AuthNMappingResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/authn_mappings",
                "operation_id": "create_authn_mapping",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (AuthNMappingCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_authn_mapping_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/authn_mappings/{authn_mapping_id}",
                "operation_id": "delete_authn_mapping",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "authn_mapping_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "authn_mapping_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_authn_mapping_endpoint = _Endpoint(
            settings={
                "response_type": (AuthNMappingResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/authn_mappings/{authn_mapping_id}",
                "operation_id": "get_authn_mapping",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "authn_mapping_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "authn_mapping_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_authn_mappings_endpoint = _Endpoint(
            settings={
                "response_type": (AuthNMappingsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/authn_mappings",
                "operation_id": "list_authn_mappings",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
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
                    "openapi_types": (AuthNMappingsSort,),
                    "attribute": "sort",
                    "location": "query",
                },
                "filter": {
                    "openapi_types": (str,),
                    "attribute": "filter",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._update_authn_mapping_endpoint = _Endpoint(
            settings={
                "response_type": (AuthNMappingResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/authn_mappings/{authn_mapping_id}",
                "operation_id": "update_authn_mapping",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "authn_mapping_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "authn_mapping_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (AuthNMappingUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_authn_mapping(
        self,
        body: AuthNMappingCreateRequest,
    ) -> AuthNMappingResponse:
        """Create an AuthN Mapping.

        Create an AuthN Mapping.

        :type body: AuthNMappingCreateRequest
        :rtype: AuthNMappingResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_authn_mapping_endpoint.call_with_http_info(**kwargs)

    def delete_authn_mapping(
        self,
        authn_mapping_id: str,
    ) -> None:
        """Delete an AuthN Mapping.

        Delete an AuthN Mapping specified by AuthN Mapping UUID.

        :param authn_mapping_id: The UUID of the AuthN Mapping.
        :type authn_mapping_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["authn_mapping_id"] = authn_mapping_id

        return self._delete_authn_mapping_endpoint.call_with_http_info(**kwargs)

    def get_authn_mapping(
        self,
        authn_mapping_id: str,
    ) -> AuthNMappingResponse:
        """Get an AuthN Mapping by UUID.

        Get an AuthN Mapping specified by the AuthN Mapping UUID.

        :param authn_mapping_id: The UUID of the AuthN Mapping.
        :type authn_mapping_id: str
        :rtype: AuthNMappingResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["authn_mapping_id"] = authn_mapping_id

        return self._get_authn_mapping_endpoint.call_with_http_info(**kwargs)

    def list_authn_mappings(
        self,
        *,
        page_size: Union[int, UnsetType] = unset,
        page_number: Union[int, UnsetType] = unset,
        sort: Union[AuthNMappingsSort, UnsetType] = unset,
        filter: Union[str, UnsetType] = unset,
    ) -> AuthNMappingsResponse:
        """List all AuthN Mappings.

        List all AuthN Mappings in the org.

        :param page_size: Size for a given page. The maximum allowed value is 5000.
        :type page_size: int, optional
        :param page_number: Specific page number to return.
        :type page_number: int, optional
        :param sort: Sort AuthN Mappings depending on the given field.
        :type sort: AuthNMappingsSort, optional
        :param filter: Filter all mappings by the given string.
        :type filter: str, optional
        :rtype: AuthNMappingsResponse
        """
        kwargs: Dict[str, Any] = {}
        if page_size is not unset:
            kwargs["page_size"] = page_size

        if page_number is not unset:
            kwargs["page_number"] = page_number

        if sort is not unset:
            kwargs["sort"] = sort

        if filter is not unset:
            kwargs["filter"] = filter

        return self._list_authn_mappings_endpoint.call_with_http_info(**kwargs)

    def update_authn_mapping(
        self,
        authn_mapping_id: str,
        body: AuthNMappingUpdateRequest,
    ) -> AuthNMappingResponse:
        """Edit an AuthN Mapping.

        Edit an AuthN Mapping.

        :param authn_mapping_id: The UUID of the AuthN Mapping.
        :type authn_mapping_id: str
        :type body: AuthNMappingUpdateRequest
        :rtype: AuthNMappingResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["authn_mapping_id"] = authn_mapping_id

        kwargs["body"] = body

        return self._update_authn_mapping_endpoint.call_with_http_info(**kwargs)
