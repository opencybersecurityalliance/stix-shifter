# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict, List, Union

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.model_utils import (
    UnsetType,
    unset,
)
from datadog_api_client.v2.model.teams_response import TeamsResponse
from datadog_api_client.v2.model.list_teams_sort import ListTeamsSort
from datadog_api_client.v2.model.list_teams_include import ListTeamsInclude
from datadog_api_client.v2.model.team_response import TeamResponse
from datadog_api_client.v2.model.team_create_request import TeamCreateRequest
from datadog_api_client.v2.model.team_update_request import TeamUpdateRequest
from datadog_api_client.v2.model.team_links_response import TeamLinksResponse
from datadog_api_client.v2.model.team_link_response import TeamLinkResponse
from datadog_api_client.v2.model.team_link_create_request import TeamLinkCreateRequest
from datadog_api_client.v2.model.user_teams_response import UserTeamsResponse
from datadog_api_client.v2.model.get_team_memberships_sort import GetTeamMembershipsSort
from datadog_api_client.v2.model.user_team_response import UserTeamResponse
from datadog_api_client.v2.model.user_team_request import UserTeamRequest
from datadog_api_client.v2.model.user_team_update_request import UserTeamUpdateRequest
from datadog_api_client.v2.model.team_permission_settings_response import TeamPermissionSettingsResponse
from datadog_api_client.v2.model.team_permission_setting_response import TeamPermissionSettingResponse
from datadog_api_client.v2.model.team_permission_setting_update_request import TeamPermissionSettingUpdateRequest


class TeamsApi:
    """
    View and manage teams within Datadog.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._create_team_endpoint = _Endpoint(
            settings={
                "response_type": (TeamResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/team",
                "operation_id": "create_team",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (TeamCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._create_team_link_endpoint = _Endpoint(
            settings={
                "response_type": (TeamLinkResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/team/{team_id}/links",
                "operation_id": "create_team_link",
                "http_method": "POST",
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
                    "openapi_types": (TeamLinkCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._create_team_membership_endpoint = _Endpoint(
            settings={
                "response_type": (UserTeamResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/team/{team_id}/memberships",
                "operation_id": "create_team_membership",
                "http_method": "POST",
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
                    "openapi_types": (UserTeamRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_team_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/team/{team_id}",
                "operation_id": "delete_team",
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

        self._delete_team_link_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/team/{team_id}/links/{link_id}",
                "operation_id": "delete_team_link",
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
                "link_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "link_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._delete_team_membership_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/team/{team_id}/memberships/{user_id}",
                "operation_id": "delete_team_membership",
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
                "user_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "user_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_team_endpoint = _Endpoint(
            settings={
                "response_type": (TeamResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/team/{team_id}",
                "operation_id": "get_team",
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
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_team_link_endpoint = _Endpoint(
            settings={
                "response_type": (TeamLinkResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/team/{team_id}/links/{link_id}",
                "operation_id": "get_team_link",
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
                "link_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "link_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_team_links_endpoint = _Endpoint(
            settings={
                "response_type": (TeamLinksResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/team/{team_id}/links",
                "operation_id": "get_team_links",
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
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_team_memberships_endpoint = _Endpoint(
            settings={
                "response_type": (UserTeamsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/team/{team_id}/memberships",
                "operation_id": "get_team_memberships",
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
                    "openapi_types": (GetTeamMembershipsSort,),
                    "attribute": "sort",
                    "location": "query",
                },
                "filter_keyword": {
                    "openapi_types": (str,),
                    "attribute": "filter[keyword]",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_team_permission_settings_endpoint = _Endpoint(
            settings={
                "response_type": (TeamPermissionSettingsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/team/{team_id}/permission-settings",
                "operation_id": "get_team_permission_settings",
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
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_teams_endpoint = _Endpoint(
            settings={
                "response_type": (TeamsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/team",
                "operation_id": "list_teams",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "page_number": {
                    "openapi_types": (int,),
                    "attribute": "page[number]",
                    "location": "query",
                },
                "page_size": {
                    "openapi_types": (int,),
                    "attribute": "page[size]",
                    "location": "query",
                },
                "sort": {
                    "openapi_types": (ListTeamsSort,),
                    "attribute": "sort",
                    "location": "query",
                },
                "include": {
                    "openapi_types": ([ListTeamsInclude],),
                    "attribute": "include",
                    "location": "query",
                    "collection_format": "multi",
                },
                "filter_keyword": {
                    "openapi_types": (str,),
                    "attribute": "filter[keyword]",
                    "location": "query",
                },
                "filter_me": {
                    "openapi_types": (bool,),
                    "attribute": "filter[me]",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._update_team_endpoint = _Endpoint(
            settings={
                "response_type": (TeamResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/team/{team_id}",
                "operation_id": "update_team",
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
                    "openapi_types": (TeamUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_team_link_endpoint = _Endpoint(
            settings={
                "response_type": (TeamLinkResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/team/{team_id}/links/{link_id}",
                "operation_id": "update_team_link",
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
                "link_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "link_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (TeamLinkCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_team_membership_endpoint = _Endpoint(
            settings={
                "response_type": (UserTeamResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/team/{team_id}/memberships/{user_id}",
                "operation_id": "update_team_membership",
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
                "user_id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "user_id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (UserTeamUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_team_permission_setting_endpoint = _Endpoint(
            settings={
                "response_type": (TeamPermissionSettingResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/team/{team_id}/permission-settings/{action}",
                "operation_id": "update_team_permission_setting",
                "http_method": "PUT",
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
                "action": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "action",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (TeamPermissionSettingUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def create_team(
        self,
        body: TeamCreateRequest,
    ) -> TeamResponse:
        """Create a team.

        Create a new team.
        User IDs passed through the ``users`` relationship field are added to the team.

        :type body: TeamCreateRequest
        :rtype: TeamResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_team_endpoint.call_with_http_info(**kwargs)

    def create_team_link(
        self,
        team_id: str,
        body: TeamLinkCreateRequest,
    ) -> TeamLinkResponse:
        """Create a team link.

        Add a new link to a team.

        :param team_id: None
        :type team_id: str
        :type body: TeamLinkCreateRequest
        :rtype: TeamLinkResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["team_id"] = team_id

        kwargs["body"] = body

        return self._create_team_link_endpoint.call_with_http_info(**kwargs)

    def create_team_membership(
        self,
        team_id: str,
        body: UserTeamRequest,
    ) -> UserTeamResponse:
        """Add a user to a team.

        Add a user to a team.

        :param team_id: None
        :type team_id: str
        :type body: UserTeamRequest
        :rtype: UserTeamResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["team_id"] = team_id

        kwargs["body"] = body

        return self._create_team_membership_endpoint.call_with_http_info(**kwargs)

    def delete_team(
        self,
        team_id: str,
    ) -> None:
        """Remove a team.

        Remove a team using the team's ``id``.

        :param team_id: None
        :type team_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["team_id"] = team_id

        return self._delete_team_endpoint.call_with_http_info(**kwargs)

    def delete_team_link(
        self,
        team_id: str,
        link_id: str,
    ) -> None:
        """Remove a team link.

        Remove a link from a team.

        :param team_id: None
        :type team_id: str
        :param link_id: None
        :type link_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["team_id"] = team_id

        kwargs["link_id"] = link_id

        return self._delete_team_link_endpoint.call_with_http_info(**kwargs)

    def delete_team_membership(
        self,
        team_id: str,
        user_id: str,
    ) -> None:
        """Remove a user from a team.

        Remove a user from a team.

        :param team_id: None
        :type team_id: str
        :param user_id: None
        :type user_id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["team_id"] = team_id

        kwargs["user_id"] = user_id

        return self._delete_team_membership_endpoint.call_with_http_info(**kwargs)

    def get_team(
        self,
        team_id: str,
    ) -> TeamResponse:
        """Get a team.

        Get a single team using the team's ``id``.

        :param team_id: None
        :type team_id: str
        :rtype: TeamResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["team_id"] = team_id

        return self._get_team_endpoint.call_with_http_info(**kwargs)

    def get_team_link(
        self,
        team_id: str,
        link_id: str,
    ) -> TeamLinkResponse:
        """Get a team link.

        Get a single link for a team.

        :param team_id: None
        :type team_id: str
        :param link_id: None
        :type link_id: str
        :rtype: TeamLinkResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["team_id"] = team_id

        kwargs["link_id"] = link_id

        return self._get_team_link_endpoint.call_with_http_info(**kwargs)

    def get_team_links(
        self,
        team_id: str,
    ) -> TeamLinksResponse:
        """Get links for a team.

        Get all links for a given team.

        :param team_id: None
        :type team_id: str
        :rtype: TeamLinksResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["team_id"] = team_id

        return self._get_team_links_endpoint.call_with_http_info(**kwargs)

    def get_team_memberships(
        self,
        team_id: str,
        *,
        page_size: Union[int, UnsetType] = unset,
        page_number: Union[int, UnsetType] = unset,
        sort: Union[GetTeamMembershipsSort, UnsetType] = unset,
        filter_keyword: Union[str, UnsetType] = unset,
    ) -> UserTeamsResponse:
        """Get team memberships.

        Get a paginated list of members for a team

        :param team_id: None
        :type team_id: str
        :param page_size: Size for a given page. The maximum allowed value is 5000.
        :type page_size: int, optional
        :param page_number: Specific page number to return.
        :type page_number: int, optional
        :param sort: Specifies the order of returned team memberships
        :type sort: GetTeamMembershipsSort, optional
        :param filter_keyword: Search query, can be user email or name
        :type filter_keyword: str, optional
        :rtype: UserTeamsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["team_id"] = team_id

        if page_size is not unset:
            kwargs["page_size"] = page_size

        if page_number is not unset:
            kwargs["page_number"] = page_number

        if sort is not unset:
            kwargs["sort"] = sort

        if filter_keyword is not unset:
            kwargs["filter_keyword"] = filter_keyword

        return self._get_team_memberships_endpoint.call_with_http_info(**kwargs)

    def get_team_permission_settings(
        self,
        team_id: str,
    ) -> TeamPermissionSettingsResponse:
        """Get permission settings for a team.

        Get all permission settings for a given team.

        :param team_id: None
        :type team_id: str
        :rtype: TeamPermissionSettingsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["team_id"] = team_id

        return self._get_team_permission_settings_endpoint.call_with_http_info(**kwargs)

    def list_teams(
        self,
        *,
        page_number: Union[int, UnsetType] = unset,
        page_size: Union[int, UnsetType] = unset,
        sort: Union[ListTeamsSort, UnsetType] = unset,
        include: Union[List[ListTeamsInclude], UnsetType] = unset,
        filter_keyword: Union[str, UnsetType] = unset,
        filter_me: Union[bool, UnsetType] = unset,
    ) -> TeamsResponse:
        """Get all teams.

        Get all teams.
        Can be used to search for teams using the ``filter[keyword]`` and ``filter[me]`` query parameters.

        :param page_number: Specific page number to return.
        :type page_number: int, optional
        :param page_size: Size for a given page. The maximum allowed value is 5000.
        :type page_size: int, optional
        :param sort: Specifies the order of the returned teams
        :type sort: ListTeamsSort, optional
        :param include: Included related resources optionally requested. Allowed enum values: ``team_links, user_team_permissions``
        :type include: [ListTeamsInclude], optional
        :param filter_keyword: Search query. Can be team name, team handle, or email of team member
        :type filter_keyword: str, optional
        :param filter_me: When true, only returns teams the current user belongs to
        :type filter_me: bool, optional
        :rtype: TeamsResponse
        """
        kwargs: Dict[str, Any] = {}
        if page_number is not unset:
            kwargs["page_number"] = page_number

        if page_size is not unset:
            kwargs["page_size"] = page_size

        if sort is not unset:
            kwargs["sort"] = sort

        if include is not unset:
            kwargs["include"] = include

        if filter_keyword is not unset:
            kwargs["filter_keyword"] = filter_keyword

        if filter_me is not unset:
            kwargs["filter_me"] = filter_me

        return self._list_teams_endpoint.call_with_http_info(**kwargs)

    def update_team(
        self,
        team_id: str,
        body: TeamUpdateRequest,
    ) -> TeamResponse:
        """Update a team.

        Update a team using the team's ``id``.
        If the ``team_links`` relationship is present, the associated links are updated to be in the order they appear in the array, and any existing team links not present are removed.

        :param team_id: None
        :type team_id: str
        :type body: TeamUpdateRequest
        :rtype: TeamResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["team_id"] = team_id

        kwargs["body"] = body

        return self._update_team_endpoint.call_with_http_info(**kwargs)

    def update_team_link(
        self,
        team_id: str,
        link_id: str,
        body: TeamLinkCreateRequest,
    ) -> TeamLinkResponse:
        """Update a team link.

        Update a team link.

        :param team_id: None
        :type team_id: str
        :param link_id: None
        :type link_id: str
        :type body: TeamLinkCreateRequest
        :rtype: TeamLinkResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["team_id"] = team_id

        kwargs["link_id"] = link_id

        kwargs["body"] = body

        return self._update_team_link_endpoint.call_with_http_info(**kwargs)

    def update_team_membership(
        self,
        team_id: str,
        user_id: str,
        body: UserTeamUpdateRequest,
    ) -> UserTeamResponse:
        """Update a user's membership attributes on a team.

        Update a user's membership attributes on a team.

        :param team_id: None
        :type team_id: str
        :param user_id: None
        :type user_id: str
        :type body: UserTeamUpdateRequest
        :rtype: UserTeamResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["team_id"] = team_id

        kwargs["user_id"] = user_id

        kwargs["body"] = body

        return self._update_team_membership_endpoint.call_with_http_info(**kwargs)

    def update_team_permission_setting(
        self,
        team_id: str,
        action: str,
        body: TeamPermissionSettingUpdateRequest,
    ) -> TeamPermissionSettingResponse:
        """Update permission setting for team.

        Update a team permission setting for a given team.

        :param team_id: None
        :type team_id: str
        :param action: None
        :type action: str
        :type body: TeamPermissionSettingUpdateRequest
        :rtype: TeamPermissionSettingResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["team_id"] = team_id

        kwargs["action"] = action

        kwargs["body"] = body

        return self._update_team_permission_setting_endpoint.call_with_http_info(**kwargs)
