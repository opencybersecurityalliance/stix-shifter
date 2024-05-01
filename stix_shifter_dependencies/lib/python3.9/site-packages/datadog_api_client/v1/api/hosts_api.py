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
from datadog_api_client.v1.model.host_mute_response import HostMuteResponse
from datadog_api_client.v1.model.host_mute_settings import HostMuteSettings
from datadog_api_client.v1.model.host_list_response import HostListResponse
from datadog_api_client.v1.model.host_totals import HostTotals


class HostsApi:
    """
    Get information about your live hosts in Datadog.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._get_host_totals_endpoint = _Endpoint(
            settings={
                "response_type": (HostTotals,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/hosts/totals",
                "operation_id": "get_host_totals",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "_from": {
                    "openapi_types": (int,),
                    "attribute": "from",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_hosts_endpoint = _Endpoint(
            settings={
                "response_type": (HostListResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/hosts",
                "operation_id": "list_hosts",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "filter": {
                    "openapi_types": (str,),
                    "attribute": "filter",
                    "location": "query",
                },
                "sort_field": {
                    "openapi_types": (str,),
                    "attribute": "sort_field",
                    "location": "query",
                },
                "sort_dir": {
                    "openapi_types": (str,),
                    "attribute": "sort_dir",
                    "location": "query",
                },
                "start": {
                    "openapi_types": (int,),
                    "attribute": "start",
                    "location": "query",
                },
                "count": {
                    "openapi_types": (int,),
                    "attribute": "count",
                    "location": "query",
                },
                "_from": {
                    "openapi_types": (int,),
                    "attribute": "from",
                    "location": "query",
                },
                "include_muted_hosts_data": {
                    "openapi_types": (bool,),
                    "attribute": "include_muted_hosts_data",
                    "location": "query",
                },
                "include_hosts_metadata": {
                    "openapi_types": (bool,),
                    "attribute": "include_hosts_metadata",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._mute_host_endpoint = _Endpoint(
            settings={
                "response_type": (HostMuteResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/host/{host_name}/mute",
                "operation_id": "mute_host",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "host_name": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "host_name",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (HostMuteSettings,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._unmute_host_endpoint = _Endpoint(
            settings={
                "response_type": (HostMuteResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/host/{host_name}/unmute",
                "operation_id": "unmute_host",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "host_name": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "host_name",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

    def get_host_totals(
        self,
        *,
        _from: Union[int, UnsetType] = unset,
    ) -> HostTotals:
        """Get the total number of active hosts.

        This endpoint returns the total number of active and up hosts in your Datadog account.
        Active means the host has reported in the past hour, and up means it has reported in the past two hours.

        :param _from: Number of seconds from which you want to get total number of active hosts.
        :type _from: int, optional
        :rtype: HostTotals
        """
        kwargs: Dict[str, Any] = {}
        if _from is not unset:
            kwargs["_from"] = _from

        return self._get_host_totals_endpoint.call_with_http_info(**kwargs)

    def list_hosts(
        self,
        *,
        filter: Union[str, UnsetType] = unset,
        sort_field: Union[str, UnsetType] = unset,
        sort_dir: Union[str, UnsetType] = unset,
        start: Union[int, UnsetType] = unset,
        count: Union[int, UnsetType] = unset,
        _from: Union[int, UnsetType] = unset,
        include_muted_hosts_data: Union[bool, UnsetType] = unset,
        include_hosts_metadata: Union[bool, UnsetType] = unset,
    ) -> HostListResponse:
        """Get all hosts for your organization.

        This endpoint allows searching for hosts by name, alias, or tag.
        Hosts live within the past 3 hours are included by default.
        Retention is 7 days.
        Results are paginated with a max of 1000 results at a time.

        :param filter: String to filter search results.
        :type filter: str, optional
        :param sort_field: Sort hosts by this field.
        :type sort_field: str, optional
        :param sort_dir: Direction of sort. Options include ``asc`` and ``desc``.
        :type sort_dir: str, optional
        :param start: Host result to start search from.
        :type start: int, optional
        :param count: Number of hosts to return. Max 1000.
        :type count: int, optional
        :param _from: Number of seconds since UNIX epoch from which you want to search your hosts.
        :type _from: int, optional
        :param include_muted_hosts_data: Include information on the muted status of hosts and when the mute expires.
        :type include_muted_hosts_data: bool, optional
        :param include_hosts_metadata: Include additional metadata about the hosts (agent_version, machine, platform, processor, etc.).
        :type include_hosts_metadata: bool, optional
        :rtype: HostListResponse
        """
        kwargs: Dict[str, Any] = {}
        if filter is not unset:
            kwargs["filter"] = filter

        if sort_field is not unset:
            kwargs["sort_field"] = sort_field

        if sort_dir is not unset:
            kwargs["sort_dir"] = sort_dir

        if start is not unset:
            kwargs["start"] = start

        if count is not unset:
            kwargs["count"] = count

        if _from is not unset:
            kwargs["_from"] = _from

        if include_muted_hosts_data is not unset:
            kwargs["include_muted_hosts_data"] = include_muted_hosts_data

        if include_hosts_metadata is not unset:
            kwargs["include_hosts_metadata"] = include_hosts_metadata

        return self._list_hosts_endpoint.call_with_http_info(**kwargs)

    def mute_host(
        self,
        host_name: str,
        body: HostMuteSettings,
    ) -> HostMuteResponse:
        """Mute a host.

        Mute a host.

        :param host_name: Name of the host to mute.
        :type host_name: str
        :param body: Mute a host request body.
        :type body: HostMuteSettings
        :rtype: HostMuteResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["host_name"] = host_name

        kwargs["body"] = body

        return self._mute_host_endpoint.call_with_http_info(**kwargs)

    def unmute_host(
        self,
        host_name: str,
    ) -> HostMuteResponse:
        """Unmute a host.

        Unmutes a host. This endpoint takes no JSON arguments.

        :param host_name: Name of the host to unmute.
        :type host_name: str
        :rtype: HostMuteResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["host_name"] = host_name

        return self._unmute_host_endpoint.call_with_http_info(**kwargs)
