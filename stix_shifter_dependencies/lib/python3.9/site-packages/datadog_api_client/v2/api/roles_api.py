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
from datadog_api_client.v2.model.permissions_response import PermissionsResponse
from datadog_api_client.v2.model.roles_response import RolesResponse
from datadog_api_client.v2.model.roles_sort import RolesSort
from datadog_api_client.v2.model.role_create_response import RoleCreateResponse
from datadog_api_client.v2.model.role_create_request import RoleCreateRequest
from datadog_api_client.v2.model.role_response import RoleResponse
from datadog_api_client.v2.model.role_update_response import RoleUpdateResponse
from datadog_api_client.v2.model.role_update_request import RoleUpdateRequest
from datadog_api_client.v2.model.role_clone_request import RoleCloneRequest
from datadog_api_client.v2.model.relationship_to_permission import RelationshipToPermission
from datadog_api_client.v2.model.users_response import UsersResponse
from datadog_api_client.v2.model.relationship_to_user import RelationshipToUser


class RolesApi:
    """
    The Roles API is used to create and manage Datadog roles, what
    `global permissions <https://docs.datadoghq.com/account_management/rbac/>`_
    they grant, and which users belong to them.

    Permissions related to specific account assets can be granted to roles
    in the Datadog application without using this API. For example, granting
    read access on a specific log index to a role can be done in Datadog from the
    `Pipelines page <https://app.datadoghq.com/logs/pipelines>`_.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._add_permission_to_role_endpoint = _Endpoint(
            settings={
                "response_type": (PermissionsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/roles/{role_id}/permissions",
                "operation_id": "add_permission_to_role",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "role_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "role_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (RelationshipToPermission,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._add_user_to_role_endpoint = _Endpoint(
            settings={
                "response_type": (UsersResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/roles/{role_id}/users",
                "operation_id": "add_user_to_role",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "role_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "role_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (RelationshipToUser,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._clone_role_endpoint = _Endpoint(
            settings={
                "response_type": (RoleResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/roles/{role_id}/clone",
                "operation_id": "clone_role",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "role_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "role_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (RoleCloneRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._create_role_endpoint = _Endpoint(
            settings={
                "response_type": (RoleCreateResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/roles",
                "operation_id": "create_role",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (RoleCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_role_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/roles/{role_id}",
                "operation_id": "delete_role",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "role_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "role_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_role_endpoint = _Endpoint(
            settings={
                "response_type": (RoleResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/roles/{role_id}",
                "operation_id": "get_role",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "role_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "role_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_permissions_endpoint = _Endpoint(
            settings={
                "response_type": (PermissionsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/permissions",
                "operation_id": "list_permissions",
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

        self._list_role_permissions_endpoint = _Endpoint(
            settings={
                "response_type": (PermissionsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/roles/{role_id}/permissions",
                "operation_id": "list_role_permissions",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "role_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "role_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_roles_endpoint = _Endpoint(
            settings={
                "response_type": (RolesResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/roles",
                "operation_id": "list_roles",
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
                    "openapi_types": (RolesSort,),
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

        self._list_role_users_endpoint = _Endpoint(
            settings={
                "response_type": (UsersResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/roles/{role_id}/users",
                "operation_id": "list_role_users",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "role_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "role_id",
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
                    "openapi_types": (str,),
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

        self._remove_permission_from_role_endpoint = _Endpoint(
            settings={
                "response_type": (PermissionsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/roles/{role_id}/permissions",
                "operation_id": "remove_permission_from_role",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "role_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "role_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (RelationshipToPermission,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._remove_user_from_role_endpoint = _Endpoint(
            settings={
                "response_type": (UsersResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/roles/{role_id}/users",
                "operation_id": "remove_user_from_role",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "role_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "role_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (RelationshipToUser,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_role_endpoint = _Endpoint(
            settings={
                "response_type": (RoleUpdateResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/roles/{role_id}",
                "operation_id": "update_role",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "role_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "role_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (RoleUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def add_permission_to_role(
        self,
        role_id: str,
        body: RelationshipToPermission,
    ) -> PermissionsResponse:
        """Grant permission to a role.

        Adds a permission to a role.

        :param role_id: The unique identifier of the role.
        :type role_id: str
        :type body: RelationshipToPermission
        :rtype: PermissionsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["role_id"] = role_id

        kwargs["body"] = body

        return self._add_permission_to_role_endpoint.call_with_http_info(**kwargs)

    def add_user_to_role(
        self,
        role_id: str,
        body: RelationshipToUser,
    ) -> UsersResponse:
        """Add a user to a role.

        Adds a user to a role.

        :param role_id: The unique identifier of the role.
        :type role_id: str
        :type body: RelationshipToUser
        :rtype: UsersResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["role_id"] = role_id

        kwargs["body"] = body

        return self._add_user_to_role_endpoint.call_with_http_info(**kwargs)

    def clone_role(
        self,
        role_id: str,
        body: RoleCloneRequest,
    ) -> RoleResponse:
        """Create a new role by cloning an existing role.

        Clone an existing role

        :param role_id: The unique identifier of the role.
        :type role_id: str
        :type body: RoleCloneRequest
        :rtype: RoleResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["role_id"] = role_id

        kwargs["body"] = body

        return self._clone_role_endpoint.call_with_http_info(**kwargs)

    def create_role(
        self,
        body: RoleCreateRequest,
    ) -> RoleCreateResponse:
        """Create role.

        Create a new role for your organization.

        :type body: RoleCreateRequest
        :rtype: RoleCreateResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_role_endpoint.call_with_http_info(**kwargs)

    def delete_role(
        self,
        role_id: str,
    ) -> None:
        """Delete role.

        Disables a role.

        :param role_id: The unique identifier of the role.
        :type role_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["role_id"] = role_id

        return self._delete_role_endpoint.call_with_http_info(**kwargs)

    def get_role(
        self,
        role_id: str,
    ) -> RoleResponse:
        """Get a role.

        Get a role in the organization specified by the role’s ``role_id``.

        :param role_id: The unique identifier of the role.
        :type role_id: str
        :rtype: RoleResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["role_id"] = role_id

        return self._get_role_endpoint.call_with_http_info(**kwargs)

    def list_permissions(
        self,
    ) -> PermissionsResponse:
        """List permissions.

        Returns a list of all permissions, including name, description, and ID.

        :rtype: PermissionsResponse
        """
        kwargs: Dict[str, Any] = {}
        return self._list_permissions_endpoint.call_with_http_info(**kwargs)

    def list_role_permissions(
        self,
        role_id: str,
    ) -> PermissionsResponse:
        """List permissions for a role.

        Returns a list of all permissions for a single role.

        :param role_id: The unique identifier of the role.
        :type role_id: str
        :rtype: PermissionsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["role_id"] = role_id

        return self._list_role_permissions_endpoint.call_with_http_info(**kwargs)

    def list_roles(
        self,
        *,
        page_size: Union[int, UnsetType] = unset,
        page_number: Union[int, UnsetType] = unset,
        sort: Union[RolesSort, UnsetType] = unset,
        filter: Union[str, UnsetType] = unset,
    ) -> RolesResponse:
        """List roles.

        Returns all roles, including their names and their unique identifiers.

        :param page_size: Size for a given page. The maximum allowed value is 5000.
        :type page_size: int, optional
        :param page_number: Specific page number to return.
        :type page_number: int, optional
        :param sort: Sort roles depending on the given field. Sort order is **ascending** by default.
            Sort order is **descending** if the field is prefixed by a negative sign, for example:
            ``sort=-name``.
        :type sort: RolesSort, optional
        :param filter: Filter all roles by the given string.
        :type filter: str, optional
        :rtype: RolesResponse
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

        return self._list_roles_endpoint.call_with_http_info(**kwargs)

    def list_role_users(
        self,
        role_id: str,
        *,
        page_size: Union[int, UnsetType] = unset,
        page_number: Union[int, UnsetType] = unset,
        sort: Union[str, UnsetType] = unset,
        filter: Union[str, UnsetType] = unset,
    ) -> UsersResponse:
        """Get all users of a role.

        Gets all users of a role.

        :param role_id: The unique identifier of the role.
        :type role_id: str
        :param page_size: Size for a given page. The maximum allowed value is 5000.
        :type page_size: int, optional
        :param page_number: Specific page number to return.
        :type page_number: int, optional
        :param sort: User attribute to order results by. Sort order is **ascending** by default.
            Sort order is **descending** if the field is prefixed by a negative sign,
            for example ``sort=-name``. Options: ``name`` , ``email`` , ``status``.
        :type sort: str, optional
        :param filter: Filter all users by the given string. Defaults to no filtering.
        :type filter: str, optional
        :rtype: UsersResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["role_id"] = role_id

        if page_size is not unset:
            kwargs["page_size"] = page_size

        if page_number is not unset:
            kwargs["page_number"] = page_number

        if sort is not unset:
            kwargs["sort"] = sort

        if filter is not unset:
            kwargs["filter"] = filter

        return self._list_role_users_endpoint.call_with_http_info(**kwargs)

    def remove_permission_from_role(
        self,
        role_id: str,
        body: RelationshipToPermission,
    ) -> PermissionsResponse:
        """Revoke permission.

        Removes a permission from a role.

        :param role_id: The unique identifier of the role.
        :type role_id: str
        :type body: RelationshipToPermission
        :rtype: PermissionsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["role_id"] = role_id

        kwargs["body"] = body

        return self._remove_permission_from_role_endpoint.call_with_http_info(**kwargs)

    def remove_user_from_role(
        self,
        role_id: str,
        body: RelationshipToUser,
    ) -> UsersResponse:
        """Remove a user from a role.

        Removes a user from a role.

        :param role_id: The unique identifier of the role.
        :type role_id: str
        :type body: RelationshipToUser
        :rtype: UsersResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["role_id"] = role_id

        kwargs["body"] = body

        return self._remove_user_from_role_endpoint.call_with_http_info(**kwargs)

    def update_role(
        self,
        role_id: str,
        body: RoleUpdateRequest,
    ) -> RoleUpdateResponse:
        """Update a role.

        Edit a role. Can only be used with application keys belonging to administrators.

        :param role_id: The unique identifier of the role.
        :type role_id: str
        :type body: RoleUpdateRequest
        :rtype: RoleUpdateResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["role_id"] = role_id

        kwargs["body"] = body

        return self._update_role_endpoint.call_with_http_info(**kwargs)
