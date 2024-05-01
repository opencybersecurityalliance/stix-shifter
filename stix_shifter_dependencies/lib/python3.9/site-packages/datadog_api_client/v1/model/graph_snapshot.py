# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class GraphSnapshot(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "graph_def": (str,),
            "metric_query": (str,),
            "snapshot_url": (str,),
        }

    attribute_map = {
        "graph_def": "graph_def",
        "metric_query": "metric_query",
        "snapshot_url": "snapshot_url",
    }

    def __init__(
        self_,
        graph_def: Union[str, UnsetType] = unset,
        metric_query: Union[str, UnsetType] = unset,
        snapshot_url: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object representing a graph snapshot.

        :param graph_def: A JSON document defining the graph. ``graph_def`` can be used instead of ``metric_query``.
            The JSON document uses the `grammar defined here <https://docs.datadoghq.com/graphing/graphing_json/#grammar>`_
            and should be formatted to a single line then URL encoded.
        :type graph_def: str, optional

        :param metric_query: The metric query. One of ``metric_query`` or ``graph_def`` is required.
        :type metric_query: str, optional

        :param snapshot_url: URL of your `graph snapshot <https://docs.datadoghq.com/metrics/explorer/#snapshot>`_.
        :type snapshot_url: str, optional
        """
        if graph_def is not unset:
            kwargs["graph_def"] = graph_def
        if metric_query is not unset:
            kwargs["metric_query"] = metric_query
        if snapshot_url is not unset:
            kwargs["snapshot_url"] = snapshot_url
        super().__init__(kwargs)
