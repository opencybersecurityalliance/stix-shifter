# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v1.model.user_list_response import UserListResponse
from datadog_api_client.v1.model.user_response import UserResponse
from datadog_api_client.v1.model.user import User
from datadog_api_client.v1.model.user_disable_response import UserDisableResponse


class UsersApi:
    """
    Create, edit, and disable users.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_user_endpoint = _Endpoint(
            settings={
                "response_type": (UserResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/user",
                "operation_id": "create_user",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (User,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._disable_user_endpoint = _Endpoint(
            settings={
                "response_type": (UserDisableResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/user/{user_handle}",
                "operation_id": "disable_user",
                "http_method": "DELETE",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "user_handle": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "user_handle",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_user_endpoint = _Endpoint(
            settings={
                "response_type": (UserResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/user/{user_handle}",
                "operation_id": "get_user",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "user_handle": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "user_handle",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_users_endpoint = _Endpoint(
            settings={
                "response_type": (UserListResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/user",
                "operation_id": "list_users",
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

        self._update_user_endpoint = _Endpoint(
            settings={
                "response_type": (UserResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/user/{user_handle}",
                "operation_id": "update_user",
                "http_method": "PUT",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "user_handle": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "user_handle",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (User,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_user(
        self,
        body: User,
    ) -> UserResponse:
        """Create a user.

        Create a user for your organization.

        **Note** : Users can only be created with the admin access role
        if application keys belong to administrators.

        :param body: User object that needs to be created.
        :type body: User
        :rtype: UserResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_user_endpoint.call_with_http_info(**kwargs)

    def disable_user(
        self,
        user_handle: str,
    ) -> UserDisableResponse:
        """Disable a user.

        Delete a user from an organization.

        **Note** : This endpoint can only be used with application keys belonging to
        administrators.

        :param user_handle: The handle of the user.
        :type user_handle: str
        :rtype: UserDisableResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["user_handle"] = user_handle

        return self._disable_user_endpoint.call_with_http_info(**kwargs)

    def get_user(
        self,
        user_handle: str,
    ) -> UserResponse:
        """Get user details.

        Get a user's details.

        :param user_handle: The ID of the user.
        :type user_handle: str
        :rtype: UserResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["user_handle"] = user_handle

        return self._get_user_endpoint.call_with_http_info(**kwargs)

    def list_users(
        self,
    ) -> UserListResponse:
        """List all users.

        List all users for your organization.

        :rtype: UserListResponse
        """
        kwargs: Dict[str, Any] = {}
        return self._list_users_endpoint.call_with_http_info(**kwargs)

    def update_user(
        self,
        user_handle: str,
        body: User,
    ) -> UserResponse:
        """Update a user.

        Update a user information.

        **Note** : It can only be used with application keys belonging to administrators.

        :param user_handle: The ID of the user.
        :type user_handle: str
        :param body: Description of the update.
        :type body: User
        :rtype: UserResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["user_handle"] = user_handle

        kwargs["body"] = body

        return self._update_user_endpoint.call_with_http_info(**kwargs)
