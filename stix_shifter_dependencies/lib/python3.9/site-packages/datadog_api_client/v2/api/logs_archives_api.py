# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.v2.model.logs_archive_order import LogsArchiveOrder
from datadog_api_client.v2.model.logs_archives import LogsArchives
from datadog_api_client.v2.model.logs_archive import LogsArchive
from datadog_api_client.v2.model.logs_archive_create_request import LogsArchiveCreateRequest
from datadog_api_client.v2.model.relationship_to_role import RelationshipToRole
from datadog_api_client.v2.model.roles_response import RolesResponse


class LogsArchivesApi:
    """
    Archives forward all the logs ingested to a cloud storage system.

    See the `Archives Page <https://app.datadoghq.com/logs/pipelines/archives>`_
    for a list of the archives currently configured in web UI.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._add_read_role_to_archive_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/logs/config/archives/{archive_id}/readers",
                "operation_id": "add_read_role_to_archive",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "archive_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "archive_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (RelationshipToRole,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["*/*"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._create_logs_archive_endpoint = _Endpoint(
            settings={
                "response_type": (LogsArchive,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/logs/config/archives",
                "operation_id": "create_logs_archive",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (LogsArchiveCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_logs_archive_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/logs/config/archives/{archive_id}",
                "operation_id": "delete_logs_archive",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "archive_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "archive_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_logs_archive_endpoint = _Endpoint(
            settings={
                "response_type": (LogsArchive,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/logs/config/archives/{archive_id}",
                "operation_id": "get_logs_archive",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "archive_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "archive_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_logs_archive_order_endpoint = _Endpoint(
            settings={
                "response_type": (LogsArchiveOrder,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/logs/config/archive-order",
                "operation_id": "get_logs_archive_order",
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

        self._list_archive_read_roles_endpoint = _Endpoint(
            settings={
                "response_type": (RolesResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/logs/config/archives/{archive_id}/readers",
                "operation_id": "list_archive_read_roles",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "archive_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "archive_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_logs_archives_endpoint = _Endpoint(
            settings={
                "response_type": (LogsArchives,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/logs/config/archives",
                "operation_id": "list_logs_archives",
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

        self._remove_role_from_archive_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/logs/config/archives/{archive_id}/readers",
                "operation_id": "remove_role_from_archive",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "archive_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "archive_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (RelationshipToRole,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["*/*"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_logs_archive_endpoint = _Endpoint(
            settings={
                "response_type": (LogsArchive,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/logs/config/archives/{archive_id}",
                "operation_id": "update_logs_archive",
                "http_method": "PUT",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "archive_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "archive_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (LogsArchiveCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_logs_archive_order_endpoint = _Endpoint(
            settings={
                "response_type": (LogsArchiveOrder,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/logs/config/archive-order",
                "operation_id": "update_logs_archive_order",
                "http_method": "PUT",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (LogsArchiveOrder,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def add_read_role_to_archive(
        self,
        archive_id: str,
        body: RelationshipToRole,
    ) -> None:
        """Grant role to an archive.

        Adds a read role to an archive. ( `Roles API <https://docs.datadoghq.com/api/v2/roles/>`_ )

        :param archive_id: The ID of the archive.
        :type archive_id: str
        :type body: RelationshipToRole
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["archive_id"] = archive_id

        kwargs["body"] = body

        return self._add_read_role_to_archive_endpoint.call_with_http_info(**kwargs)

    def create_logs_archive(
        self,
        body: LogsArchiveCreateRequest,
    ) -> LogsArchive:
        """Create an archive.

        Create an archive in your organization.

        :param body: The definition of the new archive.
        :type body: LogsArchiveCreateRequest
        :rtype: LogsArchive
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_logs_archive_endpoint.call_with_http_info(**kwargs)

    def delete_logs_archive(
        self,
        archive_id: str,
    ) -> None:
        """Delete an archive.

        Delete a given archive from your organization.

        :param archive_id: The ID of the archive.
        :type archive_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["archive_id"] = archive_id

        return self._delete_logs_archive_endpoint.call_with_http_info(**kwargs)

    def get_logs_archive(
        self,
        archive_id: str,
    ) -> LogsArchive:
        """Get an archive.

        Get a specific archive from your organization.

        :param archive_id: The ID of the archive.
        :type archive_id: str
        :rtype: LogsArchive
        """
        kwargs: Dict[str, Any] = {}
        kwargs["archive_id"] = archive_id

        return self._get_logs_archive_endpoint.call_with_http_info(**kwargs)

    def get_logs_archive_order(
        self,
    ) -> LogsArchiveOrder:
        """Get archive order.

        Get the current order of your archives.
        This endpoint takes no JSON arguments.

        :rtype: LogsArchiveOrder
        """
        kwargs: Dict[str, Any] = {}
        return self._get_logs_archive_order_endpoint.call_with_http_info(**kwargs)

    def list_archive_read_roles(
        self,
        archive_id: str,
    ) -> RolesResponse:
        """List read roles for an archive.

        Returns all read roles a given archive is restricted to.

        :param archive_id: The ID of the archive.
        :type archive_id: str
        :rtype: RolesResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["archive_id"] = archive_id

        return self._list_archive_read_roles_endpoint.call_with_http_info(**kwargs)

    def list_logs_archives(
        self,
    ) -> LogsArchives:
        """Get all archives.

        Get the list of configured logs archives with their definitions.

        :rtype: LogsArchives
        """
        kwargs: Dict[str, Any] = {}
        return self._list_logs_archives_endpoint.call_with_http_info(**kwargs)

    def remove_role_from_archive(
        self,
        archive_id: str,
        body: RelationshipToRole,
    ) -> None:
        """Revoke role from an archive.

        Removes a role from an archive. ( `Roles API <https://docs.datadoghq.com/api/v2/roles/>`_ )

        :param archive_id: The ID of the archive.
        :type archive_id: str
        :type body: RelationshipToRole
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["archive_id"] = archive_id

        kwargs["body"] = body

        return self._remove_role_from_archive_endpoint.call_with_http_info(**kwargs)

    def update_logs_archive(
        self,
        archive_id: str,
        body: LogsArchiveCreateRequest,
    ) -> LogsArchive:
        """Update an archive.

        Update a given archive configuration.

        **Note** : Using this method updates your archive configuration by **replacing**
        your current configuration with the new one sent to your Datadog organization.

        :param archive_id: The ID of the archive.
        :type archive_id: str
        :param body: New definition of the archive.
        :type body: LogsArchiveCreateRequest
        :rtype: LogsArchive
        """
        kwargs: Dict[str, Any] = {}
        kwargs["archive_id"] = archive_id

        kwargs["body"] = body

        return self._update_logs_archive_endpoint.call_with_http_info(**kwargs)

    def update_logs_archive_order(
        self,
        body: LogsArchiveOrder,
    ) -> LogsArchiveOrder:
        """Update archive order.

        Update the order of your archives. Since logs are processed sequentially, reordering an archive may change
        the structure and content of the data processed by other archives.

        **Note** : Using the ``PUT`` method updates your archive's order by replacing the current order
        with the new one.

        :param body: An object containing the new ordered list of archive IDs.
        :type body: LogsArchiveOrder
        :rtype: LogsArchiveOrder
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._update_logs_archive_order_endpoint.call_with_http_info(**kwargs)
