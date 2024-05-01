# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

import collections
from typing import Any, Dict, List, Union

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.model_utils import (
    set_attribute_from_path,
    get_attribute_from_path,
    UnsetType,
    unset,
)
from datadog_api_client.v2.model.incidents_response import IncidentsResponse
from datadog_api_client.v2.model.incident_related_object import IncidentRelatedObject
from datadog_api_client.v2.model.incident_response_data import IncidentResponseData
from datadog_api_client.v2.model.incident_response import IncidentResponse
from datadog_api_client.v2.model.incident_create_request import IncidentCreateRequest
from datadog_api_client.v2.model.incident_search_response import IncidentSearchResponse
from datadog_api_client.v2.model.incident_search_sort_order import IncidentSearchSortOrder
from datadog_api_client.v2.model.incident_search_response_incidents_data import IncidentSearchResponseIncidentsData
from datadog_api_client.v2.model.incident_update_request import IncidentUpdateRequest
from datadog_api_client.v2.model.incident_attachments_response import IncidentAttachmentsResponse
from datadog_api_client.v2.model.incident_attachment_related_object import IncidentAttachmentRelatedObject
from datadog_api_client.v2.model.incident_attachment_attachment_type import IncidentAttachmentAttachmentType
from datadog_api_client.v2.model.incident_attachment_update_response import IncidentAttachmentUpdateResponse
from datadog_api_client.v2.model.incident_attachment_update_request import IncidentAttachmentUpdateRequest
from datadog_api_client.v2.model.incident_integration_metadata_list_response import (
    IncidentIntegrationMetadataListResponse,
)
from datadog_api_client.v2.model.incident_integration_metadata_response import IncidentIntegrationMetadataResponse
from datadog_api_client.v2.model.incident_integration_metadata_create_request import (
    IncidentIntegrationMetadataCreateRequest,
)
from datadog_api_client.v2.model.incident_integration_metadata_patch_request import (
    IncidentIntegrationMetadataPatchRequest,
)
from datadog_api_client.v2.model.incident_todo_list_response import IncidentTodoListResponse
from datadog_api_client.v2.model.incident_todo_response import IncidentTodoResponse
from datadog_api_client.v2.model.incident_todo_create_request import IncidentTodoCreateRequest
from datadog_api_client.v2.model.incident_todo_patch_request import IncidentTodoPatchRequest


class IncidentsApi:
    """
    Manage incident response.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_incident_endpoint = _Endpoint(
            settings={
                "response_type": (IncidentResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/incidents",
                "operation_id": "create_incident",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (IncidentCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._create_incident_integration_endpoint = _Endpoint(
            settings={
                "response_type": (IncidentIntegrationMetadataResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/incidents/{incident_id}/relationships/integrations",
                "operation_id": "create_incident_integration",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "incident_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "incident_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (IncidentIntegrationMetadataCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._create_incident_todo_endpoint = _Endpoint(
            settings={
                "response_type": (IncidentTodoResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/incidents/{incident_id}/relationships/todos",
                "operation_id": "create_incident_todo",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "incident_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "incident_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (IncidentTodoCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_incident_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/incidents/{incident_id}",
                "operation_id": "delete_incident",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "incident_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "incident_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._delete_incident_integration_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/incidents/{incident_id}/relationships/integrations/{integration_metadata_id}",
                "operation_id": "delete_incident_integration",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "incident_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "incident_id",
                    "location": "path",
                },
                "integration_metadata_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "integration_metadata_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._delete_incident_todo_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/incidents/{incident_id}/relationships/todos/{todo_id}",
                "operation_id": "delete_incident_todo",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "incident_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "incident_id",
                    "location": "path",
                },
                "todo_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "todo_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_incident_endpoint = _Endpoint(
            settings={
                "response_type": (IncidentResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/incidents/{incident_id}",
                "operation_id": "get_incident",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "incident_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "incident_id",
                    "location": "path",
                },
                "include": {
                    "openapi_types": ([IncidentRelatedObject],),
                    "attribute": "include",
                    "location": "query",
                    "collection_format": "csv",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_incident_integration_endpoint = _Endpoint(
            settings={
                "response_type": (IncidentIntegrationMetadataResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/incidents/{incident_id}/relationships/integrations/{integration_metadata_id}",
                "operation_id": "get_incident_integration",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "incident_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "incident_id",
                    "location": "path",
                },
                "integration_metadata_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "integration_metadata_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_incident_todo_endpoint = _Endpoint(
            settings={
                "response_type": (IncidentTodoResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/incidents/{incident_id}/relationships/todos/{todo_id}",
                "operation_id": "get_incident_todo",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "incident_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "incident_id",
                    "location": "path",
                },
                "todo_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "todo_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_incident_attachments_endpoint = _Endpoint(
            settings={
                "response_type": (IncidentAttachmentsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/incidents/{incident_id}/attachments",
                "operation_id": "list_incident_attachments",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "incident_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "incident_id",
                    "location": "path",
                },
                "include": {
                    "openapi_types": ([IncidentAttachmentRelatedObject],),
                    "attribute": "include",
                    "location": "query",
                    "collection_format": "csv",
                },
                "filter_attachment_type": {
                    "openapi_types": ([IncidentAttachmentAttachmentType],),
                    "attribute": "filter[attachment_type]",
                    "location": "query",
                    "collection_format": "csv",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_incident_integrations_endpoint = _Endpoint(
            settings={
                "response_type": (IncidentIntegrationMetadataListResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/incidents/{incident_id}/relationships/integrations",
                "operation_id": "list_incident_integrations",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "incident_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "incident_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_incidents_endpoint = _Endpoint(
            settings={
                "response_type": (IncidentsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/incidents",
                "operation_id": "list_incidents",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "include": {
                    "openapi_types": ([IncidentRelatedObject],),
                    "attribute": "include",
                    "location": "query",
                    "collection_format": "csv",
                },
                "page_size": {
                    "openapi_types": (int,),
                    "attribute": "page[size]",
                    "location": "query",
                },
                "page_offset": {
                    "openapi_types": (int,),
                    "attribute": "page[offset]",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_incident_todos_endpoint = _Endpoint(
            settings={
                "response_type": (IncidentTodoListResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/incidents/{incident_id}/relationships/todos",
                "operation_id": "list_incident_todos",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "incident_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "incident_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._search_incidents_endpoint = _Endpoint(
            settings={
                "response_type": (IncidentSearchResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/incidents/search",
                "operation_id": "search_incidents",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "include": {
                    "openapi_types": (IncidentRelatedObject,),
                    "attribute": "include",
                    "location": "query",
                },
                "query": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "query",
                    "location": "query",
                },
                "sort": {
                    "openapi_types": (IncidentSearchSortOrder,),
                    "attribute": "sort",
                    "location": "query",
                },
                "page_size": {
                    "openapi_types": (int,),
                    "attribute": "page[size]",
                    "location": "query",
                },
                "page_offset": {
                    "openapi_types": (int,),
                    "attribute": "page[offset]",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._update_incident_endpoint = _Endpoint(
            settings={
                "response_type": (IncidentResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/incidents/{incident_id}",
                "operation_id": "update_incident",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "incident_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "incident_id",
                    "location": "path",
                },
                "include": {
                    "openapi_types": ([IncidentRelatedObject],),
                    "attribute": "include",
                    "location": "query",
                    "collection_format": "csv",
                },
                "body": {
                    "required": True,
                    "openapi_types": (IncidentUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_incident_attachments_endpoint = _Endpoint(
            settings={
                "response_type": (IncidentAttachmentUpdateResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/incidents/{incident_id}/attachments",
                "operation_id": "update_incident_attachments",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "incident_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "incident_id",
                    "location": "path",
                },
                "include": {
                    "openapi_types": ([IncidentAttachmentRelatedObject],),
                    "attribute": "include",
                    "location": "query",
                    "collection_format": "csv",
                },
                "body": {
                    "required": True,
                    "openapi_types": (IncidentAttachmentUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_incident_integration_endpoint = _Endpoint(
            settings={
                "response_type": (IncidentIntegrationMetadataResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/incidents/{incident_id}/relationships/integrations/{integration_metadata_id}",
                "operation_id": "update_incident_integration",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "incident_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "incident_id",
                    "location": "path",
                },
                "integration_metadata_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "integration_metadata_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (IncidentIntegrationMetadataPatchRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_incident_todo_endpoint = _Endpoint(
            settings={
                "response_type": (IncidentTodoResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/incidents/{incident_id}/relationships/todos/{todo_id}",
                "operation_id": "update_incident_todo",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "incident_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "incident_id",
                    "location": "path",
                },
                "todo_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "todo_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (IncidentTodoPatchRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_incident(
        self,
        body: IncidentCreateRequest,
    ) -> IncidentResponse:
        """Create an incident.

        Create an incident.

        :param body: Incident payload.
        :type body: IncidentCreateRequest
        :rtype: IncidentResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_incident_endpoint.call_with_http_info(**kwargs)

    def create_incident_integration(
        self,
        incident_id: str,
        body: IncidentIntegrationMetadataCreateRequest,
    ) -> IncidentIntegrationMetadataResponse:
        """Create an incident integration metadata.

        Create an incident integration metadata.

        :param incident_id: The UUID of the incident.
        :type incident_id: str
        :param body: Incident integration metadata payload.
        :type body: IncidentIntegrationMetadataCreateRequest
        :rtype: IncidentIntegrationMetadataResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["incident_id"] = incident_id

        kwargs["body"] = body

        return self._create_incident_integration_endpoint.call_with_http_info(**kwargs)

    def create_incident_todo(
        self,
        incident_id: str,
        body: IncidentTodoCreateRequest,
    ) -> IncidentTodoResponse:
        """Create an incident todo.

        Create an incident todo.

        :param incident_id: The UUID of the incident.
        :type incident_id: str
        :param body: Incident todo payload.
        :type body: IncidentTodoCreateRequest
        :rtype: IncidentTodoResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["incident_id"] = incident_id

        kwargs["body"] = body

        return self._create_incident_todo_endpoint.call_with_http_info(**kwargs)

    def delete_incident(
        self,
        incident_id: str,
    ) -> None:
        """Delete an existing incident.

        Deletes an existing incident from the users organization.

        :param incident_id: The UUID of the incident.
        :type incident_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["incident_id"] = incident_id

        return self._delete_incident_endpoint.call_with_http_info(**kwargs)

    def delete_incident_integration(
        self,
        incident_id: str,
        integration_metadata_id: str,
    ) -> None:
        """Delete an incident integration metadata.

        Delete an incident integration metadata.

        :param incident_id: The UUID of the incident.
        :type incident_id: str
        :param integration_metadata_id: The UUID of the incident integration metadata.
        :type integration_metadata_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["incident_id"] = incident_id

        kwargs["integration_metadata_id"] = integration_metadata_id

        return self._delete_incident_integration_endpoint.call_with_http_info(**kwargs)

    def delete_incident_todo(
        self,
        incident_id: str,
        todo_id: str,
    ) -> None:
        """Delete an incident todo.

        Delete an incident todo.

        :param incident_id: The UUID of the incident.
        :type incident_id: str
        :param todo_id: The UUID of the incident todo.
        :type todo_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["incident_id"] = incident_id

        kwargs["todo_id"] = todo_id

        return self._delete_incident_todo_endpoint.call_with_http_info(**kwargs)

    def get_incident(
        self,
        incident_id: str,
        *,
        include: Union[List[IncidentRelatedObject], UnsetType] = unset,
    ) -> IncidentResponse:
        """Get the details of an incident.

        Get the details of an incident by ``incident_id``.

        :param incident_id: The UUID of the incident.
        :type incident_id: str
        :param include: Specifies which types of related objects should be included in the response.
        :type include: [IncidentRelatedObject], optional
        :rtype: IncidentResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["incident_id"] = incident_id

        if include is not unset:
            kwargs["include"] = include

        return self._get_incident_endpoint.call_with_http_info(**kwargs)

    def get_incident_integration(
        self,
        incident_id: str,
        integration_metadata_id: str,
    ) -> IncidentIntegrationMetadataResponse:
        """Get incident integration metadata details.

        Get incident integration metadata details.

        :param incident_id: The UUID of the incident.
        :type incident_id: str
        :param integration_metadata_id: The UUID of the incident integration metadata.
        :type integration_metadata_id: str
        :rtype: IncidentIntegrationMetadataResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["incident_id"] = incident_id

        kwargs["integration_metadata_id"] = integration_metadata_id

        return self._get_incident_integration_endpoint.call_with_http_info(**kwargs)

    def get_incident_todo(
        self,
        incident_id: str,
        todo_id: str,
    ) -> IncidentTodoResponse:
        """Get incident todo details.

        Get incident todo details.

        :param incident_id: The UUID of the incident.
        :type incident_id: str
        :param todo_id: The UUID of the incident todo.
        :type todo_id: str
        :rtype: IncidentTodoResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["incident_id"] = incident_id

        kwargs["todo_id"] = todo_id

        return self._get_incident_todo_endpoint.call_with_http_info(**kwargs)

    def list_incident_attachments(
        self,
        incident_id: str,
        *,
        include: Union[List[IncidentAttachmentRelatedObject], UnsetType] = unset,
        filter_attachment_type: Union[List[IncidentAttachmentAttachmentType], UnsetType] = unset,
    ) -> IncidentAttachmentsResponse:
        """Get a list of attachments.

        Get all attachments for a given incident.

        :param incident_id: The UUID of the incident.
        :type incident_id: str
        :param include: Specifies which types of related objects are included in the response.
        :type include: [IncidentAttachmentRelatedObject], optional
        :param filter_attachment_type: Specifies which types of attachments are included in the response.
        :type filter_attachment_type: [IncidentAttachmentAttachmentType], optional
        :rtype: IncidentAttachmentsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["incident_id"] = incident_id

        if include is not unset:
            kwargs["include"] = include

        if filter_attachment_type is not unset:
            kwargs["filter_attachment_type"] = filter_attachment_type

        return self._list_incident_attachments_endpoint.call_with_http_info(**kwargs)

    def list_incident_integrations(
        self,
        incident_id: str,
    ) -> IncidentIntegrationMetadataListResponse:
        """Get a list of an incident's integration metadata.

        Get all integration metadata for an incident.

        :param incident_id: The UUID of the incident.
        :type incident_id: str
        :rtype: IncidentIntegrationMetadataListResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["incident_id"] = incident_id

        return self._list_incident_integrations_endpoint.call_with_http_info(**kwargs)

    def list_incidents(
        self,
        *,
        include: Union[List[IncidentRelatedObject], UnsetType] = unset,
        page_size: Union[int, UnsetType] = unset,
        page_offset: Union[int, UnsetType] = unset,
    ) -> IncidentsResponse:
        """Get a list of incidents.

        Get all incidents for the user's organization.

        :param include: Specifies which types of related objects should be included in the response.
        :type include: [IncidentRelatedObject], optional
        :param page_size: Size for a given page. The maximum allowed value is 5000.
        :type page_size: int, optional
        :param page_offset: Specific offset to use as the beginning of the returned page.
        :type page_offset: int, optional
        :rtype: IncidentsResponse
        """
        kwargs: Dict[str, Any] = {}
        if include is not unset:
            kwargs["include"] = include

        if page_size is not unset:
            kwargs["page_size"] = page_size

        if page_offset is not unset:
            kwargs["page_offset"] = page_offset

        return self._list_incidents_endpoint.call_with_http_info(**kwargs)

    def list_incidents_with_pagination(
        self,
        *,
        include: Union[List[IncidentRelatedObject], UnsetType] = unset,
        page_size: Union[int, UnsetType] = unset,
        page_offset: Union[int, UnsetType] = unset,
    ) -> collections.abc.Iterable[IncidentResponseData]:
        """Get a list of incidents.

        Provide a paginated version of :meth:`list_incidents`, returning all items.

        :param include: Specifies which types of related objects should be included in the response.
        :type include: [IncidentRelatedObject], optional
        :param page_size: Size for a given page. The maximum allowed value is 5000.
        :type page_size: int, optional
        :param page_offset: Specific offset to use as the beginning of the returned page.
        :type page_offset: int, optional

        :return: A generator of paginated results.
        :rtype: collections.abc.Iterable[IncidentResponseData]
        """
        kwargs: Dict[str, Any] = {}
        if include is not unset:
            kwargs["include"] = include

        if page_size is not unset:
            kwargs["page_size"] = page_size

        if page_offset is not unset:
            kwargs["page_offset"] = page_offset

        local_page_size = get_attribute_from_path(kwargs, "page_size", 10)
        endpoint = self._list_incidents_endpoint
        set_attribute_from_path(kwargs, "page_size", local_page_size, endpoint.params_map)
        while True:
            response = endpoint.call_with_http_info(**kwargs)
            for item in get_attribute_from_path(response, "data"):
                yield item
            if len(get_attribute_from_path(response, "data")) < local_page_size:
                break
            set_attribute_from_path(
                kwargs,
                "page_offset",
                get_attribute_from_path(kwargs, "page_offset", 0) + local_page_size,
                endpoint.params_map,
            )

    def list_incident_todos(
        self,
        incident_id: str,
    ) -> IncidentTodoListResponse:
        """Get a list of an incident's todos.

        Get all todos for an incident.

        :param incident_id: The UUID of the incident.
        :type incident_id: str
        :rtype: IncidentTodoListResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["incident_id"] = incident_id

        return self._list_incident_todos_endpoint.call_with_http_info(**kwargs)

    def search_incidents(
        self,
        query: str,
        *,
        include: Union[IncidentRelatedObject, UnsetType] = unset,
        sort: Union[IncidentSearchSortOrder, UnsetType] = unset,
        page_size: Union[int, UnsetType] = unset,
        page_offset: Union[int, UnsetType] = unset,
    ) -> IncidentSearchResponse:
        """Search for incidents.

        Search for incidents matching a certain query.

        :param query: Specifies which incidents should be returned. After entering a search query in your `Incidents page <https://app.datadoghq.com/incidents>`_ ,
            use the query parameter value in the URL of the page as the value for this parameter.

            The query can contain any number of incident facets joined by ``ANDs`` , along with multiple values for each of
            those facets joined by ``OR`` s, for instance: ``query="state:active AND severity:(SEV-2 OR SEV-1)"``.
        :type query: str
        :param include: Specifies which types of related objects should be included in the response.
        :type include: IncidentRelatedObject, optional
        :param sort: Specifies the order of returned incidents.
        :type sort: IncidentSearchSortOrder, optional
        :param page_size: Size for a given page. The maximum allowed value is 5000.
        :type page_size: int, optional
        :param page_offset: Specific offset to use as the beginning of the returned page.
        :type page_offset: int, optional
        :rtype: IncidentSearchResponse
        """
        kwargs: Dict[str, Any] = {}
        if include is not unset:
            kwargs["include"] = include

        kwargs["query"] = query

        if sort is not unset:
            kwargs["sort"] = sort

        if page_size is not unset:
            kwargs["page_size"] = page_size

        if page_offset is not unset:
            kwargs["page_offset"] = page_offset

        return self._search_incidents_endpoint.call_with_http_info(**kwargs)

    def search_incidents_with_pagination(
        self,
        query: str,
        *,
        include: Union[IncidentRelatedObject, UnsetType] = unset,
        sort: Union[IncidentSearchSortOrder, UnsetType] = unset,
        page_size: Union[int, UnsetType] = unset,
        page_offset: Union[int, UnsetType] = unset,
    ) -> collections.abc.Iterable[IncidentSearchResponseIncidentsData]:
        """Search for incidents.

        Provide a paginated version of :meth:`search_incidents`, returning all items.

        :param query: Specifies which incidents should be returned. After entering a search query in your `Incidents page <https://app.datadoghq.com/incidents>`_ ,
            use the query parameter value in the URL of the page as the value for this parameter.

            The query can contain any number of incident facets joined by ``ANDs`` , along with multiple values for each of
            those facets joined by ``OR`` s, for instance: ``query="state:active AND severity:(SEV-2 OR SEV-1)"``.
        :type query: str
        :param include: Specifies which types of related objects should be included in the response.
        :type include: IncidentRelatedObject, optional
        :param sort: Specifies the order of returned incidents.
        :type sort: IncidentSearchSortOrder, optional
        :param page_size: Size for a given page. The maximum allowed value is 5000.
        :type page_size: int, optional
        :param page_offset: Specific offset to use as the beginning of the returned page.
        :type page_offset: int, optional

        :return: A generator of paginated results.
        :rtype: collections.abc.Iterable[IncidentSearchResponseIncidentsData]
        """
        kwargs: Dict[str, Any] = {}
        if include is not unset:
            kwargs["include"] = include

        kwargs["query"] = query

        if sort is not unset:
            kwargs["sort"] = sort

        if page_size is not unset:
            kwargs["page_size"] = page_size

        if page_offset is not unset:
            kwargs["page_offset"] = page_offset

        local_page_size = get_attribute_from_path(kwargs, "page_size", 10)
        endpoint = self._search_incidents_endpoint
        set_attribute_from_path(kwargs, "page_size", local_page_size, endpoint.params_map)
        while True:
            response = endpoint.call_with_http_info(**kwargs)
            for item in get_attribute_from_path(response, "data.attributes.incidents"):
                yield item
            if len(get_attribute_from_path(response, "data.attributes.incidents")) < local_page_size:
                break
            set_attribute_from_path(
                kwargs,
                "page_offset",
                get_attribute_from_path(kwargs, "page_offset", 0) + local_page_size,
                endpoint.params_map,
            )

    def update_incident(
        self,
        incident_id: str,
        body: IncidentUpdateRequest,
        *,
        include: Union[List[IncidentRelatedObject], UnsetType] = unset,
    ) -> IncidentResponse:
        """Update an existing incident.

        Updates an incident. Provide only the attributes that should be updated as this request is a partial update.

        :param incident_id: The UUID of the incident.
        :type incident_id: str
        :param body: Incident Payload.
        :type body: IncidentUpdateRequest
        :param include: Specifies which types of related objects should be included in the response.
        :type include: [IncidentRelatedObject], optional
        :rtype: IncidentResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["incident_id"] = incident_id

        if include is not unset:
            kwargs["include"] = include

        kwargs["body"] = body

        return self._update_incident_endpoint.call_with_http_info(**kwargs)

    def update_incident_attachments(
        self,
        incident_id: str,
        body: IncidentAttachmentUpdateRequest,
        *,
        include: Union[List[IncidentAttachmentRelatedObject], UnsetType] = unset,
    ) -> IncidentAttachmentUpdateResponse:
        """Create, update, and delete incident attachments.

        The bulk update endpoint for creating, updating, and deleting attachments for a given incident.

        :param incident_id: The UUID of the incident.
        :type incident_id: str
        :param body: Incident Attachment Payload.
        :type body: IncidentAttachmentUpdateRequest
        :param include: Specifies which types of related objects are included in the response.
        :type include: [IncidentAttachmentRelatedObject], optional
        :rtype: IncidentAttachmentUpdateResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["incident_id"] = incident_id

        if include is not unset:
            kwargs["include"] = include

        kwargs["body"] = body

        return self._update_incident_attachments_endpoint.call_with_http_info(**kwargs)

    def update_incident_integration(
        self,
        incident_id: str,
        integration_metadata_id: str,
        body: IncidentIntegrationMetadataPatchRequest,
    ) -> IncidentIntegrationMetadataResponse:
        """Update an existing incident integration metadata.

        Update an existing incident integration metadata.

        :param incident_id: The UUID of the incident.
        :type incident_id: str
        :param integration_metadata_id: The UUID of the incident integration metadata.
        :type integration_metadata_id: str
        :param body: Incident integration metadata payload.
        :type body: IncidentIntegrationMetadataPatchRequest
        :rtype: IncidentIntegrationMetadataResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["incident_id"] = incident_id

        kwargs["integration_metadata_id"] = integration_metadata_id

        kwargs["body"] = body

        return self._update_incident_integration_endpoint.call_with_http_info(**kwargs)

    def update_incident_todo(
        self,
        incident_id: str,
        todo_id: str,
        body: IncidentTodoPatchRequest,
    ) -> IncidentTodoResponse:
        """Update an incident todo.

        Update an incident todo.

        :param incident_id: The UUID of the incident.
        :type incident_id: str
        :param todo_id: The UUID of the incident todo.
        :type todo_id: str
        :param body: Incident todo payload.
        :type body: IncidentTodoPatchRequest
        :rtype: IncidentTodoResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["incident_id"] = incident_id

        kwargs["todo_id"] = todo_id

        kwargs["body"] = body

        return self._update_incident_todo_endpoint.call_with_http_info(**kwargs)
