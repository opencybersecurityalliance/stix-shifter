# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v2.model.dashboard_list_delete_items_response import DashboardListDeleteItemsResponse
from datadog_api_client.v2.model.dashboard_list_delete_items_request import DashboardListDeleteItemsRequest
from datadog_api_client.v2.model.dashboard_list_items import DashboardListItems
from datadog_api_client.v2.model.dashboard_list_add_items_response import DashboardListAddItemsResponse
from datadog_api_client.v2.model.dashboard_list_add_items_request import DashboardListAddItemsRequest
from datadog_api_client.v2.model.dashboard_list_update_items_response import DashboardListUpdateItemsResponse
from datadog_api_client.v2.model.dashboard_list_update_items_request import DashboardListUpdateItemsRequest


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

        self._create_dashboard_list_items_endpoint = _Endpoint(
            settings={
                "response_type": (DashboardListAddItemsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/dashboard/lists/manual/{dashboard_list_id}/dashboards",
                "operation_id": "create_dashboard_list_items",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "dashboard_list_id": {
                    "required": True,
                    "openapi_types": (int,),
                    "attribute": "dashboard_list_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (DashboardListAddItemsRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_dashboard_list_items_endpoint = _Endpoint(
            settings={
                "response_type": (DashboardListDeleteItemsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/dashboard/lists/manual/{dashboard_list_id}/dashboards",
                "operation_id": "delete_dashboard_list_items",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "dashboard_list_id": {
                    "required": True,
                    "openapi_types": (int,),
                    "attribute": "dashboard_list_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (DashboardListDeleteItemsRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._get_dashboard_list_items_endpoint = _Endpoint(
            settings={
                "response_type": (DashboardListItems,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/dashboard/lists/manual/{dashboard_list_id}/dashboards",
                "operation_id": "get_dashboard_list_items",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "dashboard_list_id": {
                    "required": True,
                    "openapi_types": (int,),
                    "attribute": "dashboard_list_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._update_dashboard_list_items_endpoint = _Endpoint(
            settings={
                "response_type": (DashboardListUpdateItemsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/dashboard/lists/manual/{dashboard_list_id}/dashboards",
                "operation_id": "update_dashboard_list_items",
                "http_method": "PUT",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "dashboard_list_id": {
                    "required": True,
                    "openapi_types": (int,),
                    "attribute": "dashboard_list_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (DashboardListUpdateItemsRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_dashboard_list_items(
        self,
        dashboard_list_id: int,
        body: DashboardListAddItemsRequest,
    ) -> DashboardListAddItemsResponse:
        """Add Items to a Dashboard List.

        Add dashboards to an existing dashboard list.

        :param dashboard_list_id: ID of the dashboard list to add items to.
        :type dashboard_list_id: int
        :param body: Dashboards to add to the dashboard list.
        :type body: DashboardListAddItemsRequest
        :rtype: DashboardListAddItemsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["dashboard_list_id"] = dashboard_list_id

        kwargs["body"] = body

        return self._create_dashboard_list_items_endpoint.call_with_http_info(**kwargs)

    def delete_dashboard_list_items(
        self,
        dashboard_list_id: int,
        body: DashboardListDeleteItemsRequest,
    ) -> DashboardListDeleteItemsResponse:
        """Delete items from a dashboard list.

        Delete dashboards from an existing dashboard list.

        :param dashboard_list_id: ID of the dashboard list to delete items from.
        :type dashboard_list_id: int
        :param body: Dashboards to delete from the dashboard list.
        :type body: DashboardListDeleteItemsRequest
        :rtype: DashboardListDeleteItemsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["dashboard_list_id"] = dashboard_list_id

        kwargs["body"] = body

        return self._delete_dashboard_list_items_endpoint.call_with_http_info(**kwargs)

    def get_dashboard_list_items(
        self,
        dashboard_list_id: int,
    ) -> DashboardListItems:
        """Get items of a Dashboard List.

        Fetch the dashboard list’s dashboard definitions.

        :param dashboard_list_id: ID of the dashboard list to get items from.
        :type dashboard_list_id: int
        :rtype: DashboardListItems
        """
        kwargs: Dict[str, Any] = {}
        kwargs["dashboard_list_id"] = dashboard_list_id

        return self._get_dashboard_list_items_endpoint.call_with_http_info(**kwargs)

    def update_dashboard_list_items(
        self,
        dashboard_list_id: int,
        body: DashboardListUpdateItemsRequest,
    ) -> DashboardListUpdateItemsResponse:
        """Update items of a dashboard list.

        Update dashboards of an existing dashboard list.

        :param dashboard_list_id: ID of the dashboard list to update items from.
        :type dashboard_list_id: int
        :param body: New dashboards of the dashboard list.
        :type body: DashboardListUpdateItemsRequest
        :rtype: DashboardListUpdateItemsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["dashboard_list_id"] = dashboard_list_id

        kwargs["body"] = body

        return self._update_dashboard_list_items_endpoint.call_with_http_info(**kwargs)
