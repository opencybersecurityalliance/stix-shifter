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
from datadog_api_client.v1.model.dashboard_bulk_delete_request import DashboardBulkDeleteRequest
from datadog_api_client.v1.model.dashboard_summary import DashboardSummary
from datadog_api_client.v1.model.dashboard_restore_request import DashboardRestoreRequest
from datadog_api_client.v1.model.dashboard import Dashboard
from datadog_api_client.v1.model.shared_dashboard import SharedDashboard
from datadog_api_client.v1.model.delete_shared_dashboard_response import DeleteSharedDashboardResponse
from datadog_api_client.v1.model.shared_dashboard_update_request import SharedDashboardUpdateRequest
from datadog_api_client.v1.model.shared_dashboard_invites import SharedDashboardInvites
from datadog_api_client.v1.model.dashboard_delete_response import DashboardDeleteResponse


class DashboardsApi:
    """
    Interact with your dashboard lists through the API to make it easier to organize,
    find, and share all of your dashboards with your team and organization.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_dashboard_endpoint = _Endpoint(
            settings={
                "response_type": (Dashboard,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/dashboard",
                "operation_id": "create_dashboard",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (Dashboard,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._create_public_dashboard_endpoint = _Endpoint(
            settings={
                "response_type": (SharedDashboard,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/dashboard/public",
                "operation_id": "create_public_dashboard",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (SharedDashboard,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_dashboard_endpoint = _Endpoint(
            settings={
                "response_type": (DashboardDeleteResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/dashboard/{dashboard_id}",
                "operation_id": "delete_dashboard",
                "http_method": "DELETE",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "dashboard_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "dashboard_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._delete_dashboards_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/dashboard",
                "operation_id": "delete_dashboards",
                "http_method": "DELETE",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (DashboardBulkDeleteRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["*/*"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_public_dashboard_endpoint = _Endpoint(
            settings={
                "response_type": (DeleteSharedDashboardResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/dashboard/public/{token}",
                "operation_id": "delete_public_dashboard",
                "http_method": "DELETE",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "token": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "token",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._delete_public_dashboard_invitation_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/dashboard/public/{token}/invitation",
                "operation_id": "delete_public_dashboard_invitation",
                "http_method": "DELETE",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "token": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "token",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (SharedDashboardInvites,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["*/*"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._get_dashboard_endpoint = _Endpoint(
            settings={
                "response_type": (Dashboard,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/dashboard/{dashboard_id}",
                "operation_id": "get_dashboard",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "dashboard_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "dashboard_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_public_dashboard_endpoint = _Endpoint(
            settings={
                "response_type": (SharedDashboard,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/dashboard/public/{token}",
                "operation_id": "get_public_dashboard",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "token": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "token",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_public_dashboard_invitations_endpoint = _Endpoint(
            settings={
                "response_type": (SharedDashboardInvites,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/dashboard/public/{token}/invitation",
                "operation_id": "get_public_dashboard_invitations",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "token": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "token",
                    "location": "path",
                },
                "page_size": {
                    "openapi_types": (int,),
                    "attribute": "page_size",
                    "location": "query",
                },
                "page_number": {
                    "openapi_types": (int,),
                    "attribute": "page_number",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_dashboards_endpoint = _Endpoint(
            settings={
                "response_type": (DashboardSummary,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/dashboard",
                "operation_id": "list_dashboards",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "filter_shared": {
                    "openapi_types": (bool,),
                    "attribute": "filter[shared]",
                    "location": "query",
                },
                "filter_deleted": {
                    "openapi_types": (bool,),
                    "attribute": "filter[deleted]",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._restore_dashboards_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/dashboard",
                "operation_id": "restore_dashboards",
                "http_method": "PATCH",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (DashboardRestoreRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["*/*"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._send_public_dashboard_invitation_endpoint = _Endpoint(
            settings={
                "response_type": (SharedDashboardInvites,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/dashboard/public/{token}/invitation",
                "operation_id": "send_public_dashboard_invitation",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "token": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "token",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (SharedDashboardInvites,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_dashboard_endpoint = _Endpoint(
            settings={
                "response_type": (Dashboard,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/dashboard/{dashboard_id}",
                "operation_id": "update_dashboard",
                "http_method": "PUT",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "dashboard_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "dashboard_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (Dashboard,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_public_dashboard_endpoint = _Endpoint(
            settings={
                "response_type": (SharedDashboard,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/dashboard/public/{token}",
                "operation_id": "update_public_dashboard",
                "http_method": "PUT",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "token": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "token",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (SharedDashboardUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_dashboard(
        self,
        body: Dashboard,
    ) -> Dashboard:
        """Create a new dashboard.

        Create a dashboard using the specified options. When defining queries in your widgets, take note of which queries should have the ``as_count()`` or ``as_rate()`` modifiers appended.
        Refer to the following `documentation <https://docs.datadoghq.com/developers/metrics/type_modifiers/?tab=count#in-application-modifiers>`_ for more information on these modifiers.

        :param body: Create a dashboard request body.
        :type body: Dashboard
        :rtype: Dashboard
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_dashboard_endpoint.call_with_http_info(**kwargs)

    def create_public_dashboard(
        self,
        body: SharedDashboard,
    ) -> SharedDashboard:
        """Create a shared dashboard.

        Share a specified private dashboard, generating a URL at which it can be publicly viewed.

        :param body: Create a shared dashboard request body.
        :type body: SharedDashboard
        :rtype: SharedDashboard
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_public_dashboard_endpoint.call_with_http_info(**kwargs)

    def delete_dashboard(
        self,
        dashboard_id: str,
    ) -> DashboardDeleteResponse:
        """Delete a dashboard.

        Delete a dashboard using the specified ID.

        :param dashboard_id: The ID of the dashboard.
        :type dashboard_id: str
        :rtype: DashboardDeleteResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["dashboard_id"] = dashboard_id

        return self._delete_dashboard_endpoint.call_with_http_info(**kwargs)

    def delete_dashboards(
        self,
        body: DashboardBulkDeleteRequest,
    ) -> None:
        """Delete dashboards.

        Delete dashboards using the specified IDs. If there are any failures, no dashboards will be deleted (partial success is not allowed).

        :param body: Delete dashboards request body.
        :type body: DashboardBulkDeleteRequest
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._delete_dashboards_endpoint.call_with_http_info(**kwargs)

    def delete_public_dashboard(
        self,
        token: str,
    ) -> DeleteSharedDashboardResponse:
        """Revoke a shared dashboard URL.

        Revoke the public URL for a dashboard (rendering it private) associated with the specified token.

        :param token: The token of the shared dashboard.
        :type token: str
        :rtype: DeleteSharedDashboardResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["token"] = token

        return self._delete_public_dashboard_endpoint.call_with_http_info(**kwargs)

    def delete_public_dashboard_invitation(
        self,
        token: str,
        body: SharedDashboardInvites,
    ) -> None:
        """Revoke shared dashboard invitations.

        Revoke previously sent invitation emails and active sessions used to access a given shared dashboard for specific email addresses.

        :param token: The token of the shared dashboard.
        :type token: str
        :param body: Shared Dashboard Invitation deletion request body.
        :type body: SharedDashboardInvites
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["token"] = token

        kwargs["body"] = body

        return self._delete_public_dashboard_invitation_endpoint.call_with_http_info(**kwargs)

    def get_dashboard(
        self,
        dashboard_id: str,
    ) -> Dashboard:
        """Get a dashboard.

        Get a dashboard using the specified ID.

        :param dashboard_id: The ID of the dashboard.
        :type dashboard_id: str
        :rtype: Dashboard
        """
        kwargs: Dict[str, Any] = {}
        kwargs["dashboard_id"] = dashboard_id

        return self._get_dashboard_endpoint.call_with_http_info(**kwargs)

    def get_public_dashboard(
        self,
        token: str,
    ) -> SharedDashboard:
        """Get a shared dashboard.

        Fetch an existing shared dashboard's sharing metadata associated with the specified token.

        :param token: The token of the shared dashboard. Generated when a dashboard is shared.
        :type token: str
        :rtype: SharedDashboard
        """
        kwargs: Dict[str, Any] = {}
        kwargs["token"] = token

        return self._get_public_dashboard_endpoint.call_with_http_info(**kwargs)

    def get_public_dashboard_invitations(
        self,
        token: str,
        *,
        page_size: Union[int, UnsetType] = unset,
        page_number: Union[int, UnsetType] = unset,
    ) -> SharedDashboardInvites:
        """Get all invitations for a shared dashboard.

        Describe the invitations that exist for the given shared dashboard (paginated).

        :param token: Token of the shared dashboard for which to fetch invitations.
        :type token: str
        :param page_size: The number of records to return in a single request.
        :type page_size: int, optional
        :param page_number: The page to access (base 0).
        :type page_number: int, optional
        :rtype: SharedDashboardInvites
        """
        kwargs: Dict[str, Any] = {}
        kwargs["token"] = token

        if page_size is not unset:
            kwargs["page_size"] = page_size

        if page_number is not unset:
            kwargs["page_number"] = page_number

        return self._get_public_dashboard_invitations_endpoint.call_with_http_info(**kwargs)

    def list_dashboards(
        self,
        *,
        filter_shared: Union[bool, UnsetType] = unset,
        filter_deleted: Union[bool, UnsetType] = unset,
    ) -> DashboardSummary:
        """Get all dashboards.

        Get all dashboards.

        **Note** : This query will only return custom created or cloned dashboards.
        This query will not return preset dashboards.

        :param filter_shared: When ``true`` , this query only returns shared custom created
            or cloned dashboards.
        :type filter_shared: bool, optional
        :param filter_deleted: When ``true`` , this query returns only deleted custom-created
            or cloned dashboards. This parameter is incompatible with ``filter[shared]``.
        :type filter_deleted: bool, optional
        :rtype: DashboardSummary
        """
        kwargs: Dict[str, Any] = {}
        if filter_shared is not unset:
            kwargs["filter_shared"] = filter_shared

        if filter_deleted is not unset:
            kwargs["filter_deleted"] = filter_deleted

        return self._list_dashboards_endpoint.call_with_http_info(**kwargs)

    def restore_dashboards(
        self,
        body: DashboardRestoreRequest,
    ) -> None:
        """Restore deleted dashboards.

        Restore dashboards using the specified IDs. If there are any failures, no dashboards will be restored (partial success is not allowed).

        :param body: Restore dashboards request body.
        :type body: DashboardRestoreRequest
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._restore_dashboards_endpoint.call_with_http_info(**kwargs)

    def send_public_dashboard_invitation(
        self,
        token: str,
        body: SharedDashboardInvites,
    ) -> SharedDashboardInvites:
        """Send shared dashboard invitation email.

        Send emails to specified email addresses containing links to access a given authenticated shared dashboard. Email addresses must already belong to the authenticated shared dashboard's share_list.

        :param token: The token of the shared dashboard.
        :type token: str
        :param body: Shared Dashboard Invitation request body.
        :type body: SharedDashboardInvites
        :rtype: SharedDashboardInvites
        """
        kwargs: Dict[str, Any] = {}
        kwargs["token"] = token

        kwargs["body"] = body

        return self._send_public_dashboard_invitation_endpoint.call_with_http_info(**kwargs)

    def update_dashboard(
        self,
        dashboard_id: str,
        body: Dashboard,
    ) -> Dashboard:
        """Update a dashboard.

        Update a dashboard using the specified ID.

        :param dashboard_id: The ID of the dashboard.
        :type dashboard_id: str
        :param body: Update Dashboard request body.
        :type body: Dashboard
        :rtype: Dashboard
        """
        kwargs: Dict[str, Any] = {}
        kwargs["dashboard_id"] = dashboard_id

        kwargs["body"] = body

        return self._update_dashboard_endpoint.call_with_http_info(**kwargs)

    def update_public_dashboard(
        self,
        token: str,
        body: SharedDashboardUpdateRequest,
    ) -> SharedDashboard:
        """Update a shared dashboard.

        Update a shared dashboard associated with the specified token.

        :param token: The token of the shared dashboard.
        :type token: str
        :param body: Update Dashboard request body.
        :type body: SharedDashboardUpdateRequest
        :rtype: SharedDashboard
        """
        kwargs: Dict[str, Any] = {}
        kwargs["token"] = token

        kwargs["body"] = body

        return self._update_public_dashboard_endpoint.call_with_http_info(**kwargs)
