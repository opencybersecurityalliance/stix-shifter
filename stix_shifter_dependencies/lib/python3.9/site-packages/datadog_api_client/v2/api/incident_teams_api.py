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
from datadog_api_client.v2.model.incident_teams_response import IncidentTeamsResponse
from datadog_api_client.v2.model.incident_related_object import IncidentRelatedObject
from datadog_api_client.v2.model.incident_team_response import IncidentTeamResponse
from datadog_api_client.v2.model.incident_team_create_request import IncidentTeamCreateRequest
from datadog_api_client.v2.model.incident_team_update_request import IncidentTeamUpdateRequest


class IncidentTeamsApi:
    """
    Create, update, delete and retrieve teams which can be associated with incidents.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_incident_team_endpoint = _Endpoint(
            settings={
                "response_type": (IncidentTeamResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/teams",
                "operation_id": "create_incident_team",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (IncidentTeamCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_incident_team_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/teams/{team_id}",
                "operation_id": "delete_incident_team",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "team_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "team_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_incident_team_endpoint = _Endpoint(
            settings={
                "response_type": (IncidentTeamResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/teams/{team_id}",
                "operation_id": "get_incident_team",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "team_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "team_id",
                    "location": "path",
                },
                "include": {
                    "openapi_types": (IncidentRelatedObject,),
                    "attribute": "include",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_incident_teams_endpoint = _Endpoint(
            settings={
                "response_type": (IncidentTeamsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/teams",
                "operation_id": "list_incident_teams",
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

        self._update_incident_team_endpoint = _Endpoint(
            settings={
                "response_type": (IncidentTeamResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/teams/{team_id}",
                "operation_id": "update_incident_team",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "team_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "team_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (IncidentTeamUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_incident_team(
        self,
        body: IncidentTeamCreateRequest,
    ) -> IncidentTeamResponse:
        """Create a new incident team.

        Creates a new incident team.

        :param body: Incident Team Payload.
        :type body: IncidentTeamCreateRequest
        :rtype: IncidentTeamResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_incident_team_endpoint.call_with_http_info(**kwargs)

    def delete_incident_team(
        self,
        team_id: str,
    ) -> None:
        """Delete an existing incident team.

        Deletes an existing incident team.

        :param team_id: The ID of the incident team.
        :type team_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["team_id"] = team_id

        return self._delete_incident_team_endpoint.call_with_http_info(**kwargs)

    def get_incident_team(
        self,
        team_id: str,
        *,
        include: Union[IncidentRelatedObject, UnsetType] = unset,
    ) -> IncidentTeamResponse:
        """Get details of an incident team.

        Get details of an incident team. If the ``include[users]`` query parameter is provided,
        the included attribute will contain the users related to these incident teams.

        :param team_id: The ID of the incident team.
        :type team_id: str
        :param include: Specifies which types of related objects should be included in the response.
        :type include: IncidentRelatedObject, optional
        :rtype: IncidentTeamResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["team_id"] = team_id

        if include is not unset:
            kwargs["include"] = include

        return self._get_incident_team_endpoint.call_with_http_info(**kwargs)

    def list_incident_teams(
        self,
        *,
        include: Union[IncidentRelatedObject, UnsetType] = unset,
        page_size: Union[int, UnsetType] = unset,
        page_offset: Union[int, UnsetType] = unset,
        filter: Union[str, UnsetType] = unset,
    ) -> IncidentTeamsResponse:
        """Get a list of all incident teams.

        Get all incident teams for the requesting user's organization. If the ``include[users]`` query parameter is provided, the included attribute will contain the users related to these incident teams.

        :param include: Specifies which types of related objects should be included in the response.
        :type include: IncidentRelatedObject, optional
        :param page_size: Size for a given page. The maximum allowed value is 5000.
        :type page_size: int, optional
        :param page_offset: Specific offset to use as the beginning of the returned page.
        :type page_offset: int, optional
        :param filter: A search query that filters teams by name.
        :type filter: str, optional
        :rtype: IncidentTeamsResponse
        """
        kwargs: Dict[str, Any] = {}
        if include is not unset:
            kwargs["include"] = include

        if page_size is not unset:
            kwargs["page_size"] = page_size

        if page_offset is not unset:
            kwargs["page_offset"] = page_offset

        if filter is not unset:
            kwargs["filter"] = filter

        return self._list_incident_teams_endpoint.call_with_http_info(**kwargs)

    def update_incident_team(
        self,
        team_id: str,
        body: IncidentTeamUpdateRequest,
    ) -> IncidentTeamResponse:
        """Update an existing incident team.

        Updates an existing incident team. Only provide the attributes which should be updated as this request is a partial update.

        :param team_id: The ID of the incident team.
        :type team_id: str
        :param body: Incident Team Payload.
        :type body: IncidentTeamUpdateRequest
        :rtype: IncidentTeamResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["team_id"] = team_id

        kwargs["body"] = body

        return self._update_incident_team_endpoint.call_with_http_info(**kwargs)
