# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v1.model.dashboard_list_list_response import DashboardListListResponse
from datadog_api_client.v1.model.dashboard_list import DashboardList
from datadog_api_client.v1.model.dashboard_list_delete_response import DashboardListDeleteResponse


class DashboardListsApi:
    """
    Interact with your dashboard lists through the API to
    organize, find, and share all of your dashboards with your team and
    organization.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_dashboard_list_endpoint = _Endpoint(
            settings={
                "response_type": (DashboardList,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/dashboard/lists/manual",
                "operation_id": "create_dashboard_list",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (DashboardList,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_dashboard_list_endpoint = _Endpoint(
            settings={
                "response_type": (DashboardListDeleteResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/dashboard/lists/manual/{list_id}",
                "operation_id": "delete_dashboard_list",
                "http_method": "DELETE",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "list_id": {
                    "required": True,
                    "openapi_types": (int,),
                    "attribute": "list_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_dashboard_list_endpoint = _Endpoint(
            settings={
                "response_type": (DashboardList,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/dashboard/lists/manual/{list_id}",
                "operation_id": "get_dashboard_list",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "list_id": {
                    "required": True,
                    "openapi_types": (int,),
                    "attribute": "list_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_dashboard_lists_endpoint = _Endpoint(
            settings={
                "response_type": (DashboardListListResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/dashboard/lists/manual",
                "operation_id": "list_dashboard_lists",
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

        self._update_dashboard_list_endpoint = _Endpoint(
            settings={
                "response_type": (DashboardList,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/dashboard/lists/manual/{list_id}",
                "operation_id": "update_dashboard_list",
                "http_method": "PUT",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "list_id": {
                    "required": True,
                    "openapi_types": (int,),
                    "attribute": "list_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (DashboardList,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_dashboard_list(
        self,
        body: DashboardList,
    ) -> DashboardList:
        """Create a dashboard list.

        Create an empty dashboard list.

        :param body: Create a dashboard list request body.
        :type body: DashboardList
        :rtype: DashboardList
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_dashboard_list_endpoint.call_with_http_info(**kwargs)

    def delete_dashboard_list(
        self,
        list_id: int,
    ) -> DashboardListDeleteResponse:
        """Delete a dashboard list.

        Delete a dashboard list.

        :param list_id: ID of the dashboard list to delete.
        :type list_id: int
        :rtype: DashboardListDeleteResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["list_id"] = list_id

        return self._delete_dashboard_list_endpoint.call_with_http_info(**kwargs)

    def get_dashboard_list(
        self,
        list_id: int,
    ) -> DashboardList:
        """Get a dashboard list.

        Fetch an existing dashboard list's definition.

        :param list_id: ID of the dashboard list to fetch.
        :type list_id: int
        :rtype: DashboardList
        """
        kwargs: Dict[str, Any] = {}
        kwargs["list_id"] = list_id

        return self._get_dashboard_list_endpoint.call_with_http_info(**kwargs)

    def list_dashboard_lists(
        self,
    ) -> DashboardListListResponse:
        """Get all dashboard lists.

        Fetch all of your existing dashboard list definitions.

        :rtype: DashboardListListResponse
        """
        kwargs: Dict[str, Any] = {}
        return self._list_dashboard_lists_endpoint.call_with_http_info(**kwargs)

    def update_dashboard_list(
        self,
        list_id: int,
        body: DashboardList,
    ) -> DashboardList:
        """Update a dashboard list.

        Update the name of a dashboard list.

        :param list_id: ID of the dashboard list to update.
        :type list_id: int
        :param body: Update a dashboard list request body.
        :type body: DashboardList
        :rtype: DashboardList
        """
        kwargs: Dict[str, Any] = {}
        kwargs["list_id"] = list_id

        kwargs["body"] = body

        return self._update_dashboard_list_endpoint.call_with_http_info(**kwargs)
