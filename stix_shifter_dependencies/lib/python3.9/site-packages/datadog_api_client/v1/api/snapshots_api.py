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
from datadog_api_client.v1.model.graph_snapshot import GraphSnapshot


class SnapshotsApi:
    """
    Take graph snapshots using the API.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._get_graph_snapshot_endpoint = _Endpoint(
            settings={
                "response_type": (GraphSnapshot,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/graph/snapshot",
                "operation_id": "get_graph_snapshot",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "metric_query": {
                    "openapi_types": (str,),
                    "attribute": "metric_query",
                    "location": "query",
                },
                "start": {
                    "required": True,
                    "openapi_types": (int,),
                    "attribute": "start",
                    "location": "query",
                },
                "end": {
                    "required": True,
                    "openapi_types": (int,),
                    "attribute": "end",
                    "location": "query",
                },
                "event_query": {
                    "openapi_types": (str,),
                    "attribute": "event_query",
                    "location": "query",
                },
                "graph_def": {
                    "openapi_types": (str,),
                    "attribute": "graph_def",
                    "location": "query",
                },
                "title": {
                    "openapi_types": (str,),
                    "attribute": "title",
                    "location": "query",
                },
                "height": {
                    "openapi_types": (int,),
                    "attribute": "height",
                    "location": "query",
                },
                "width": {
                    "openapi_types": (int,),
                    "attribute": "width",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

    def get_graph_snapshot(
        self,
        start: int,
        end: int,
        *,
        metric_query: Union[str, UnsetType] = unset,
        event_query: Union[str, UnsetType] = unset,
        graph_def: Union[str, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        height: Union[int, UnsetType] = unset,
        width: Union[int, UnsetType] = unset,
    ) -> GraphSnapshot:
        """Take graph snapshots.

        Take graph snapshots.
        **Note** : When a snapshot is created, there is some delay before it is available.

        :param start: The POSIX timestamp of the start of the query in seconds.
        :type start: int
        :param end: The POSIX timestamp of the end of the query in seconds.
        :type end: int
        :param metric_query: The metric query.
        :type metric_query: str, optional
        :param event_query: A query that adds event bands to the graph.
        :type event_query: str, optional
        :param graph_def: A JSON document defining the graph. ``graph_def`` can be used instead of ``metric_query``.
            The JSON document uses the `grammar defined here <https://docs.datadoghq.com/graphing/graphing_json/#grammar>`_
            and should be formatted to a single line then URL encoded.
        :type graph_def: str, optional
        :param title: A title for the graph. If no title is specified, the graph does not have a title.
        :type title: str, optional
        :param height: The height of the graph. If no height is specified, the graph's original height is used.
        :type height: int, optional
        :param width: The width of the graph. If no width is specified, the graph's original width is used.
        :type width: int, optional
        :rtype: GraphSnapshot
        """
        kwargs: Dict[str, Any] = {}
        if metric_query is not unset:
            kwargs["metric_query"] = metric_query

        kwargs["start"] = start

        kwargs["end"] = end

        if event_query is not unset:
            kwargs["event_query"] = event_query

        if graph_def is not unset:
            kwargs["graph_def"] = graph_def

        if title is not unset:
            kwargs["title"] = title

        if height is not unset:
            kwargs["height"] = height

        if width is not unset:
            kwargs["width"] = width

        return self._get_graph_snapshot_endpoint.call_with_http_info(**kwargs)
